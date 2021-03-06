APP_COLORS = {
    'red': 'f45757',
    'yellow': 'e4c847',
    'blue': '57d5f4',
    'purple': '88a2f6',
    'pink': 'f378ac'
}

APP_OS = ['linux', 'windows', 'android']

ALLOWED_CONFIGURATION_MODES = ['development', 'production', 'test']
DEVELOPMENT_CONFIG_MODE = 'development'

FACEBOOK_APP_ID = '196700654526136'  # '443981506013508'
FACEBOOK_APP_SECRET = 'e7a2dc3e960bc53c4ae378d9e3761e43'
                      # 'fcf0d6153ac7cfcb5ab5eb7ec26f842c'
FACEBOOK_PAGE_ID = '271401833666830'  # '2112206745661442'
FACEBOOK_MESSENGER_URL = 'https://www.messenger.com/t'

'EAACy5fCj3rgBAP98hkUBZB2GCgecTnWfPz1b47b0SeLSq2QZAD8lvJxZCrnNlxrvuEQV3vVxqQ3CNER49BZCTlAlBvPMx6XX0f8K8cPGF9cQvXgJwboPLVwJPxOuMrZAAWl2AFaCSFJ2EROyhPEVxv0hfiZClqqy6bZC5ylpXfotAZDZD'

PAGINATE_DEFAULT_PER_PAGE = 8
PAYLOADABLE_HTTP_METHODS = ['put', 'delete', 'patch', 'post']
PROGRAMMING_LANGUAGES = [
    'C++', 'C#', 'Java', 'Perl', 'Python', 'JavaScript', 'PHP', 'CSS', 'HTML']
SALARY_INTERVALS = ['Hour', 'Day', 'Week', 'Month', 'Year']
SCHOOL_COURSE_CATEGORIES = [
    'Web', 'Functional Programming', 'Object Oriented Programming',
    'Networking', 'Electronics']
DEFAULT_BLOCS = SOFTWARE_BRANCHES = [
    'Mobile Application', 'Web Application', 'UI/UX Design', 'Data Science',
    'Embedded Systems', 'Security Software']
STATUSES = ('active', 'deleted')
SUPPORTED_HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
TIMEZONES = ['GMT', 'PST', 'CAT']

LANDING_MESSAGE = (
    'Facebook, tailored to suit the Developer.')
LANDING_MESSAGE_2 = ('Alternate version of Facebook, for the devs.')

MENU_ITEMS = {
    'Courses': (
        'Widen your tech-stack by taking courses taken by developers on '
        'Facebook.'),
    'Projects': (
        'Team-up and build projects with the best developers on Facebook.'),
    'Events': 'Find upcoming events within your Blocs',
    'Jobs': 'Job offers from people within your Blocs',
    'Feeds': "Fun stuff shared by other developers.",
    'News': 'Just news on technology pulled from the internet.'
}

PLATFORMS_URL = {
    'facebook-bot': '{}/{}'.format(FACEBOOK_MESSENGER_URL, FACEBOOK_PAGE_ID)
}
