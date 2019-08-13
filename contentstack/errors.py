"""
 * MIT License
 * Copyright (c) 2012 - 2019 Contentstack
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
"""


class Error:
    """
    contentstack.error
    ~~~~~~~~~~~~~~~~~~
    This module implements the Error class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#error
    """

    def __init__(self):
        self.__error_dict = {}
        self.__error_code = str
        self.__msg = str
        self.__cause_err = str

    def config(self, result: dict):

        if result is not None and len(result) > 0:
            self.__error_dict = result
            self.__error_code = self.__error_dict['error_code']
            self.__msg = self.__error_dict['error_message']
            self.__cause_err = self.__error_dict['errors']

        return self

    @property
    def error_code(self):
        """
        :return: error_code as int
        """
        return self.__error_code

    @property
    def error_message(self):
        """
        :return: error_message
        """
        return self.__msg

    @property
    def error(self):
        """
        :return: error dict
        """
        return self.__cause_err

    @property
    def error_info(self) -> dict:
        """
        :return: dict, error information
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
        504: "A server did not receive a timely response from another server that it was accessing while attempting "
             "to load the web page or fill another request by the browser. "
    }

    @staticmethod
    def logging_config(level):
        print('level ' + level)


class ConfigError(Exception):
    pass


class StackException(Exception):
    pass


class ContentstackError(Exception):
    pass


class NotSupportedException(Exception):
    pass
