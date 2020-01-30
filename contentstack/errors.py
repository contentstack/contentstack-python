
"""

Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

contentstack.error
~~~~~~~~~~~~~~~~~~

API Reference: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#errors

"""


class Error:
    
    """
    This module implements the Error class.
    
    API Reference: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#errors

    """

    def __init__(self):

        self.__error_dict = {}
        self.__error_code = str
        self.__msg = str

    def _config(self, result):
        
        # _instance is the protected member of the asset, So outsiders can not access this file.
        if result is not None and len(result) > 0:
            self.__error_dict = result
            self.__error_code = self.__error_dict['error_code']
            self.__msg = self.__error_dict['error_message']

        return self

    @property
    def error_code(self):
        """It returns error code from the stack response
        
        Returns:
            int -- error_code as int
        
        ==============================
        
        [Example:]

        >>> error_code = error.error_code

        ==============================

        """
        return self.__error_code

    @property
    def error_message(self):

        """
        Returns error_message from the stack response

        Returns:
            str -- error_message from the stack response

        ==============================

        [Example:]

        >>> message = error.error_message

        ==============================
        """

        return self.__msg

    @property
    def error(self):

        """
        error property returns error code and error_message in dict formats

        Returns:
            dict -- error code and error_message in dict formats

        ==============================

        [Example:]

        >>> error = error.error

        ==============================
        """

        return self.__msg

    @property
    def error_info(self):

        """error information

        Returns:
            dict -- error information

        ==============================

        [Example:]

        >>> ode = error.error_info
        
        ==============================
        """
        return self.__error_dict

    errors_str = {

        'invalid_json': "Please provide valid JSON.",
        'api_key_is_none': "Stack api key can not be None.",
        'empty_content_type': "Please set contentType name.",
        'access_token_error': "Access token can not be None.",
        'environment_error': "Environment can not be None.",
        'connection_error': "Connection error",
        'auth_failure': "Authentication Not present.",
        'parse_error': "Parsing Error.",
        'server_error': "Server interaction went wrong, Please try again.",
        'error_default': "Oops! Something went wrong. Please try again.",
        'no_network': "Network not available.",
        'query_error': "Please provide valid params."
    }

    __error_code = {

        400: "The request was incorrect or corrupted.",
        401: "The login credentials are invalid.",
        403: "The page or resource that is being accessed is forbidden.",
        404: "The requested page or resource could not be found.",
        412: "The entered API key is invalid.",
        422: "The request is syntactically correct but contains semantic errors",
        429: "The number of requests exceeds the allowed limit for the given time period.",
        500: "The server is malfunctioning and is not specific on what the problem is.",
        502: "A server received an invalid response from another server.",
        504: """ A server did not receive a timely response from another server that it was accessing while attempting
             to load the web page or fill another request by the browser. """
    }


class StackException(Exception):
    """
    StackException used to handle Stack validation Errors.
    """
    pass


class RequestsWarning(Warning):
    """Base warning for Requests."""
    pass


class FileModeWarning(RequestsWarning, DeprecationWarning):
    """A file was opened in text mode, but Requests determined its binary length."""
    pass
