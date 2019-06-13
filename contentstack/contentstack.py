
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

import config
import logging
import stack
from contentstack import stack


class Contentstack(object):

    def stack(self, api_key, access_token, environment, config):
        logging.info("Initicalised with configs")
        
        if api_key is None:
            logging.error("API Key can not be empty")
            raise AssertionError("API Key can not be empty")
        
        if access_token is None:
            logging.error("Access Token can not be empty")
            raise AssertionError("Access Token can not be empty")
        
        if environment is None:
            logging.error("Environment can not be empty")
            raise AssertionError("Environment can not be empty")
        
        if config is None:
            logging.error("congig can not be empty")
            raise AssertionError("Environment can not be empty")
        
        else:
            logging.info("stack initialisation attempted with config")
            return_stack = stack(api_key, access_token, environment)
            return return_stack






