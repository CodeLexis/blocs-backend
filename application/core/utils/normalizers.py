from collections import OrderedDict

from application.core import errors, logger


def normalize_phone_number(phone_num, silent=False):
    """Validate given `phone_num`.

    Check that the phone number format is valid.
    Try to format the phone number if possible to meet
    required format.
    In the end, return a valid phone number or raise an error.

    Valid format is: 234XXXXXXXXXX (comprising of 13 digits)
    """

    try:
        phone_num = (
            str(phone_num).strip('+').replace(' ', '').replace('-', '')
        )

        if not phone_num.isdigit():
            raise ValueError(
                'Invalid phone number: {0}'.format(repr(phone_num)))

        if len(phone_num) == 10 and not phone_num.startswith('0'):
            return '234' + phone_num
        elif len(phone_num) == 11 and phone_num.startswith('0'):
            return '234' + phone_num[1:]
        elif phone_num.startswith('234') and len(phone_num) == 13:
            return phone_num
        else:
            raise ValueError(
                'Invalid phone number: {0}'.format(repr(phone_num)))
    except (ValueError, AttributeError) as error:
        if not silent:
            logger.error(error.message, exc_info=True)
            raise errors.InvalidPhoneNumber

        # Warn instead of indicating an error
        logger.warn(error.message, exc_info=True)


def normalize_ip(ip):
    # strip IP of any leading or trailing space(s)
    return getattr(ip, 'strip', lambda: None)()


def _normalize_dict(dict_):
    for k, v in dict_.iteritems():
        if v == 'None':
            dict_[k] = None
        elif isinstance(v, dict):
            dict_[k] = _normalize_dict(v)
    return OrderedDict(dict_)


def normalize_json_data(response_data):

    if isinstance(response_data, list):
        return map(normalize_request_data, response_data)

    if isinstance(response_data, dict):
        # recursively:
        #   - change all `'None'` values to `None`
        #   - make dict data ordered
        return _normalize_dict(response_data)

    return response_data


# def _normalize_imei_str(imei):
#     return imei.strip()


# def _normalize_imei_data(imei):
#     if isinstance(imei, basestring):
#         return _normalize_imei_str(imei) or None  # in case of empty string ''
#     return None  # any other data type is invalid


def normalize_request_data(request_data):
    request_data = request_data or {}

    # if 'imei' in request_data:
    #     request_data['imei'] = _normalize_imei_data(request_data['imei'])

    return request_data


# def normalize_sparkmeter_meter_number(meter_number):
#     return meter_number.upper()


def normalize_str_whitespaces(str_):
    if '  ' in str_:
        return ' '.join(str_.split()).strip()
    return str_.strip()


if __name__ == '__main__':

    def test_normalize_phone_number(phone_number, *args, **kwargs):
        result = normalize_phone_number(phone_number, *args, **kwargs)
        logger.debug('Result: ', result)

    # test_normalize_phone_number('23470113890641', True)
    # test_normalize_phone_number('2347011389064')
    test_normalize_phone_number(None)
