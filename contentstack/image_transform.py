"""
The Image Delivery API is used to retrieve, manipulate and/or convert image
files of your Contentstack account and deliver it to your web or mobile properties.
It is an second parameter in which we want to place different manipulation key and
value in array form ImageTransform method is define for image manipulation with
different transform_params in second parameter in array form
"""

# ************* Module image_transform **************
# Your code has been rated at 10.00/10  by pylint


class ImageTransform:
    """
    The Image Delivery API is used to retrieve, manipulate and/or convert image
    files
    """

    def __init__(self, http_instance, image_url, **kwargs):
        """
        :param httpInstance: instance of HttpsConnection
        :param image_url: url on which manipulation required, Image transformation url
        :param kwargs: parameter in which we want to place different
        manipulation key-worded, variable-length argument list
        ------------------------------
        Example::
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> stack.image_transform('image_url', width=100, height=100)
        ------------------------------
        """
        super().__init__()
        self.http_instance = http_instance
        self.image_url = image_url
        self.image_params = kwargs

    def get_url(self):
        """
        Returns a complete url after concatenate with parameters
        :return: updated asset url
        ------------------------------
        Example::
            >>> import contentstack
            >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
            >>> image_url = stack.image_transform('image_url', width=100, height=100)
            >>> result = image_url.fetch()
        ------------------------------
        """
        args = ['{0}={1}'.format(k, v) for k, v in self.image_params.items()]
        if args:
            self.image_url += '?{0}'.format('&'.join(args))
        return self.image_url


