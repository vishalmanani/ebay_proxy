import os
import sys

# Below Environment should exist in os.
# If below listed env variables are not found, then an error is raised.
# No need of assert statement. Just make sure variable is in list below


self = sys.modules[__name__]
ENVIRON_VARIABLES = [
    'ENVIRON',
    'PRODUCTION',
    'DEV',
    'LOCAL',
    'DEBUG',
    'SLACK_SECRET_KEY',
    'TOKEN',
    'DOMAIN',
    'APP_ID',
    'DEV_ID',
    'CERT_ID',
    'EBAY',

]
for env in ENVIRON_VARIABLES:
    value = os.environ[env]

    if value.isdigit():
        value = int(value)
    setattr(self, env, value)