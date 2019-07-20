from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'creed_05',
        'display_name': "Creed game, 50% of catch",
        'num_demo_participants': 6,
        'app_sequence': ['creed'],
        'fine': 100,
        'prob_catch': 0.5,
        'use_browser_bots': False,
    },
    {
        'name': 'creed_075',
        'display_name': "Creed game, 75% of catch",
        'num_demo_participants': 6,
        'app_sequence': ['creed'],
        'fine': 100,
        'prob_catch': 0.75,
        'use_browser_bots': False,
    },

]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECU'

ROOMS = [{'name': 'hse', 'display_name': 'hse'}]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = ')in8jmri5&8s=hs0jqc+!$zmk9fw$6!d(_^ait^0pglyg#glxp'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
