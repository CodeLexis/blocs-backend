from functools import wraps

from flask import g

from .dialogue import Dialogue
from .monologue import Monologue
from .collections import Collections
from application.core import db
from application.core.constants import SOFTWARE_BRANCHES
from application.core.models import (BlocsPlatform, Conversation, Course,
    Feed, Job, JobApplication, Message, Project, SoftwareBranch, User)
from application import blocs, courses, events, feeds, location, projects
from application.users.helpers import (add_course_to_offered,
    add_user_software_branch, create_new_user)
from application.wrappers.facebook.helpers import send_message, get_user_profile


def set_conversation_course(title, index=None, response_type=None):
    convo = g.user.conversations[-1]
    convo.update(expecting_response_for=title)


def handle_attachments(attachments):
    response = list()

    for attachment in attachments:

        if attachment['type'] == 'location':
            payload = attachment['payload']

            user_location_coordinates = payload['coordinates']

            location.save_new_location(
                title=attachment['title'],
                coordinates=user_location_coordinates)

            user_state_locale = location.get_user_state_locale(g.user)
            user_state_locale_id = None

            if user_state_locale is not None:
                user_state_locale_id = location.get_user_state_locale(g.user).id

            response.append(('text', Monologue.compliment_location()))

            response.append(('text', Monologue.take_to_all_blocs()))

            response.append(
                (
                    'generic',
                    Collections.all_default_blocs(
                        _location_id=user_state_locale_id)
                )
            )

        else:
            if g.user.conversations[-1].expecting_response_for.startswith(
                    'APPLY_FOR_JOB'):

                job_id = g.user.conversations[-1].expecting_response_for.split(
                    "__")[1]
                cv_url = attachment['payload']['url']

                job = Job.get(id=job_id)

                JobApplication(
                    cv=cv_url, job_id=job_id, created_by_id=g.user.id).save()

                # {'type': 'image', 'payload': {
                # 'url': 'https://scontent.xx.fbcdn.net/v/t1.15752-9/37772680_2197540350274914_6479394538988240896_n.png?_nc_cat=0&_nc_ad=z-m&_nc_cid=0&oh=5b595d781c5d080fe2ce272be21fb153&oe=5BD46D3A'}}

                send_message(
                    job.created_by.external_app_uid,
                    ('text', 'Hey {}, {} {} just applied for {}! Have a look '
                             'at the resume {} sent {}'.format(
                            job.created_by.first_name,
                            g.user.first_name, g.user.last_name,
                            job.title,
                            job.created_by.first_name,
                            cv_url
                        )
                    )
                )

                response.append(('text', Monologue.process_completion()))
                response.append(('text', Monologue.take_to_menu()))
                response.append(('text', Collections.menu()))

    return response


def blocs_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.has_bloc:
            return f(*args, **kwargs)

        else:
            response = list()

            response.append(('text', Monologue.ask_to_join_bloc()))
            response.append(('generic', Collections.all_default_blocs()))

            return response

    return decorated_function


