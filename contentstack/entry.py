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


from contentstack import http_request, stack, group, Asset

"""
contentstack.entry
~~~~~~~~~~~~~~~~~~
This module implements the Entry class.
API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#entries
"""


class Entry(stack.Stack):

    def __init__(self, content_type_id, entry_uid=None):

        self.asset = Asset()

        self._uid = entry_uid
        self._content_type_id = content_type_id
        self._entry_url = str
        self._local_params: dict = {}
        self._stack_headers: dict = {}

        self.__uid_for_except: list = []
        self.__uid_for_only: list = []
        self.__only_dict: dict = {}
        self.__except_dic: list = []
        self.__other_post_dict: list = {}
        self.__reference_list: list = []

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

    def set_content_type_instance(self, entry_url_path: str, stack_headers: dict):
        if entry_url_path is not None and stack_headers is not None:
            if isinstance(entry_url_path, str) and isinstance(stack_headers, dict):
                self._entry_url = entry_url_path
                for key, value in stack_headers:
                    self._stack_headers[key] = value
                self._stack_headers = stack_headers
        return self

    def set_headers(self, local_header: dict):
        if local_header is not None and isinstance(local_header, dict):
            for key, value in local_header:
                self._stack_headers[key] = value
        return self

    def set_entry_uid(self, entry_uid: str):
        if entry_uid is not None and isinstance(entry_uid, str):
            self._uid = entry_uid
        return self

    def add_params(self, key: str, value):
        if key is not None and value is not None:
            if isinstance(key, str) and isinstance(value, str):
                self._local_params[key] = value
        return self

    def set_version(self, version: str):
        if version is not None and isinstance(version, str):
            self._local_params["version"] = version
        return self

    def set_locale(self, locale_code):
        if locale_code is not None and isinstance(locale_code, str):
            self._local_params["locale"] = locale_code
        return self

    def configure(self, model: dict):
        if model is not None and isinstance(model, dict):
            self._result_json = model

            if self._result_json is not None:

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
        """ [Uses]: header = set_header('key', 'value') """
        if key is not None and value is not None:
            if isinstance(key, str) and isinstance(value, str):
                self._stack_headers[key] = value

        return self

    def remove_header(self, key):
        """
        [Uses]: header = remove_header('key')
        :param key:
        :return Entry:
        """
        if key is not None and isinstance(key, str):
            if key in self._stack_headers:
                self._stack_headers.pop(key)
        return self

    def get_title(self):
        """ title = entry.get_title() """
        return self._title

    def get_url(self):
        """ [Uses]: url = entry.get_url() """
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
        if isinstance(value, str):
            return value
        else:
            return None

    def get_boolean(self, key):
        value = self.get(key)
        if isinstance(value, bool):
            return value
        else:
            return None

    def get_json(self, key):
        value = self.get(key)
        if isinstance(value, dict):
            return value
        else:
            return None

    def get_json_list(self, key):
        value = self.get(key)
        if isinstance(value, list):
            return value
        else:
            return None

    def get_int(self, key):
        value = self.get(key)
        if isinstance(value, int):
            return value
        else:
            return None

    def get_float(self, key):
        value = self.get(key)
        if isinstance(value, float):
            return value
        else:
            return None


    def get_created_at(self):
        """
        value of creation time of entry.
        [Uses] created_at = entry.get_created_at()
        :return: str
        """
        return self._created_at

    def get_created_by(self):
        """
        Get uid who created this entry.
        created_by = entry.get_created_by()
        :return: str:
        """
        return self._created_by

    def get_updated_at(self):
        """
        value of updating time of entry.
        [Uses] updated_at = entry.get_updated_at()
        :returns str:
        """
        return self._updated_at

    def get_updated_by(self):
        """
        Get uid who updated this entry.
        [Uses]  updated_by = entry.get_updated_by()
        :return str:
        """
        return self._updated_by

    def get_asset(self, key: str):
        """
        Get an asset from the entry
        [Uses]
        asset = entry.get_asset("key")
        :param field_uid as key:
        :return: asset
        """
        if key is not None:
            asset_response = self.get_json(key)
            if asset_response is not None and isinstance(asset_response, dict):
                self.asset = self.asset.configure(asset_response)
        return self.asset

    def get_assets(self, key: str) -> list:
        """
        Get an assets from the entry. This works with multiple true fields
        [Uses] assets = entry.get_assets("key")
        :param key: str key
        :return: list of Assets
        """
        assets = []
        if key is not None and isinstance(key, str):
            assets_list = self.get_json_list(key)
            if isinstance(assets_list, list):
                for asset in assets_list:
                    if isinstance(asset, dict):
                        self.asset = self.asset.configure(asset)
                        assets.append(self.asset)
        return assets

    def get_group(self, key: str):
        """
        Get a group from entry.
        [USES]: Group innerGroup = entry.getGroup("key")
        :param key: field_uid as key.
        :return: None
        """
        if key is not None and self._result_json is not None:
            if key in self._result_json:
                extract_json = self._result_json[key]
                if isinstance(extract_json, dict):
                    return group.Group(extract_json)
        else:
            return None

    def get_groups(self, key):
        """
        Get a list of group from entry.
        This will work when group is multiple true.
        :param key field_uid as key.
        :return  list of group from entry
        [Uses]: Group inner_group = entry.get_groups("key")
        """
        if key is not None and self._result_json is not None:
            group_list = []
            if key in self._result_json:
                groups = self._result_json[key]
                if isinstance(groups, list):
                    for single_group in groups:
                        group_list.append(single_group)
                    return group_list

    # [INCOMPLETE]
    def get_all_entries(self, ref_key: str, ref_content_type: str):
        """
        :param ref_key: key of a reference field.
        :param ref_content_type: class uid.
        :return: list of  @Entry instances. Also specified contentType value will be set as class uid for all  :Entry instance.
        #'blt5d4sample2633b' is a dummy Stack API key
        #'blt6d0240b5sample254090d' is dummy access token.

        Uses:

        # stack = contentstack.Stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        # cs_query = stack.contentType("content_type_uid").query()
        # cs_query.include_reference("for_bug")
        # (resp, err) = csQuery.find()
        # if err is None:
        # list_query = cs_query.get_dict()
        # for entry in list_query:
        #      task_entry = entry.get_all_entries("for_task", "task")


        """
        if self._result_json is not None and isinstance(self._result_json[ref_key], list):
            list_of_entries: list = self._result_json[ref_key]
            for entry in list_of_entries:
                if ref_content_type is not None:
                    entry_instance = stack.content_type.ContentType(ref_content_type).entry()

    def except_field_uid(self, field_uid: list):
        """
        Specifies list of field uids that would be &#39excluded&#39 from the response.
        //'blt5d4sample2633b' is a dummy Stack API key
        //'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        entry = stack.content_type.ContentType("content_type_uid").entry("entry_uid")
        entry.except(["name", "description"])
        :param field_uid: field uid  which get &#39excluded&#39 from the response.
        :return: entry object, so you can chain this call
        """
        if field_uid is not None and len(field_uid) > 0:
            for uid in field_uid:
                self.__uid_for_except.append(uid)
        return self

    def include_reference(self, *reference_fields):
        """
        Add a constraint that requires a particular reference key details.
        //'blt5d4sample2633b' is a dummy Stack API key
        //'blt6d0240b5sample254090d' is dummy access token.
        [Uses]
        stack = contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        entry = stack.contentType("content_type_uid").entry("entry_uid")
        entry.includeReference("referenceUid")
        :param reference_fields: list of reference_field key that to be constrained.
        :return: entry object, so you can chain this call.
        """
        # if reference_field is not None:
        #    self.__reference_list.append(reference_field)
        #    self.__other_post_dict["include[]"] = self.__reference_list
        if reference_fields is not None:
            for field in reference_fields:
                self.__reference_list.append(field)
            self.__other_post_dict["include[]"] = self.__reference_list
        pass

    def only(self, field_uid: list):
        """
        # Specifies an array of &#39;only&#39; keys in BASE object that would be &#39;included&#39; in the response.
        # 'blt5d4sample2633b' is a dummy Stack API key
        # 'blt6d0240b5sample254090d' is dummy access token.

        [USES]
        # stack = contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        # entry = stack.contentType("content_type_uid").entry("entry_uid")
        # entry.only(["name", "description"])
        # :param field_uid: list  of the &#39;only&#39; reference keys to be included in response.
        # :return: Entry object, so you can chain this call.
        """
        if field_uid is not None and len(field_uid) > 0:
            for field in field_uid:
                self.__uid_for_only.append(field)
            return self

    def only_with_reference_uid(self, field_uid: list, reference_field_uid: str):
        """
        :param field_uid: list of the &#39;only&#39; reference keys to be included in response.
        :param reference_field_uid: Key who has reference to some other class object..
        :return: Entry object, so you can chain this call.

        Uses:
        //'blt5d4sample2633b' is a dummy Stack API key
        //'blt6d0240b5sample254090d' is dummy access token.
        stack = contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        entry = stack.content_type.ContentType("content_type_uid").entry("entry_uid")
        array.append("description")
        array.append("name")
        entry.only_with_reference_uid(array, "reference_uid")
        """
        if field_uid is not None and reference_field_uid is not None:
            field_value_list: list = []
            for field in field_uid:
                field_value_list.append(field)
            self.__only_dict[reference_field_uid] = field_value_list
            self.include_reference(reference_field_uid)

    def except_with_reference_uid(self, field_uid: list, reference_field_uid: str):
        """
        :param field_uid: field_uid list of the &#39;except&#39; reference keys to be excluded in response.
        :param reference_field_uid: Key who has reference to some other class object.
        :return: Entry object, so you can chain this call.

        Uses:

        stack = contentstack.stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag");
        entry = stack.contentType("content_type_uid").entry("entry_uid")
        array.append("description")
        array.append("name")
        entry.except_with_reference_uid(array, "reference_uid");
        """
        if field_uid is not None and reference_field_uid is not None:
            field_value_list: list = []
            for field in field_uid:
                field_value_list.append(field)
            self.__uid_for_except[reference_field_uid] = field_value_list
            self.include_reference(reference_field_uid)

    def set_include_dict(self, main_dict: dict):

        for key, value in self.__other_post_dict:
            main_dict[key] = value
        if self.__uid_for_only is not None and len(self.__uid_for_only) > 0:
            main_dict["only[BASE][]"] = self.__uid_for_only
            self.__uid_for_only = None
        if self.__uid_for_except is not None and len(self.__uid_for_except) > 0:
            main_dict["except[BASE][]"] = self.__uid_for_except
            self.__uid_for_except = None
        if self.__except_dic is not None and len(self.__except_dic) > 0:
            main_dict["except"] = self.__except_dic
            self.__except_dic = None
        if self.__only_dict is not None and len(self.__only_dict) > 0:
            main_dict["only"] = self.__only_dict
            self.__only_dict = None

    def fetch(self) -> tuple:
        https_request = http_request.HTTPRequestConnection(self._entry_url, self._local_params, self._stack_headers)
        (response, error) = https_request.http_request()
        if error is None:
            result = response['entry']
            self.configure(result)
        return response, error
