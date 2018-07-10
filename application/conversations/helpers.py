from flask import g

from .dialogue import Dialogue
from .monologue import Monologue
from .collections import Collections
from application.core import db
from application.core.constants import SOFTWARE_BRANCHES
from application.core.models import (BlocsPlatform, Conversation, Course,
    Message, SoftwareBranch)
from application import blocs, courses, events, location, projects
from application.users.helpers import (add_course_to_offered,
    add_user_software_branch, create_new_user)
from application.wrappers.facebook.helpers import get_user_profile


def set_conversation_course(title, index, response_type):
    return


def handle_attachment(attachments):
    response = list()

    for attachment in attachments:

        if attachment['type'] == 'location':
            payload = attachment['payload']

            user_location_coordinates = payload['coordinates']

            location.save_new_location(
                title=attachment['title'],
                coordinates=user_location_coordinates)

            response.append(('text', Monologue.compliment_location()))

            response.append(('text', Monologue.take_to_all_blocs()))

            response.append(
                (
                    'generic',
                    Collections.all_default_blocs(
                        _location_id=location.get_user_state_locale(g.user).id)
                )
            )

    return response


def handle_payload(sender_id, payload, platform='Facebook Bot'):
    response = list()

    elif isinstance(payload, str):
        if payload == 'GET_STARTED_PAYLOAD':
            user_profile = get_user_profile(sender_id)

            print('USER PROFILE: {}'.format(user_profile))

            blocs_platform = BlocsPlatform.get(name=platform)

            create_new_user(
                first_name=user_profile.pop('first_name'),
                last_name=user_profile.pop('last_name'),
                uid=user_profile.pop('id'),
                blocs_platform_id=blocs_platform.id,
                avatar_url=user_profile.pop('profile_pic')
            )

            welcome = Monologue.welcome()
            for statement in welcome:
                response.append(('text', statement))

            get_location = Dialogue.quick_reply(
                title=Monologue.request_location('Blocs'),
                texts_and_payloads=[
                    Dialogue.location_tuple()
                ]
            )

            response.append(('quick_reply', get_location))

        ### COURSES
        elif payload.startswith('CREATE_COURSE'):
            set_conversation_course(
                'COURSE', courses.COURSE_CREATION_STEPS[0], 'text')
            response.append(('text', Monologue.ask_for_course_title()))

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
            response.append(('text', Monologue.process_completion()))

        ### EVENTS
        elif payload.startswith('CREATE_EVENT'):
            set_conversation_course(
                'EVENT', events.EVENT_CREATION_STEPS[0], 'text')
            response.append(('text', Monologue.ask_for_event_title()))

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
        elif payload.startswith('CREATE_PROJECT'):
            set_conversation_course(
                'PROJECT', projects.PROJECT_CREATION_STEPS[0], 'text')
            response.append(('text', Monologue.ask_for_event_title()))

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

    return response


def get_response(sender_id, platform, text=None, attachments=None, nlp=None,
                 sticker_id=None, payload=None, title=None, is_postback=True):

    response = list()

    if text:
        text = text.lower()

    if sticker_id == 369239263222822:  # if thumbs-up
        response.append(('text', Monologue.blush()))

    elif payload:
        response = handle_payload(sender_id, payload)

    elif attachments:
        response = handle_attachment(attachments)

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
        conversation = Conversation(user_id=g.user.id)
        conversation.save()

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