@blocs_required
def handle_bloc_required_payload(payload):
    response = list()

    ### COURSES
    if payload == 'DISPLAY_ALL_COURSES':
        response.append(('text', Monologue.take_to_all_courses()))

        all_user_blocs_courses = Collections.all_courses()
        if len(all_user_blocs_courses) > 1:
            response.append(('generic', all_user_blocs_courses))
        else:
            response.append(
                ('text', Monologue.empty_resource(scope='course'))
            )
            response.append(
                ('generic', Collections.create_course())
            )

    elif payload == 'DISPLAY_ALL_COURSES_OFFERED':
        response.append(('text', Monologue.take_to_all_courses()))
        response.append(
            ('generic', Collections.all_courses(_tailored=True)))

    elif payload.startswith('ADD_COURSE_TO_OFFERED'):
        course_id = int(payload.split('__')[1])

        course = Course.get(id=course_id)

        add_course_to_offered(course_id)

        response.append(('text', Monologue.process_completion()))
        response.append(
            ('generic', Collections.ask_to_view_people_offering_course(
                course))
        )

    ### EVENTS
    elif payload == 'DISPLAY_ALL_EVENTS':
        if g.user.events_count:
            response.append(
                ('buttons', Collections.ask_to_view_events_created())
            )
        if g.user.event_interests_count:
            response.append(
                ('buttons', Collections.ask_to_view_events_interested_in())
            )

        response.append(('text', Monologue.take_to_all_events()))
        # response.append(('quick_reply', Dialogue.get_location()))
        all_events = Collections.all_events()
        if len(all_events) > 1:
            response.append(('generic', all_events))
        else:
            response.append(('text', Monologue.empty_resource('event')))
            response.append(('generic', Collections.create_event()))

    elif payload == 'DISPLAY_ALL_EVENTS_CREATED':
        response.append(('text', Monologue.take_to_events_created()))
        response.append(
            ('generic', Collections.all_events_created()))

    elif payload == 'DISPLAY_ALL_EVENTS_INTERESTED_IN':
        response.append(('text', Monologue.take_to_events_interested_in()))
        response.append(
            ('generic', Collections.all_events(_tailored=True)))

    elif payload.startswith('ADD_EVENT'):
        event_id = payload.split('__')[1]

        event_interest = events.declare_event_interest(event_id)

        response.append(('text', Monologue.process_completion()))

        response.append(
            ('buttons', Collections.ask_to_view_people_interested_in_event(
                event_interest.event))
        )

    ### JOBS
    elif payload == 'DISPLAY_ALL_JOBS':
        response.append(('text', Monologue.take_to_all_jobs()))

        all_user_blocs_jobs = Collections.all_jobs()

        if len(all_user_blocs_jobs) > 1:
            response.append(('generic', all_user_blocs_jobs))
        else:
            response.append(('text', Monologue.empty_resource('job')))
            response.append(('generic', Collections.create_job()))

    elif payload == 'DISPLAY_ALL_JOBS_INTERESTED_IN':
        response.append(('text', Monologue.take_to_all_jobs()))
        response.append(('generic', Collections.all_jobs(_tailored=True)))

    elif payload.startswith('APPLY_FOR_JOB'):
        set_conversation_course(payload)
        response.append(('text', Monologue.ask_to_send_cv()))

    ### PROJECTS
    elif payload == 'DISPLAY_ALL_PROJECTS':
        response.append(('text', Monologue.take_to_all_projects()))
        all_user_blocs_projects = Collections.all_projects()

        if len(all_user_blocs_projects) > 1:
            response.append(('generic', all_user_blocs_projects))
        else:
            response.append(('text', Monologue.empty_resource('project')))
            response.append(('generic', Collections.create_project()))

    elif payload == 'DISPLAY_ALL_PROJECTS_INTERESTED_IN':
        response.append(('text', Monologue.take_to_all_projects()))
        response.append(
            ('generic', Collections.all_projects(_tailored=True))
        )

    elif payload.startswith('LIKE_PROJECT'):
        project_id = int(payload.split('__')[1])

        projects.like_bloc_project(project_id)

        project = Project.get(id=project_id)

        response.append(('text', Monologue.support_decision()))
        response.append(
            ('buttons', Collections.ask_to_view_project_likes(project))
        )

    ### FEEDS
    elif payload == 'DISPLAY_ALL_FEEDS':
        response.append(('text', Monologue.take_to_all_feeds()))
        response.append(('generic', Collections.all_feeds()))

    elif payload.startswith('LIKE_FEED'):
        feed_id = int(payload.split('__')[1])

        feed = Feed.get(id=feed_id)

        feeds.like_feed(feed.external_app_uid, feed_id)

        response.append(('text', Monologue.compliment()))
        response.append(
            ('buttons',
             Collections.ask_to_view_people_that_liked_feed(feed))
        )

    elif payload.startswith('REPLY_FEED'):
        feed_id = int(payload.split('__')[1])

        feed = Feed.get(id=feed_id)

        set_conversation_course(payload)

        response.append(('text', Monologue.ask_for_reply(feed)))

    return response


