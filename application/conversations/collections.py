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

        for bloc in g.user.blocs:
            for course in bloc.courses:
                title = course.title
                description = course.description
                image_url = url_for(
                    'web_blueprint.render_course_thumbnail', id=course.id,
                    _external=True)

                buttons = [
                    Dialogue.button(
                        type='postback', title='ADD',
                        payload='ADD_COURSE_TO_OFFERED__%s' % course.id
                    ),
                    Dialogue.button(
                        type='url', title='DETAILS',
                        url=url_for('web_blueprint.render_course_details',
                                    id=course.id, _external=True)
                    ),
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
    def course(cls, course_id):
        section_orm = Section.get(id=section_id)

        articles = get_existing_section_headlines(section_orm)[:70]
        # articles.reverse()

        random.shuffle(articles)

        all_headline_elements = []

        for article in articles:
            if len(all_headline_elements) == 10:
                break

            title = article['title']
            subtitle = article['body']
            image_url = article.get('image_url')

            buttons = [
                Dialogue.button(
                    type='web_url', title='READ',
                    url=article['url']
                )
            ]

            section_data = Dialogue.generic(
                title=title, subtitle=subtitle,
                image_url=image_url,
                buttons=buttons
            )

            all_headline_elements.append(section_data)

        return all_headline_elements

    @classmethod
    def all_events(cls, page=1, _tailored=False):
        all_event_elements = []

        for bloc in g.user.blocs:
            for event in bloc.events:

                title = event.title
                subtitle = '{} {}'.format(bloc.name, event.description)

                buttons = [
                    Dialogue.button(
                        type='web_url', title='VIEW',
                        payload=url_for(
                            'web_blueprint.render_event_details',
                            id=event.id, _external=True)
                    )
                ]

                event_data = Dialogue.generic(
                    title=title.upper(), subtitle=subtitle,
                    image_url=url_for(
                        'web_blueprint.render_event_thumbnail',
                        id=event.id, _external=True),
                    buttons=buttons
                )

                all_event_elements.append(event_data)

        return all_event_elements

    @classmethod
    def event(cls, section_id):
        section_orm = Section.get(id=section_id)

        articles = get_existing_section_headlines(section_orm)[:70]
        # articles.reverse()

        random.shuffle(articles)

        all_headline_elements = []

        for article in articles:
            if len(all_headline_elements) == 10:
                break

            title = article['title']
            subtitle = article['body']
            image_url = article.get('image_url')

            buttons = [
                Dialogue.button(
                    type='web_url', title='READ',
                    url=article['url']
                )
            ]

            section_data = Dialogue.generic(
                title=title, subtitle=subtitle,
                image_url=image_url,
                buttons=buttons
            )

            all_headline_elements.append(section_data)

        return all_headline_elements

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
                        type='postback', title='REPLIES (4)',
                        payload='REPLY_FEED__%s' % feed.id
                    ),
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

        for bloc in g.user.blocs:
            for job in bloc.jobs:

                title = job.title
                subtitle = job.description

                buttons = [
                    Dialogue.button(
                        type='web_url', title='VIEW',
                        payload=url_for(
                            'web_blueprint.render_job_details_page',
                            id=job.id, _external=True)
                    )
                ]

                job_element = Dialogue.generic(
                    title=title.upper(), subtitle=subtitle,
                    image_url=url_for(
                        'web_blueprint.render_job_thumbnail', id=job.id,
                        _external=True
                    ),
                    buttons=buttons
                )

                all_job_elements.append(job_element)

        return all_job_elements

    @classmethod
    def job(cls, section_id):
        section_orm = Section.get(id=section_id)

        articles = get_existing_section_headlines(section_orm)[:70]
        # articles.reverse()

        random.shuffle(articles)

        all_headline_elements = []

        for article in articles:
            if len(all_headline_elements) == 10:
                break

            title = article['title']
            subtitle = article['body']
            image_url = article.get('image_url')

            buttons = [
                Dialogue.button(
                    type='web_url', title='READ',
                    url=article['url']
                )
            ]

            section_data = Dialogue.generic(
                title=title, subtitle=subtitle,
                image_url=image_url,
                buttons=buttons
            )

            all_headline_elements.append(section_data)

        return all_headline_elements

    @classmethod
    def all_projects(cls, page=1, _tailored=False):
        briefs = get_reader_brief_sources()

        all_briefs_sources_elements = []

        for brief in briefs:
            if brief.brief_source_category == 'SECTION':
                title = brief.section.name
                image_url = get_section_thumbnail(title.lower())
            else:
                title = brief.news_source.title
                image_url = get_section_thumbnail(title.lower())

            description = None

            buttons = [
                Dialogue.button(
                    type='postback', title='DROP',
                    payload='DROP_BRIEF_SOURCE__%s' % brief.id
                )
            ]

            brief_source_data = Dialogue.generic(
                title=title.upper(), subtitle=description,
                image_url=image_url,
                buttons=buttons
            )

            all_briefs_sources_elements.append(brief_source_data)

        return all_briefs_sources_elements[:9]

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
        title = 'CREATE EVENT'
        subtitle = "Bring all the developers around your Blocs, under one roof"

        buttons = [
            Dialogue.button(
                type='web_url', title='YES',
                url=url_for('web_blueprint.render_event_creation_page',
                            user_id=g.user.id, _external=True)
            )
        ]

        section_data = Dialogue.generic(
            title=title, subtitle=subtitle,
            image_url=url_for(
                'web_blueprint.render_default_avatar', color='e4c847', _external=True),
            buttons=buttons
        )

        return [section_data]

    @classmethod
    def create_project(cls):
        title = 'CREATE PROJECT'
        subtitle = (
            "Take-on big projects with developers all over the world!\nYour "
            "project will be shared on your Blocs, as well as your "
            "Facebook & Instagram pages, to let more developers know about it!")

        buttons = [
            Dialogue.button(
                type='web_url', title='YES',
                url=url_for('web_blueprint.render_project_creation_page',
                            user_id=g.user.id, _external=True)
            )
        ]

        section_data = Dialogue.generic(
            title=title, subtitle=subtitle,
            image_url=url_for(
                'web_blueprint.render_default_avatar',
                color='e4c847', user_id=g.user.id, _external=True),
            buttons=buttons
        )

        return [section_data]

    @classmethod
    def create_job(cls):
        title = 'CREATE JOB'
        subtitle = (
            "Looking to hire someone?\nYour job offer will be shared on your "
            "Blocs, as well as your Facebook & Instagram pages, to help find "
            "more people!")

        buttons = [
            Dialogue.button(
                type='web_url', title='YES',
                url=url_for('web_blueprint.render_job_creation_page',
                            _external=True)
            )
        ]

        section_data = Dialogue.generic(
            title=title, subtitle=subtitle,
            image_url=url_for(
                'web_blueprint.render_default_avatar',
                color='e4c847', user_id=g.user.id, _external=True),
            buttons=buttons
        )

        return [section_data]

    @classmethod
    def create_course(cls):

        title = 'CREATE COURSE'
        subtitle = (
            "Gain respect & influence by passing on your awesome skills on "
            "Facebook!\nYour course will be shared on your Blocs, as well as "
            "your Facebook & Instagram pages, to let more developers know "
            "about it!")

        buttons = [
            Dialogue.button(
                type='web_url', title='YES',
                url=url_for('web_blueprint.render_course_creation_page',
                            user_id=g.user.id, _external=True)
            )
        ]

        section_data = Dialogue.generic(
            title=title, subtitle=subtitle,
            image_url=url_for(
                'web_blueprint.render_default_avatar',
                color='e4c847', user_id=g.user.id, _external=True),
            buttons=buttons
        )

        return [section_data]

    @classmethod
    def menu(cls):
        menu = []

        for name, description in MENU_ITEMS.iteritems():
            title = name.upper()
            subtitle = description

            buttons = [
                Dialogue.button(
                    type='web_url', title='YES',
                    url=url_for('web_blueprint.render_event_creation_page',
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

            menu.append(section_data)

        return menu
