import random

from flask import g, url_for

# from application.articles.helpers import (get_existing_section_headlines,
#                                           get_existing_news_source_headlines)
# from application.readers.helpers import get_reader_brief_sources
from application.core.constants import (
    DEFAULT_BLOCS, PAGINATE_DEFAULT_PER_PAGE)
from application.core.models import Bloc
# from application.core.utils import get_app_icon_url, get_section_thumbnail
from .dialogue import Dialogue


class Collections(object):
    @classmethod
    def all_blocs(cls, page=1):
        blocs = Bloc.paginate(
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

        if _location_id is not None:
            blocs = blocs.filter_by(location_id=_location_id)

        all_bloc_elements = []

        for bloc in blocs:
            if len(all_bloc_elements) == PAGINATE_DEFAULT_PER_PAGE:
                break

            title = bloc.name
            image_url = url_for(
                'web_blueprint.render_default_avatar',
                color=bloc.theme_color, _external=True)

            buttons = [
                Dialogue.button(
                    type='postback', title='JOIN',
                    payload='JOIN_BLOC'
                )
            ]

            bloc_data = Dialogue.generic(
                title=title, subtitle=None, image_url=image_url,
                buttons=buttons
            )

            all_bloc_elements.append(bloc_data)

        # APPEND BLOCS NOT TIED TO LOCATIONS
        if len(all_bloc_elements) < PAGINATE_DEFAULT_PER_PAGE:
            all_bloc_elements.extend(cls.all_default_blocs())

        all_bloc_elements = all_bloc_elements[:PAGINATE_DEFAULT_PER_PAGE]

        print('ALL DEFAULT BLOC ELEMENTS: {}'.format(all_bloc_elements))
        print('BLOCS: {}'.format(blocs))

        return all_bloc_elements

    @classmethod
    def all_courses(cls, page=1, _tailored=False):
        return

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
        all_section_elements = []

        for section in Section.query.paginate(per_page=10, page=page).items:

            title = section.name
            subtitle = ''  # section.description

            buttons = [
                Dialogue.button(
                    type='postback', title='VIEW',
                    payload='DISPLAY_SECTION__%s' % (section.id)
                )
            ]

            section_data = Dialogue.generic(
                title=title.upper(), subtitle=subtitle,
                image_url=get_section_thumbnail(title.lower()),
                buttons=buttons
            )

            all_section_elements.append(section_data)

        return all_section_elements

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
    def all_jobs(cls, page=1, _tailored=False):
        news_sources = NewsSource.query.order_by(
            NewsSource.id.desc()
        ).paginate(
            per_page=10, page=page
        ).items

        all_section_elements = []

        for source in news_sources:
            title = source.title
            subtitle = ''  # section.description

            buttons = [
                Dialogue.button(
                    type='postback', title='VIEW',
                    payload='DISPLAY_NEWS_SOURCE__%s' % (source.id)
                )
            ]

            section_data = Dialogue.generic(
                title=title.upper(), subtitle=subtitle,
                image_url=get_section_thumbnail(title.lower()),  # get_app_icon_url(),
                buttons=buttons
            )

            all_section_elements.append(section_data)

        return all_section_elements

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
