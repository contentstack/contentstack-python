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


"""
contentstack.entry
~~~~~~~~~~~~~~~~~~
This module implements the Entry class.
API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#entries
"""
from typing import List, Any

import contentstack


class Entry:

    def __init__(self, content_type_id: str = None):

        self.url = contentstack.config.Config().endpoint('entries')
        self.__content_type_id = content_type_id
        if self.__content_type_id is not None:
            self.url = '{}/{}/entries/'.format(self.url, self.__content_type_id)

        self.__local_params: dict = {}
        self.__stack_headers: dict = {}
        self.__only_dict: dict = {}
        self.__other_post_dict: dict = {}

        self.__uid_for_except: list = []
        self.__uid_for_only: list = []
        self.__except_dic: list = []
        self.__reference_list: list = []

        self.__result_json: dict = {}
        self.__entry_uid = str
        self.__tags = list
        self.__title = str
        self.__description = str
        self.__url = str
        self.__locale = str
        self.__created_at = str
        self.__created_by = str
        self.__updated_at = str
        self.__updated_by = str
        self.__version = str

    @property
    def headers(self):
        return self.__stack_headers

    @headers.setter
    def headers(self, local_headers: dict):
        if local_headers is not None:
            self.__stack_headers = local_headers.copy()

    @property
    def uid(self):
        return self.__entry_uid

    def set_uid(self, entry_uid):
        if entry_uid is not None and isinstance(entry_uid, str):
            self.__entry_uid = entry_uid

    def params(self, key: str, value):
        if key is not None and value is not None:
            if isinstance(key, str) and isinstance(value, str):
                self.__local_params[key] = value
        return self

    def version(self, version: str):
        if version is not None and isinstance(version, str):
            self.__local_params["version"] = version
        return self

    @property
    def locale(self):
        if 'locale' in self.__result_json:
            return self.__result_json['locale']
        else:
            return self.__locale

    @locale.setter
    def locale(self, locale_code: str):
        if locale_code is not None and isinstance(locale_code, str):
            self.__local_params["locale"] = locale_code

    def configure(self, model: dict):
        if model is not None and isinstance(model, dict):
            self.__result_json = model

            if self.__result_json is not None:
                if 'title' in self.__result_json:
                    self.__title = self.__result_json['title']
                if 'url' in self.__result_json:
                    self.__url = self.__result_json['url']
                if 'uid' in self.__result_json:
                    self.__entry_uid = self.__result_json['uid']
                if 'tags' in self.__result_json:
                    self.__tags = self.__result_json['tags']
                if 'created_by' in self.__result_json:
                    self.__created_by = self.__result_json['created_by']
                if 'created_at' in self.__result_json:
                    self.__created_at = self.__result_json['created_at']
                if 'updated_at' in self.__result_json:
                    self.__updated_at = self.__result_json['updated_at']
                if 'updated_by' in self.__result_json:
                    self.__updated_by = self.__result_json['updated_by']
                if 'locale' in self.__result_json:
                    self.__locale = self.__result_json['locale']
                if '_version' in self.__result_json:
                    self.__version = self.__result_json['_version']

        return self

    def set_header(self, key: str, value: str):
        if key is not None and value is not None:
            if isinstance(key, str) and isinstance(value, str):
                self.__stack_headers[key] = value
        return self

    def remove_header(self, key):
        """
        [Uses]: header = remove_header('key')
        :param key:
        :return Entry:
        """
        if key is not None and isinstance(key, str):
            if key in self.__stack_headers:
                self.__stack_headers.pop(key)
        return self

    @property
    def title(self):
        """ title = entry.get_title() """
        return self.__title

    @property
    def urls(self):
        """ [Uses]: url = entry.get_url() """
        return self.__url

    @property
    def tags(self):
        """
        [Uses]: tags = get_tags()
        """
        return self.__tags

    @property
    def content_type(self):

        """
         [Uses]: content_type = get_content_type()
        """
        return self.__content_type_id

    @property
    def uid(self):
        """ [Uses]: uid = get_uid() """
        return self.__entry_uid

    @property
    def to_json(self):
        if self.__result_json is not None:
            return self.__result_json

    def get(self, key: str):
        if self.__result_json is not None:
            if key is not None and isinstance(key, str):
                if key in self.__result_json:
                    return self.__result_json[key]
            else:
                return None

    def get_string(self, key):
        value = self.get(key)
        if isinstance(value, str):
            return value
        else:
            return None

    def get_boolean(self, key: str):
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

    def get_list(self, key):
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

    @property
    def created_at(self):
        """
        value of creation time of entry.
        [Uses] created_at = entry.get_created_at()
        :return: str
        """
        return self.__created_at

    @property
    def created_by(self):
        """
        Get uid who created this entry.
        created_by = entry.get_created_by()
        :return: str:
        """
        return self.__created_by

    @property
    def updated_at(self):
        """
        value of updating time of entry.
        [Uses] updated_at = entry.get_updated_at()
        :returns str:
        """
        return self.__updated_at

    @property
    def updated_by(self):
        """
        Get uid who updated this entry.
        [Uses]  updated_by = entry.get_updated_by()
        :return str:
        """
        return self.__updated_by

    def asset(self, key: str):
        """
        Get an asset from the entry
        [Uses]
        asset = entry.get_asset("key")
        :param field_uid as key:
        :return: asset
        """
        asset = contentstack.asset.Asset
        if key is not None:
            result = self.get_json(key)
            if result is not None and isinstance(result, dict):
                asset = asset.configure(result)
        return asset

    def get_assets(self, key: str) -> list:
        """
        Get an assets from the entry. This works with multiple true fields
        [Uses] assets = entry.get_assets("key")
        :param key: str key
        :return: list of Assets
        """
        assets: List[Any] = []
        if key is not None and isinstance(key, str):
            assetlist = self.get_list(key)
            if isinstance(assetlist, list):
                for assetobj in assetlist:
                    if isinstance(assetobj, dict):
                        assetmodel = self.asset.configure(assetobj)
                        assets.append(assetmodel)
        return assets

    def get_group(self, key: str):
        """
        Get a group from entry.
        [USES]: Group innerGroup = entry.getGroup("key")
        :param key: field_uid as key.
        :return: None
        """
        from contentstack import Group
        if key is not None and self.__result_json is not None:
            if key in self.__result_json:
                extract_json = self.__result_json[key]
                if isinstance(extract_json, dict):
                    return Group(extract_json)
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
        if key is not None and self.__result_json is not None:
            group_list = []
            if key in self.__result_json:
                groups = self.__result_json[key]
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
        from contentstack import ContentType

        if self.__result_json is not None and isinstance(self.__result_json[ref_key], list):
            list_of_entries: list = self.__result_json[ref_key]
            for entry in list_of_entries:
                if ref_content_type is not None:
                    entry_instance = ContentType(ref_content_type).entry()

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

        import requests
        from urllib import parse
        from requests import Response
        import contentstack
        error = None

        self.__stack_headers["X-User-Agent"] = contentstack.__package__ + '-' + contentstack.__version__
        content_agent = 'application/json - ' + self.__user_agent
        self.__stack_headers["Content-Type"] = content_agent

        if self.__entry_uid is not None:
            self.url = '{0}{1}'.format(self.url, self.__entry_uid)

        if len(self.__stack_headers) > 0 and 'environment' in self.__stack_headers:
            self.__local_params['environment'] = self.__stack_headers['environment']

        payload = parse.urlencode(query=self.__local_params, encoding='UTF-8')
        response: Response = requests.get(self.url, params=payload, headers=self.__stack_headers)
        if response.ok:

            response = response.json()
            if error is None:
                response = response['entry']
                self.configure(response)
        else:
            error = response.json()

        return response, error

    @property
    def __user_agent(self):

        import contentstack
        import platform
        """
        Contentstack-User-Agent header.
        """
        header = {'sdk': {
            'name': contentstack.__package__,
            'version': contentstack.__version__
        }}
        os_name = platform.system()
        if os_name == 'Darwin':
            os_name = 'macOS'
        elif not os_name or os_name == 'Java':
            os_name = None
        elif os_name and os_name not in ['macOS', 'Windows']:
            os_name = 'Linux'
        header['os'] = {
            'name': os_name,
            'version': platform.release()
        }

        return header.__str__()
