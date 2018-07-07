from flask import g

from .dialogue import Dialogue
from .monologue import Monologue
from .collections import Collections
from application.core import db
from application.core.constants import SOFTWARE_BRANCHES
from application.core.models import Course, SoftwareBranch
# from application.core.models import (Conversation, Course, Message,
#     NewsSource)
from application import projects
# from application.core.models.helpers import orm_get_section_by_id
from application.users.helpers import (add_course_to_offered,
    add_user_software_branch, create_new_user)
from application.wrappers.facebook.helpers import get_user_profile
# from application.readers.helpers import (create_new_reader,
#                                          add_source_to_reader_briefs,
#                                          drop_brief_source)


def get_response(sender_id, platform, text=None, attachments=None, nlp=None,
                 sticker_id=None, payload=None, title=None, is_postback=True):

    response = list()

    if text:
        text = text.lower()

    if sticker_id == 369239263222822:  # if thumbs-up
        response.append(('text', Monologue.blush()))

    elif payload:
        if payload == 'GET_STARTED_PAYLOAD':
            user_profile = get_user_profile(sender_id)
            create_new_user(
                first_name=user_profile.pop('first_name'),
                last_name=user_profile.pop('last_name'),
                uid=user_profile.pop('id'),
                blocs_platform=platform
            )

            welcome = Monologue.welcome()
            for statement in welcome:
                response.append(('text', statement))

            response.append(
                Dialogue.quick_reply(
                    title=Monologue.ask_for_software_branch(),
                    texts_and_payloads=[
                        (
                            branch, 'ADD_SOFTWARE_BRANCH__%s' % branch.upper()
                        )
                        for branch in SOFTWARE_BRANCHES
                    ]
                )
            )

        elif payload.startswith('ADD_SOFTWARE_BRANCH'):
            branch = payload.split('__')[1]

            branch_orm = SoftwareBranch.get(name=branch)

            add_user_software_branch(branch_orm.id)
            response.append(
                ('text', Monologue.compliment_software_branch(branch))
            )

        ### COURSES
        elif payload == 'DISPLAY_ALL_COURSES':
            response.append(('text', Monologue.take_to_all_courses()))
            response.append(('generic', Collections.all_courses()))

        elif payload == 'DISPLAY_ALL_COURSES_OFFERED':
            response.append(('text', Monologue.take_to_all_courses()))
            response.append(
                ('generic', Collections.all_courses(_tailored=True)))

        elif payload.startswith('DISPLAY_COURSE'):
            course_id = int(payload.split('__')[1])

            course = Course.get(id=course_id)

            order_now_quick_reply = Dialogue.quick_reply(
                title=Monologue.enquire_add_to_courses_offered(course.title),
                texts_and_payloads=[
                    ('YES', 'ADD_COURSE_TO_OFFERED__%s' % course_id),
                    ('No', 'NOTHING')
                ]
            )

            response.append(('text', Monologue.take_to_course()))
            response.append(('generic', Collections.course(course_id)))
            response.append(('quick_reply', order_now_quick_reply))

        elif payload.startswith('ADD_COURSE_TO_OFFERED'):
            course_id = int(payload.split('__')[1])

            add_course_to_offered(course_id)

        ### EVENTS
        elif payload == 'DISPLAY_ALL_EVENTS':
            response.append(('quick_reply', Dialogue.get_location()))
            response.append(('text', Monologue.take_to_all_events()))
            response.append(('generic', Collections.all_events()))

        elif payload == 'DISPLAY_ALL_EVENTS_INTERESTED_IN':
            response.append(('text', Monologue.take_to_all_events()))
            response.append(
                ('generic', Collections.all_events(_tailored=True)))

        elif payload.startswith('DISPLAY_EVENT'):
            event_id = int(payload.split('__')[1])

            response.append(('text', Monologue.take_to_event()))
            response.append(('generic', Collections.event(event_id)))

        ### JOBS
        elif payload == 'DISPLAY_ALL_JOBS':
            response.append(('text', Monologue.take_to_all_jobs()))
            response.append(('generic', Collections.all_jobs()))

        elif payload == 'DISPLAY_ALL_JOBS_INTERESTED_IN':
            response.append(('text', Monologue.take_to_all_jobs()))
            response.append(('generic', Collections.all_jobs(_tailored=True)))

        elif payload.startswith('DISPLAY_JOB'):
            job_id = int(payload.split('__')[1])

            response.append(('text', Monologue.take_to_job()))
            response.append(('generic', Collections.job(job_id)))

        elif payload.startswith('ADD_NEW_JOB'):
            response.append(('text', Monologue.take_to_all_jobs()))
            response.append(('generic', Collections.all_jobs(_tailored=True)))

        ### PROJECTS
        elif payload == 'DISPLAY_ALL_PROJECTS':
            response.append(('text', Monologue.take_to_all_projects()))
            response.append(('generic', Collections.all_projects()))

        elif payload == 'DISPLAY_ALL_PROJECTS_INTERESTED_IN':
            response.append(('text', Monologue.take_to_all_projects()))
            response.append(
                ('generic', Collections.all_projects(_tailored=True)))

        elif payload.startswith('DISPLAY_PROJECT'):
            project_id = int(payload.split('__')[1])

            response.append(('text', Monologue.take_to_project()))
            response.append(('generic', Collections.project(project_id)))

        elif payload.startswith('LIKE_PROJECT'):
            project_id = int(payload.split('__')[1])

            # response.append(('text', Monologue.take_to_project()))
            projects.like_bloc_project(project_id)
            response.append(('generic', Monologue.support_decision()))

        ### FEEDS
        elif payload == 'DISPLAY_ALL_FEEDS':
            response.append(('text', Monologue.take_to_all_feeds()))
            response.append(('generic', Collections.all_feeds()))

        elif payload.startswith('DISPLAY_JOB'):
            job_id = int(payload.split('__')[1])

            response.append(('text', Monologue.take_to_job()))
            response.append(('generic', Collections.job(job_id)))

    elif nlp and 'greetings' in list(nlp.keys()):
        response.append(('text', Monologue.greet()))
        response.append(('text', Monologue.take_to_all_schools()))
        response.append(('generic', Collections.all_sections()))

    return response


def save_message(response):
    try:
        # TODO make this get_user_active_conversation
        conversation = g.user.conversations[0]
    except:
        conversation = Conversation(reader_id=g.user.id)

    Message(
        content=str(response), conversation_id=conversation.id,
        origin='SENT').save()


def get_last_message():
    try:
        return Message.query.filter(
            Message.conversation_id == g.user.conversations[0].id
        ).order_by(
            Message.id.desc()
        ).first()

    except IndexError:
        return None


def to_send_response(response):
    last_message = get_last_message()

    if last_message is not None:
        return response[1] != eval(last_message.content)[1]

    return True