def handle_payload(sender_id, payload, platform='Facebook Bot'):
    response = list()

    if payload == 'GET_STARTED_PAYLOAD':
        # If user already exists...
        # TODO uncomment this block for production code
        # if User.get(external_app_uid=sender_id) is not None:
        #     return

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
        response.append(('text', welcome[0]))
        response.append(('generic', Collections.key_onboarding_features()))

        for statement in welcome[1:]:
            response.append(('text', statement))

        response.append(('generic', Collections.all_default_blocs()))

        # get_location = Dialogue.quick_reply(
        #     title=Monologue.request_location_for_bloc(),
        #     texts_and_payloads=[
        #         Dialogue.location_tuple()
        #     ]
        # )
        #
        # response.append(('quick_reply', get_location))

    ### BLOCS
    elif payload.startswith('JOIN_BLOC'):
        bloc_id = int(payload.split('__')[1])
        blocs.join_bloc(g.user, bloc_id)

        response.append(('text', Monologue.support_decision()))
        response.append(('text', Monologue.instruct_on_posting_feeds()))
        response.append(('text', Monologue.take_to_menu()))
        response.append(('generic', Collections.menu()))

    else:
        response = handle_bloc_required_payload(payload)

    return response


def handle_text(text):
    response = list()

    current_convo = g.user.conversations[-1]

    expecting_response = (
        current_convo.expecting_response_for.startswith('REPLY_FEED')
    )

    if expecting_response:
        feed_id = expecting_response.split('__')[1]

        feed = Feed.get(id=feed_id)

        feeds.comment_on_feed(feed, text)

        response.append(('text', Monologue.compliment()))
        response.append(('buttons', Collections.ask_to_view_other_replies(
            feed)))

        current_convo.update(expecting_response=None)

    return response


def get_response(sender_id, platform, text=None, attachments=None, nlp=None,
                 sticker_id=None, payload=None, title=None, is_postback=True):

    response = list()

    if text:
        if text == 'WHOAMI':
            response.append(('text', Monologue.echo_user_details()))

        else:
            try:
                response = handle_text(text)
            except:
                pass

    if sticker_id == 369239263222822:  # if thumbs-up
        response.append(('text', Monologue.blush()))

    elif payload:
        response = handle_payload(sender_id, payload)

    elif attachments:
        response = handle_attachments(attachments)

    elif nlp and 'greetings' in list(nlp.keys()):
        response.append(('text', Monologue.greet()))

        if g.user.has_bloc:
            response.append(('text', Monologue.take_to_all_feeds()))
            response.append(('generic', Collections.all_feeds()))
        else:
            response.append(('text', Monologue.take_to_all_blocs()))
            response.append(('generic', Collections.all_default_blocs()))
        # response.append(('text', Monologue.take_to_all_courses()))
        # response.append(('generic', Collections.all_sections()))

    return response


def save_response(response):
    try:
        # TODO make this get_user_active_conversation
        conversation = g.user.conversations[-1]
    except:
        conversation = Conversation(user_id=g.user.id)
        conversation.save()

    print('User Conversation ID: %s' % conversation.id)

    Message(
        content=str(response), conversation_id=conversation.id,
        origin='SENT'
    ).save()


def get_last_message():
    try:
        return Message.query.filter(
            Message.conversation_id == g.user.conversations[-1].id
        ).order_by(
            Message.id.desc()
        ).first()

    except IndexError:
        return None


def to_send_response(response):
    last_message = get_last_message()

    if last_message is not None:
        print("LAST_MESSAGE IS:::::", last_message.content)
        print("RESPONSE:::::", response)

        return response != eval(last_message.content)

    return True
