import calendar
import datetime
import os
import random
import uuid

from application.core.constants import (
    ALLOWED_CONFIGURATION_MODES, APP_COLORS, DEVELOPMENT_CONFIG_MODE)
from application.core.errors import ConfigNotFound


def detect_configuration_mode():
    config_mode = os.getenv('RUNNING_MODE', DEVELOPMENT_CONFIG_MODE)
    if config_mode in ALLOWED_CONFIGURATION_MODES:
        print('"%s" configuration mode detected.' % config_mode)
        return config_mode

    error_message = ('Invalid or no configuration mode ("{0}") detected! '
                     'Aborting...'.format(config_mode))
    raise ConfigNotFound(error_message)


def seconds_to_hours_and_mins_and_secs(seconds):
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return '{0} hour(s), {1} minute(s) and {2} second(s)'.format(
        hours, minutes, secs)


def parse_str_to_date(str):
    str_splitted = str.split('-')

    day = int(str_splitted[0])
    month = int(str_splitted[1])
    year = int(str_splitted[2])

    try:
        return datetime.date(year, month, day)
    except ValueError:
        raise ValueError


def parse_dict_to_datetime(params_date):
    """Convert a dictionary to a datetime object, if `params_date` is of a
    `dict`, if it's a `datetime`, return it back.

    :param params_date: the dict or datetime object
    :type params_date: dict, datetime
    :rtype: datetime or None
    """

    if isinstance(params_date, dict):
        day = int(params_date['day'])
        month = int(params_date['month'])
        year = int(params_date['year'])

        return datetime.datetime(year, month, day)

    elif isinstance(params_date, datetime.datetime):
        return params_date

    elif params_date is None:
        return

    else:
        raise TypeError(
            'params_date must be either a dict or datetime object')


def get_this_month_end():
    current_date = datetime.datetime.now()

    last_month_day = calendar.monthrange(
        current_date.year, current_date.month)[1]
    month = current_date.month
    year = current_date.year

    return datetime.date(year, month, last_month_day)


def generate_unique_reference():
    return uuid.uuid4().hex


def generate_random_bloc_color():
    return random.choice(list(APP_COLORS.values()))


def convert_to_possessive_noun(word):
    word = (
        "{}'".format(word) if word.endswith('s') else "{}'s".format(
            word)
    )

    return word


def get_typing_duration(reply_type, reply_context):
    if reply_type == 'text':
        return .4 + (len(reply_context) * .0425)

    return .75


# def current_request_time():
#     try:
#         return g.current_request_time
#     except AttributeError:
#         g.current_request_time = datetime.now()
#         return current_request_time()
#
#
# def current_user_id():
#     try:
#         return g.user.id
#     except AttributeError:
#         return None
#
#
# def current_api_log_id():
#     try:
#         return g.api_log.id
#     except AttributeError:
#         return None
#
#
# def current_api_ref():
#     try:
#         return g.api_log.api_ref
#     except AttributeError:
#         return None
