# -*- coding: utf-8 -*-

# __init__.py
# Contentstack
# Created by Shailesh on 22/06/19.
# Copyright (c) 2012 - 2019 Contentstack. All rights reserved.

# [MIT License] :: Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# from .stack import Stack
from .entry import Entry
from .asset import Asset
from .asset_library import AssetLibrary
from .config import Config
from .query_result import QueryResult
from .content_type import ContentType
from .errors import HTTPError, ConfigError
from .group import Group
from .http_request import HTTPRequestConnection

__author__ = "Shailesh Mishra <mshaileshr@gmail.com>"
__status__ = "debug"
__date__ = "01 July 2019"
__version__ = "1.0.0"
__package__ = "contentstack.python"
__endpoint__ = "cdn.contentstack.io"

