r"""Assets refer to all the media files (images, videos, PDFs, audio files,
and so on) uploaded in your Contentstack repository for future use.

These files can be attached and used in multiple entries.
"""

# ************* Module asset **************
# Your code has been rated at 10/10 by pylint

import logging
from urllib import parse

log = logging.getLogger(__name__)


class Asset:
    r"""`Asset` refer to all the media files (images, videos, PDFs, audio files, and so on)."""

    def __init__(self, http_instance, uid=None):
        self.http_instance = http_instance
        self.asset_params = {}
        self.__uid = uid
        if self.__uid is None or self.__uid.strip() == 0:
            raise KeyError('Please provide valid uid')
        self.base_url = '{}/assets/{}'.format(self.http_instance.endpoint, self.__uid)
        if 'environment' in self.http_instance.headers:
            self.asset_params['environment'] = self.http_instance.headers['environment']

    def environment(self, environment):
        r"""Provide the name of the environment if you wish to retrieve the assets published
        in a particular environment.
        :param environment {str} - name of the environment
        :return: `Asset`, so we can chain the call
        -------------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> asset = stack.asset(uid='asset_uid')
            >>> asset = asset.environment('production')
        -------------------------------
        """
        if environment is not None or environment is str:
            self.http_instance.headers['environment'] = environment
        return self

    def remove_environment(self):
        r"""Removes environment from the request params
        :return: `Asset`, so we can chain the call
        -------------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> asset = stack.asset(uid='asset_uid')
            >>> asset = asset.remove_header()
            >>> asset.fetch()
        -------------------------------
        """
        if 'environment' in self.http_instance.headers:
            self.http_instance.headers.pop('environment')
        return self

    def params(self, key, value):
        r"""params is used to pass additional parameters to the asset query
        :param key: key of the query parameter
        :param value: value of the query parameter
        :return: `Asset`, so we can chain the call
        -----------------------------
        Example::
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> asset = stack.asset(uid='asset_uid')
            >>> asset = asset.params('key', 'value')
        -----------------------------
        """
        if None in (key, value) or not isinstance(key, str):
            raise KeyError('Kindly provide valid params')
        self.asset_params[key] = value
        return self

    def relative_urls(self):
        """Include the relative URLs of the assets in the response.
        :return: `Asset`, so we can chain the call
        ----------------------------
        Example::
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> asset = stack.asset(uid='asset_uid')
            >>> asset = asset.relative_urls()
        ----------------------------
        """
        self.asset_params['relative_urls'] = 'true'
        return self

    def include_dimension(self):
        r"""Include the dimensions (height and width) of the image in the response.
        Supported image types: JPG, GIF, PNG, WebP, BMP, TIFF, SVG, and PSD.
        :return: `Asset`, so we can chain the call
        ----------------------------
        Example::
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> asset = stack.asset(uid='asset_uid')
            >>> asset = asset.include_dimension()
        ----------------------------
        """
        self.asset_params['include_dimension'] = "true"
        return self

    def include_fallback(self):
        r"""Retrieve the published content of the fallback locale if an
        entry is not localized in specified locale
        :return: `Asset`, so we can chain the call
        ----------------------------
        Example::
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> asset = stack.asset(uid='asset_uid')
            >>> result = asset.include_fallback().fetch()
        ----------------------------
        """
        self.asset_params['include_fallback'] = "true"
        return self

    def fetch(self):
        r"""This call fetches the latest version of a specific asset of a particular stack.
        :return: json response of asset
        -----------------------------
        [Example]:
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> asset = stack.asset(uid='asset_uid')
            >>> result = asset.fetch()
        ------------------------------
        """
        url = '{}?{}'.format(self.base_url, parse.urlencode(self.asset_params))
        return self.http_instance.get(url)
