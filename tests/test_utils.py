import unittest

from contentstack import Utils


class TestUtils(unittest.TestCase):

    # def setUp(self):
    #     self.api_key = credentials.keys['api_key']
    #     self.delivery_token = credentials.keys['delivery_token']
    #     self.environment = credentials.keys['environment']
    #     self.host = credentials.keys['host']
    #     self.stack = contentstack.Stack(self.api_key, self.delivery_token, self.environment, host=self.host)

    def test_01_config_logging(self):
        result = Utils.config_logging()
        self.assertEqual(None, result)

    def test_02_setup_logger(self):
        result = Utils.setup_logger()
        self.assertEqual(0, result.level)

    def test_03_log(self):
        result = Utils.log('print')
        self.assertEqual(None, result)

    def test_04_do_url_encode(self):
        result = Utils.do_url_encode({'key': 'value', 'contentstack': 'cms'})
        self.assertEqual('key=value&contentstack=cms', result)
