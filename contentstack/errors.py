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


class HTTPError(Exception):

    """
    contentstack.error
    ~~~~~~~~~~~~~~~~~~
    This module implements the Error class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#error
    """

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

    error_code = {

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

    exceptions = {

        AssertionError: "Raised when the assert statement fails.",
        AttributeError: "Raised on the attribute assignment or reference fails.",
        EOFError: "Raised when the input() function hits the end-of-file condition.",
        FloatingPointError: "Raised when a floating point operation fails.",
        GeneratorExit: "Raised when a generator's close() method is called.",
        ImportError: "Raised when the imported module is not found.",
        IndexError: "Raised when the index of a sequence is out of range.",
        KeyError: "Raised when a key is not found in a dictionary.",
        KeyboardInterrupt: "Raised when the user hits the interrupt key (Ctrl+c or delete).",
        MemoryError: "Raised when an operation runs out of memory.",
        NameError: "Raised when a variable is not found in the local or global scope.",
        NotImplementedError: "Raised by abstract methods.",
        OSError: "Raised when a system operation causes a system-related error.",
        OverflowError: "Raised when the result of an arithmetic operation is too large to be represented.",
        ReferenceError: "Raised when a weak reference proxy is used to access a garbage collected referent.",
        RuntimeError: "Raised when an error does not fall under any other category.",
        StopIteration: "Raised by the next() function to indicate that there is no further item to be returned by the iterator.",
        SyntaxError: "Raised by the parser when a syntax error is encountered.",
        IndentationError: "Raised when there is an incorrect indentation.",
        TabError: "Raised when the indentation consists of inconsistent tabs and spaces.",
        SystemError: "Raised when the interpreter detects internal error.",
        SystemExit: "Raised by the sys.exit() function.",
        TypeError: "Raised when a function or operation is applied to an object of an incorrect type.",
        UnboundLocalError: "Raised when a reference is made to a local variable in a function or method, but no value has been bound to that variable.",
        UnicodeError: "Raised when a Unicode-related encoding or decoding error occurs.",
        UnicodeEncodeError: "Raised when a Unicode-related error occurs during encoding.",
        UnicodeDecodeError: "Raised when a Unicode-related error occurs during decoding.",
        UnicodeTranslateError: "Raised when a Unicode-related error occurs during translation.",
        ValueError: "Raised when a function gets an argument of correct type but improper value.",
        ZeroDivisionError: "Raised when the second operand of a division or module operation is zero."

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
