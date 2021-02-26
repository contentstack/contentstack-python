import config
from twython import Twython, TwythonError
# create a keys object by passing the necessary secret passwords
keys = Twython(config.api_key, config.delivery_token, config.environment, config.host)
