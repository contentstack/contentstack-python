r"""This call fetches the list of all the assets of a particular stack.
It also returns the content of each asset in JSON format.
You can also specify the environment of which you wish to get the assets.
"""

# ************* Module assetquery **************
# Your code has been rated at 10/10 by pylint

import json
import logging

from contentstack.basequery import BaseQuery
from contentstack.utility import Utils

log = logging.getLogger(__name__)


class AssetQuery(BaseQuery):
    """
    This call fetches the list of all the assets of a particular stack.
    """

    def __init__(self, http_instance):
        super().__init__()
        self.http_instance = http_instance
        self.asset_query_params = {}
        self.base_url = "{}/assets".format(self.http_instance.endpoint)
        if "environment" in self.http_instance.headers:
            env = self.http_instance.headers["environment"]
            self.base_url = "{}?{}".format(self.base_url, "environment={}".format(env))

    def environment(self, environment):
        r"""Provide the name of the environment if you wish to retrieve the assets published
        in a particular environment.
        :param environment: environment of the stack
        :return: AssetQuery - so we can chain the call

        -----------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().environment('production').find()
        ------------------------------
        """
        if isinstance(environment, str):
            self.http_instance.headers['environment'] = environment
        return self

    def version(self, version):
        r"""Specify the version number of the asset that you wish to retrieve.
        If the version is not specified, the details of the latest version will be retrieved.
        To retrieve a specific version, keep the environment parameter blank.
        :param version: version number of the asset that you wish to retrieve
        :return: AssetQuery: so we can chain the call

        -----------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().version(3).find()
        ------------------------------
        """
        self.asset_query_params["version"] = version
        return self

    def include_dimension(self):
        r"""Include the dimensions (height and width) of the image in the response.
        Supported image types: JPG, GIF, PNG, WebP, BMP, TIFF, SVG, and PSD

        :return: AssetQuery: so we can chain the call

        -----------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().include_dimension().find()
        ------------------------------
        """
        self.asset_query_params["include_dimension"] = "true"
        return self

    def relative_url(self):
        r"""include the relative URLs of the assets in the response.

        :return: AssetQuery: so we can chain the call

        -----------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().relative_url().find()
        ------------------------------
        """
        self.asset_query_params["relative_urls"] = "true"
        return self

    def include_fallback(self):
        """Retrieve the published content of the fallback locale if an
        entry is not localized in specified locale.

        :return: AssetQuery, so we can chain the call

        ----------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().include_fallback().find()
        ----------------------------
        """
        self.asset_query_params['include_fallback'] = 'true'
        return self

    def locale(self, locale: str):
        """Enter locale code. e.g., en-us
        This retrieves published entries of specific locale..

        :return: AssetQuery, so we can chain the call

        ----------------------------
        Example::

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().locale('en-us').find()
        ----------------------------
        """
        self.asset_query_params['locale'] = locale
        return self

    def find(self):
        r"""This call fetches the list of all the assets of a particular stack.
        It also returns the content of each asset in JSON format.
        Learn more about Assets
        [https://www.contentstack.com/docs/content-managers/work-with-assets].

        :return: json result, List of asset object

        -----------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().find()

        """
        if self.parameters is not None and len(self.parameters) > 0:
            self.asset_query_params["query"] = json.dumps(self.parameters)
        url = Utils.get_complete_url(self.base_url, self.asset_query_params)
        return self.http_instance.get(url)
