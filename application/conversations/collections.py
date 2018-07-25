import random

from flask import g, url_for

from application.core.constants import (
    DEFAULT_BLOCS, MENU_ITEMS, PAGINATE_DEFAULT_PER_PAGE)
from application.core.models import Bloc
from .dialogue import Dialogue


class Collections(object):
    @classmethod
    def all_blocs(cls, page=1):
        blocs = Bloc.query.paginate(
            page=page, per_page=PAGINATE_DEFAULT_PER_PAGE
        ).items

        all_bloc_elements = []

        for bloc in blocs:
            if len(all_bloc_elements) == 10:
                break

            title = bloc.name
            # subtitle = bloc['body']
            image_url = url_for(
                'web_blueprint.render_default_avatar',
                color=bloc.theme_color, _external=True)

            buttons = [
                Dialogue.button(
                    type='web_url', title='READ',
                    url=bloc['url']
                )
            ]

            section_data = Dialogue.generic(
                title=title, subtitle=None, image_url=image_url,
                buttons=buttons
            )

            all_bloc_elements.append(section_data)

        return all_bloc_elements

    @classmethod
    def key_onboarding_features(cls):
        all_feature_elements = []

        features = [
            ("Courses", "Letting us take classes on Facebook/Instagram Live"),
            ("Projects", "Interacting, teaming-up, pair-coding with the "
             "awesome developers on Facebook"),
            ("Jobs", "Getting to find and hire the right people. Or even find "
                     "the best jobs, so effortlessly"),
            ("Events", "Always getting notifications about the close meetups "
                       "and events.")
        ]

        for title, subtitle in features:
            image_url = url_for(
                'web_blueprint.render_walkthrough_thumbnail',
                title=title,
                _external=True)

            # buttons = [
            #     Dialogue.button(
            #         type='web_url', title='READ',
            #         url=bloc['url']
            #     )
            # ]

            section_data = Dialogue.generic(
                title=title.upper(), subtitle=subtitle, image_url=image_url,
                buttons=None
                # buttons=buttons
            )

            all_feature_elements.append(section_data)

        return all_feature_elements

    @classmethod
    def all_default_blocs(cls, _location_id=None):
        blocs = Bloc.query.filter_by(
            is_default=True
        )

        # if _location_id is not None:
        #     blocs = blocs.filter_by(location_id=_location_id)
        #
        # print('AFTER LOCATION FILTER')

        all_bloc_elements = []

        for bloc in blocs:
            if len(all_bloc_elements) == PAGINATE_DEFAULT_PER_PAGE:
                break

            title = bloc.name.upper()
            image_url = url_for(
                'web_blueprint.render_default_avatar',
                color=bloc.theme_color, _external=True)

            buttons = [
                Dialogue.button(
                    type='postback', title='JOIN',
                    payload='JOIN_BLOC__%s' % bloc.id
                )
            ]

            bloc_data = Dialogue.generic(
                title=title, subtitle=None, image_url=image_url,
                buttons=buttons
            )

            all_bloc_elements.append(bloc_data)

        # APPEND BLOCS NOT TIED TO LOCATIONS
        # if len(all_bloc_elements) < PAGINATE_DEFAULT_PER_PAGE:
        #     all_bloc_elements.extend(cls.all_default_blocs())

        all_bloc_elements = all_bloc_elements[:PAGINATE_DEFAULT_PER_PAGE]

        print('ALL DEFAULT BLOC ELEMENTS: {}'.format(all_bloc_elements))
        print('BLOCS: {}'.format(blocs))

        return all_bloc_elements

    @classmethod
    def all_courses(cls, page=1, _tailored=False):
        courses = []

        if not _tailored:
            courses.extend(cls.create_course())

        for bloc in g.user.blocs:
            for course in bloc.courses:
                title = course.title
                description = '%s | %s' % (bloc.name, course.description)

                image_url = url_for(
                    'web_blueprint.render_course_thumbnail',
                    course_id=course.id,
                    _external=True)

                buttons = [
                    Dialogue.button(
                        type='postback', title='ADD',
                        payload='ADD_COURSE_TO_OFFERED__%s' % course.id
                    ),
                    Dialogue.button(
                        type='web_url', title='VIEW',
                        url=url_for('web_blueprint.render_course_details',
                                    id=course.id, _external=True)
                    )
                ]

                course_data = Dialogue.generic(
                    title=title, subtitle=description,
                    image_url=image_url,
                    buttons=buttons
                )

                courses.append(course_data)

        random.shuffle(courses)

        return courses[:10]

    @classmethod
    def all_events(cls, page=1, _tailored=False):
        all_event_elements = []

        if not _tailored:
            all_event_elements.extend(cls.create_event())

        for bloc in g.user.blocs:
            for event in bloc.events:

                if event.user_is_interested:
                    continue

                title = event.title
                subtitle = '%s | %s' % (bloc.name, event.description)

                buttons = [
                    Dialogue.button(
                        type='postback', title='INTERESTED',
                        payload='ADD_EVENT__%s' % event.id
                    ),
                    Dialogue.button(
                        type='web_url', title='VIEW',
                        url=url_for(
                            'web_blueprint.render_event_details',
                            event_id=event.id, _external=True)
                    )
                ]

                event_data = Dialogue.generic(
                    title=title, subtitle=subtitle,
                    image_url=url_for(
                        'web_blueprint.render_event_thumbnail',
                        event_id=event.id, _external=True),
                    buttons=buttons
                )

                all_event_elements.append(event_data)

        return all_event_elements

    @classmethod
    def all_feeds(cls):
        feeds = []

        for bloc in g.user.blocs:
            for feed in bloc.latest_feeds:

                message = feed.message
                subtitle = feed.body
                image_url = feed.get('image_url')

                buttons = [
                    Dialogue.button(
                        type='postback', title='LIKE',
                        payload='LIKE_FEED__%s' % feed.id
                    ),
                    Dialogue.button(
                        type='postback', title='REPLY',
                        payload='REPLY_FEED__%s' % feed.id
                    )
                ]

                section_data = Dialogue.generic(
                    title=message, subtitle=subtitle,
                    image_url=image_url,
                    buttons=buttons
                )

                feeds.append(section_data)

        random.shuffle(feeds)

        return feeds[:10]

    @classmethod
    def all_jobs(cls, page=1, _tailored=False):
        all_job_elements = []
        all_job_elements.extend(cls.create_job())

        for bloc in g.user.blocs:
            for job in bloc.jobs:

                title = job.title
                subtitle = job.description

                buttons = [
                    Dialogue.button(
                        type='web_url', title='APPLY',
                        url=url_for(
                            'web_blueprint.render_job_application_page',
                            job_id=job.id, user_id=g.user.id, _external=True)
                    ),
                    Dialogue.button(
                        type='web_url', title='VIEW',
                        url=url_for(
                            'web_blueprint.render_job_details_page',
                            id=job.id, user_id=g.user.id, _external=True)
                    )
                ]

                job_element = Dialogue.generic(
                    title=title, subtitle='%s | %s' % (bloc.name, subtitle),
                    image_url=url_for(
                        'web_blueprint.render_job_thumbnail', job_id=job.id,
                        _external=True
                    ),
                    buttons=buttons
                )

                all_job_elements.append(job_element)

        return all_job_elements

    @classmethod
    def all_projects(cls, page=1, _tailored=False):
        all_project_elements = []
        all_project_elements.extend(cls.create_project())

        for bloc in g.user.blocs:
            for project in bloc.projects:

                title = project.title
                subtitle = '%s | %s' % (bloc.name, project.description)

                buttons = [
                    Dialogue.button(
                        type='postback', title='LIKE',
                        payload='LIKE_PROJECT__%s' % project.id
                    ),
                    Dialogue.button(
                        type='web_url', title='VIEW',
                        url=url_for(
                            'web_blueprint.render_project_details_page',
                            user_id=g.user.id,
                            project_id=project.id, _external=True)
                    )
                ]

                project_element = Dialogue.generic(
                    title=title, subtitle=subtitle,
                    image_url=url_for(
                        'web_blueprint.render_project_thumbnail',
                        project_id=project.id,
                        _external=True
                    ),
                    buttons=buttons
                )

                all_project_elements.append(project_element)

        return all_project_elements

    @classmethod
    def project(cls, news_source):
        """Like | Open"""
        articles = get_existing_news_source_headlines(news_source)
        articles.reverse()

        articles = articles[:10]

        all_section_elements = []

        for article in articles:
            title = article['title']
            subtitle = article['body']

            buttons = [
                Dialogue.button(
                    type='web_url', title='READ',
                    url=article['url']
                )
            ]

            section_data = Dialogue.generic(
                title=title, subtitle=subtitle,
                image_url=article['image_url'],
                buttons=buttons
            )

            all_section_elements.append(section_data)

        return all_section_elements

    @classmethod
    def prompt_to_pin(cls, news_source):
        return

    @classmethod
    def create_event(cls):
        title = 'CREATE AN EVENT'
        subtitle = "Bring all the developers around your Blocs, under one roof"

        buttons = [
            Dialogue.button(
                type='web_url', title='PROCEED',
                url=url_for('web_blueprint.render_event_creation_page',
                            user_id=g.user.id, _external=True)
            )
        ]

        section_data = Dialogue.generic(
            title=title, subtitle=subtitle,
            image_url=url_for(
                'web_blueprint.render_random_default_avatar', _external=True),
            buttons=buttons
        )

        return [section_data]

    @classmethod
    def create_project(cls):
        title = 'CREATE A PROJECT'
        subtitle = (
            "Take-on big projects with developers all over the world!\nYour "
            "project will be shared on your Blocs, as well as your "
            "Facebook & Instagram pages, to let more developers know about it!")

        buttons = [
            Dialogue.button(
                type='web_url', title='PROCEED',
                url=url_for('web_blueprint.render_project_creation_page',
                            user_id=g.user.id, _external=True)
            )
        ]

        section_data = Dialogue.generic(
            title=title, subtitle=subtitle,
            image_url=url_for(
                'web_blueprint.render_random_default_avatar', user_id=g.user.id,
                _external=True),
            buttons=buttons
        )

        return [section_data]

    @classmethod
    def create_job(cls):
        title = 'CREATE A JOB'
        subtitle = (
            "Looking to hire someone?\nYour job offer will be shared on your "
            "Blocs, as well as your Facebook & Instagram pages, to help find "
            "more people!")

        buttons = [
            Dialogue.button(
                type='web_url', title='PROCEED',
                url=url_for('web_blueprint.render_job_creation_page',
                            user_id=g.user.id,
                            _external=True)
            )
        ]

        section_data = Dialogue.generic(
            title=title, subtitle=subtitle,
            image_url=url_for(
                'web_blueprint.render_random_default_avatar',
                user_id=g.user.id, _external=True),
            buttons=buttons
        )

        return [section_data]

    @classmethod
    def create_course(cls):

        title = 'CREATE A COURSE'
        subtitle = (
            "Gain respect & influence by passing on your awesome skills to "
            "other developers, through Facebook!")

        buttons = [
            Dialogue.button(
                type='web_url', title='PROCEED',
                url=url_for('web_blueprint.render_course_creation_page',
                            user_id=g.user.id, _external=True)
            )
        ]

        section_data = Dialogue.generic(
            title=title, subtitle=subtitle,
            image_url=url_for(
                'web_blueprint.render_random_default_avatar',
                user_id=g.user.id, _external=True),
            buttons=buttons
        )

        return [section_data]

    @classmethod
    def menu(cls):
        menu = []

        for name, description in MENU_ITEMS.items():
            title = name.upper()
            subtitle = description

            buttons = [
                Dialogue.button(
                    type='postback', title='VIEW',
                    payload='DISPLAY_ALL_{}'.format(title)
                )
            ]

            section_data = Dialogue.generic(
                title=title, subtitle=subtitle,
                image_url=url_for(
                    'web_blueprint.render_random_default_avatar',
                    _external=True),
                buttons=buttons
            )

            menu.append(section_data)

        return menu

    @classmethod
    def ask_to_view_project_likes(cls, project):
        text = '%s others also like %s' % (project.likes_count, project.title)
        all_view_project_options = [
            Dialogue.button(
                type='web_url', title='VIEW', url=url_for(
                'web_blueprint.render_all_project_likes',
                project_id=project.id, _external=True))
        ]

        # return dict that will be splatted because of double params
        # requirement for `buttons` message
        return {'text': text, 'buttons': all_view_project_options}

    @classmethod
    def ask_to_view_events_interested_in(cls):
        text = '%s, you have %s events coming up soon.' % (
            g.user.first_name, g.user.event_interests_count
        )

        all_view_project_options = [
            Dialogue.button(
                type='postback', title='VIEW',
                payload='DISPLAY_ALL_EVENTS_INTERESTED_IN'
            )
        ]

        # return dict that will be splatted because of double params
        # requirement for `buttons` message
        return {'text': text, 'buttons': all_view_project_options}

    @classmethod
    def ask_to_view_people_interested_in_event(cls, event):
        text = '%s others are also interested.' % (
            event.interest_count)

        all_view_project_options = [
            Dialogue.button(
                type='web_url', title='VIEW', url=url_for(
                'web_blueprint.render_all_event_interests',
                event_id=event.id, _external=True)
            )
        ]

        # return dict that will be splatted because of double params
        # requirement for `buttons` message
        return {'text': text, 'buttons': all_view_project_options}

    @classmethod
    def ask_to_view_people_offering_course(cls, course):
        text = '%s others also offer %s.' % (
            course.student_count, course.title)

        all_view_people_options = [
            Dialogue.button(
                type='web_url', title='VIEW', url=url_for(
                'web_blueprint.render_all_course_students',
                course_id=course.id, _external=True)
            )
        ]

        # return dict that will be splatted because of double params
        # requirement for `buttons` message
        return {'text': text, 'buttons': all_view_people_options}
