"""
This call fetches the list of all the assets of a particular stack.
It also returns the content of each asset in JSON format.
You can also specify the environment of which you wish to get the assets.
"""

# ************* Module assetquery **************
# Your code has been rated at 10/10 by pylint

from urllib import parse


class AssetQuery:
    """
    This call fetches the list of all the assets of a particular stack.
    """

    def __init__(self, http_instance):
        self.http_instance = http_instance
        self.__query_params = {}
        self.base_url = '{}/assets'.format(self.http_instance.endpoint)
        if 'environment' in self.http_instance.headers:
            self.__query_params['environment'] = self.http_instance.headers['environment']
            # self.http_instance.headers.pop('environment')

    def environment(self, environment):
        """
        Provide the name of the environment if you wish to retrieve the assets published
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
        self.__query_params['environment'] = environment
        return self

    def version(self, version):
        """
        Specify the version number of the asset that you wish to retrieve.
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
        self.__query_params['version'] = version
        return self

    def include_dimension(self):
        """
        include the dimensions (height and width) of the image in the response.
        Supported image types: JPG, GIF, PNG, WebP, BMP, TIFF, SVG, and PSD
        :return: AssetQuery: so we can chain the call

        -----------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().include_dimension().find()
        ------------------------------
        """
        self.__query_params['include_dimension'] = 'true'
        return self

    def relative_url(self):
        """
        include the relative URLs of the assets in the response.
        :return: AssetQuery: so we can chain the call

        -----------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().relative_url().find()
        ------------------------------
        """
        self.__query_params['relative_urls'] = 'true'
        return self

    def include_count(self):
        """
        include count provides asset count
        :return: AssetQuery: so we can chain the call

        -----------------------------
        [Example]:

            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> result = stack.asset_query().include_count().find()
        ------------------------------
        """
        self.__query_params['include_count'] = 'true'
        return self

    def find(self):
        """
        This call fetches the list of all the assets of a particular stack.
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
        url = '{}?{}'.format(self.base_url, parse.urlencode(self.__query_params))
        return self.http_instance.get(url)
