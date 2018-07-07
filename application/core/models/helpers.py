import logging

from application.core.models import (Author, DisruptivPlatform,
    DisruptivPlatformCategory, NewsSource, Reader, Section,
    SocialMediaAccount)


def orm_get_author_by_name(name):
    return Author.get(name=name)


def orm_get_disruptiv_platform_by_name(name):
    return DisruptivPlatform.get(name=name)


def orm_get_new_sources_by_category(category):
    return NewsSource.query.filter_by(category=category).all()


def orm_get_social_media_account_by_username(social_media_name,
                                             social_media_username):

    return SocialMediaAccount.query_for_active().filter_by(
        app_name=social_media_name,
        username=social_media_username).first()


def orm_get_reader_by_platform_user_id(disruptiv_platform_id, uid):
    return Reader.query.order_by(
        Reader.created_at.desc()
    ).filter_by(
        disruptiv_platform_id=disruptiv_platform_id,
        uid=uid
    ).first()


def orm_get_section_by_id(section_id):
    return Section.get(id=section_id)


def orm_get_news_sources():
    return NewsSource.get()
