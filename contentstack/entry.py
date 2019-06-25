# -*- coding: utf-8 -*-

# Entry.py
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

from contentstack import http_request
import datetime


class Entry(object):

    def __init__(self, content_type_id, entry_uid=None):

        self._uid = entry_uid
        self._content_type_id = content_type_id
        self._entry_url_path = str
        self._local_params: dict = {}
        self._stack_headers: dict = {}

        self._result_json = dict
        self._uid = str
        self._tags = list
        self._title = str
        self._description = str
        self._url = str
        self._locale = str
        self._created_at = str
        self._created_by = str
        self._updated_at = str
        self._updated_by = str
        self._version = str

    def set_content_type_instance(self, entry_url_path: str, stack_headers):
        self._entry_url_path = entry_url_path
        self._stack_headers = stack_headers
        print(self._entry_url_path)
        return self

    def set_headers(self, local_header: str):
        self._stack_headers = local_header
        return self

    def set_entry_uid(self, entry_uid: str):
        if entry_uid is not None:
            self._uid = entry_uid

    def add_params(self, key: str, value):
        self._local_params[key] = value
        return self

    def set_version(self, version: str):
        self._local_params["version"] = version
        return self

    def set_locale(self, locale_code):
        self._local_params["locale"] = locale_code
        return self

    def fetch(self) -> dict:
        print('single_entry_url_endpoint', self._entry_url_path)
        https_request = http_request.\
            HTTPRequestConnection(self._entry_url_path, self._local_params, self._stack_headers)
        result = https_request.http_request()
        if type(result) == dict:
            self.__configure(result)
        return result

    def __configure(self, model: dict):
        self._result_json = model
        self._title = self._result_json['title']
        self._url = self._result_json['url']
        self._uid = self._result_json['uid']
        self._tags = self._result_json['tags']
        self._created_by = self._result_json['created_by']
        self._created_at = self._result_json['created_at']
        self._updated_at = self._result_json['updated_at']
        self._updated_by = self._result_json['updated_by']
        self._locale = self._result_json['locale']
        self._version = self._result_json['_version']
        return self

    def set_header(self, key, value):
        """
        [Uses]: header = set_header('key', 'value')
        """
        if key is not None and value is not None:
            self._stack_headers[key] = value

    def remove_header(self, key):
        """
        [Uses]: header = remove_header('key')
        """
        if key in self._stack_headers:
            self._stack_headers.pop(key)

    def get_title(self):

        """
        [Uses]: title = get_title()
        """
        return self._title

    def get_url(self):

        """
        [Uses]: url = get_url()
        """
        return self._url

    def get_tags(self):
        """
        [Uses]: tags = get_tags()
        """
        return self._tags

    def get_content_type(self):
        """
         [Uses]: content_type = get_content_type()
        """
        return self._content_type_id

    def get_uid(self):
        """ [Uses]: uid = get_uid() """
        return self._uid

    def get_locale(self):
        if 'locale' in self._result_json:
            return self._result_json['locale']
        else:
            return self._locale

    def to_json(self):
        if self._result_json is not None:
            return self._result_json

    def get(self, key: str):
        if self._result_json is not None and key is not None:
            if key in self._result_json:
                return self._result_json[key]
            else:
                return None

    def get_string(self, key):
        value = self.get(key)
        if value is not None and type(value) == str:
            return value
        else:
            return None

    def get_boolean(self, key):
        value = self.get(key)
        if value is not None and type(value) == bool:
            return value
        else:
            return None

    def get_json(self, key):
        value = self.get(key)
        if value is not None and type(value) == dict:
            return value
        else:
            return None

    def get_int(self, key):
        value = self.get(key)
        if value is not None and type(value) == int:
            return value
        else:
            return None

    def get_float(self, key):
        value = self.get(key)
        if value is not None and type(value) == float:
            return value
        else:
            return None

    def get_date(self, key):
        value = self.get(key)
        if value is not None and type(value) == datetime.date:
            return value
        else:
            return None

        # def parse_date(self, raw_date, timezone=None):
        # x = datetime.datetime(2018, 6, 1)
        # return ''

    def get_created_at(self):
        return self._created_at

    def get_created_by(self):
        return self._created_by

    def get_updated_at(self):
        return self._updated_at

    def get_updated_by(self):
        return self._updated_by

    def get_asset(self, key: str):
        asset_object: dict = self.get_json(key)

    def get_assets(self, key):
        pass

    def get_group(self, key):
        pass

    def get_groups(self, key):
        pass

    def get_all_entries(self, ref_key, ref_content_type):
        pass

    def excepts(self, field_uid):
        pass

    def include_reference(self, reference_field=None, *reference_fields):
        pass

    def only(self, *field_uid):
        pass

    def only_with_reference_uid(self):
        pass

    def except_with_reference_uid(sel):
        pass
