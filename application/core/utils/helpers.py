import calendar
import datetime
import decimal
import locale
import os
import uuid
from decimal import Decimal

from flask import current_app, g

from application.core import errors, logger, rand_gen
from application.core.constants import (ALLOWED_CONFIGURATION_MODES,
                                        DEVELOPMENT_CONFIG_MODE)
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


# def get_request_imeis():
#     request_imeis = g.request_data.get('imei')
#     if request_imeis:
#         request_imeis = [i.strip() for i in (request_imeis).split()]
#         return request_imeis[0], request_imeis[-1]
#     else:
#         return None


def ngn_str(amount, silent=False):
    locale.setlocale(locale.LC_ALL, 'en_NG')

    amount_invalid = (
        amount is None or
        (isinstance(amount, basestring) and len(amount.strip()) < 1)
    )
    if amount_invalid:
        return ''

    return locale.format('%.2f', float(amount), True)


def kobo_to_ngn(kobo_amt, silent=False):
    """Convert an amount in kobo to it's naira value

    :param kobo_amt: kobo value of amount to be converted
        as an integer type
    :param silent: flag to specify if errors should be propagated
    :return: converted amount as a `decimal.Decimal` type
    """
    try:
        with decimal.localcontext() as ctx:
            ctx.prec = 3  # Force Decimal values to 2 decimal places
            return Decimal('%.2f' % (int(kobo_amt) / 100.0))
    except Exception:
        err_msg = (
            'Could not convert Kobo ({0}) to naira!'.format(repr(kobo_amt))
        )
        if not silent:
            logger.error(err_msg, exc_info=True)
            raise errors.InvalidAmountError

        logger.warn(err_msg)


def generate_account_number(account_id):
    return str(int(current_app.config['RECEIPT_BASE']) + account_id)


def generate_unique_reference():
    return uuid.uuid4().hex
    # return str(rand_gen.getrandbits(128))[-20:]
    # return str(rand_gen.getrandbits(128))[-20:]
    # return shortuuid.uuid()


def generate_next_pay_ref():
    return g.api_ref


def clean_account_number(account_number):
    try:
        return account_number.strip('-+/ ').replace('-', '').replace(
            '+', '').replace('/', '').replace(' ', '')
    except AttributeError:
        logger.error(
            'Error cleaning up account number {0}'.format(account_number),
            exc_info=True)
        raise TypeError


def kobo_to_ngn_str(amount, silent=False):
    return ngn_str(kobo_to_ngn(amount, silent=silent))


def ngn_to_kobo(ngn_value):
    return int(ngn_value * 100)


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
