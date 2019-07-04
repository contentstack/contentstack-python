"""
 * MIT License
 *
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

import logging

"""
    contentstack.error
    ~~~~~~~~~~~~~~~~~~
    This module implements the Error class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#error

"""

class HTTPError(Exception):

    errors_str = {

        'error_invalid_json': "Please provide valid JSON.",
        'error_message_stack_api_key_is_null': "Stack api key can not be null.",
        'error_form_name': "Please set contentType name.",
        'error_stack_access_token_is_null': "Access token can not be null.",
        'error_stack_environment_is_null': "Environment can not be null.",
        'Error_Connection_Error': "Connection error",
        'Error_Auth_Failure_Error': "Authentication Not present.",
        'Error_Parse_Error': "Parsing Error.",
        'Error_Server_Error': "Server interaction went wrong, Please try again.",
        'Error_Default': "Oops! Something went wrong. Please try again.",
        'Error_No_Network': "Network not available.",
        'Error_Called_Default_Method': "You must called Contentstack.stack() first",
        'Error_Query_Filter_Exception': "Please provide valid params."
    }


def __init__(self):
    errors = {

        400: "The request was incorrect or corrupted.",
        401: "The login credentials are invalid.",
        403: "The page or resource that is being accessed is forbidden.",
        404: "The requested page or resource could not be found.",
        412: "The entered API key is invalid.",
        422: "The request is syntactically correct but contains semantic errors",
        429: "The number of requests exceeds the allowed limit for the given time period.",
        500: "The server is malfunctioning and is not specific on what the problem is.",
        502: "A server received an invalid response from another server.",
        504: "A server did not receive a timely response from another server that it was accessing while attempting to load the web page or fill another request by the browser."
    }

    def get_error(self, response):
        print('Error')

    def set_logging_config(self, level):
        print('level ' + level)


class ConfigError(Exception):
    """Configuration Error Class"""
    pass


class StackException(Exception):
    """StackException Class"""
    pass


class NotSupportedException(Exception):
    """ exception is thrown when something is not supported by the API."""
    pass


class retry_request(object):
    """
    Decorator to retry function calls in case they raise rate limit exceptions
    """
