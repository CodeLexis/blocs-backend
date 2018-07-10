import random
import re

from flask import g

from application.core import errors
from application.core.constants import APP_COLORS, DEFAULT_BLOCS
from application.core.models import Bloc, BlocMembership, BlocTag, User
from application.core.models import prep_paginate_query, get_pagination_meta
from application.core.utils.helpers import (
    generate_random_bloc_color, convert_to_possessive_noun)


def _normalize_name(name):
    name = re.sub('[!@#$%^&*()-_+=:;,<.>?/"`|]', '', name)
    return name


def _check_for_existing_bloc_with_name(name):
    normalized_name = _normalize_name(name)

    return Bloc.get(name=normalized_name)


def get_blocs(name, tags):
    blocs = BlocTag.query.join(
        BlocTag.bloc
    ).prep_query_for_active().filter(
        Bloc.name.like(name), BlocTag.name.in_(tags)
    )

    return blocs


def get_blocs_for_location(location):
    Bloc.get(location=location)


def get_bloc_members(bloc_uid, page, per_page):
    bloc = Bloc.get(uid=bloc_uid)
    if bloc is None:
        raise errors.ResourceNotFound

    bloc_memberships = BlocMembership.query.filter_by(bloc_id=bloc.id)

    paginated_query = prep_paginate_query(
        bloc_memberships, page=page, per_page=per_page)
    meta = get_pagination_meta(paginated_query)

    return page.items, meta


def add_user_to_bloc(bloc_uid, user_uid):
    bloc = Bloc.get(uid=bloc_uid)
    if bloc is None:
        raise errors.ResourceNotFound

    user = User.get(uid=user_uid)
    if user is None:
        raise errors.ResourceNotFound

    bloc_membership = BlocMembership(bloc_id=bloc.id, user_id=user.id)

    bloc_membership.save()

    return bloc_membership


def create_bloc(name, is_private, color, location):
    existing_bloc = _check_for_existing_bloc_with_name(name)

    if existing_bloc:
        raise errors.ResourceConflict('Choose another name')

    bloc = Bloc(
        name=name,
        is_private=is_private,
        theme_color=color,
        created_by=g.user.id,
        locatio=location
    )

    if is_private:
        bloc.set_invite_code()

    bloc.save()

    return bloc


def create_default_blocs_for_location(location):
    for bloc_name in DEFAULT_BLOCS:
        create_bloc(
            name='{} {} Bloc'.format(
                convert_to_possessive_noun(location), bloc_name),
            location=location,
            is_private=False,
            color=generate_random_bloc_color
        )
