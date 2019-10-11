"""
Entry
contentstack
Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

"""

import os
import sys

sys.path.insert(0, os.path.abspath('.'))


class Entry:
    """
    contentstack.entry
    This Get a single entry request fetches a particular entry of a content type.
    ~~~~~~~~~~~~~~~~~~
    This module implements the Entry class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#entries

    [Note: If no version is mentioned, this request will retrieve the
    latest published version of the entry.
    To retrieve a specific version,
    make use of the version parameter and keep the environment parameter blank.]
    """

    def __init__(self, content_type_id=None):
        self.__content_type_id = content_type_id
        self.__stack_instance = None
        self.__http_request = None
        self.__config = None
        self.__entry_url = None

        self.__local_params = {}
        self.__entry_headers = {}
        self.__only_dict = {}
        self.__result_json = {}

        self.__uid_for_except = {}
        self.__except_field = []
        self.__uid_for_only = []
        self.__tags = []

        self.__entry_uid = str
        self.__title = str
        self.__description = str
        self.__url = str
        self.__locale = str
        self.__created_at = str
        self.__created_by = str
        self.__updated_at = str
        self.__updated_by = str
        self.__version = str
        self.__count = 0

    def _instance(self, stack_instance):
        # This is the protected from outside users, so they can't access this function.
        self.__stack_instance = stack_instance
        self.__config = self.__stack_instance.config
        self.__entry_url = self.__config.endpoint
        if self.__content_type_id is not None:
            self.__entry_url = '{}/content_types/{}/entries/'.format(self.__entry_url, self.__content_type_id)
        self.__http_request = self.__stack_instance.get_http_instance

        return self

    def _configure(self, model):
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

    def add_header(self, key, value):

        """
        It is useful to accept the API key, access_token of stack of which you wish to retrieve the content types.
        :param key: key of the header
        :type key: str
        :param value: value of respected key header
        :type value: str
        :return: self
        :rtype: Entry

        ==============================

        [Example:]

        >>> entry = entry.set_header('key', 'value')

        ==============================
        """

        if key and value is not None:
            if isinstance(key, str) and isinstance(value, str):
                self.__entry_headers[key] = value
            else:
                raise ValueError('Kindly provide str type key-value pair')
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    def remove_header(self, key):

        """
        This method is helpful to remove desired key from the header of the entry
        :param key: key of the entry header
        :type key: str
        :return: self
        :rtype: Entry

        ==============================

        [Example:]

        >>> header = remove_header('key')

        ==============================
        """

        if key is None:
            raise ValueError('Kindly provide valid KEY')
        elif isinstance(key, str):
            if key in self.__entry_headers:
                self.__entry_headers.pop(key, None)
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    @property
    def uid(self):

        """
        :return: uid of the entry of str type

        ==============================

        [Example:]

        >>> entry = entry.uid

        ==============================
        """
        return self.__entry_uid

    @property
    def locale(self):

        """
        It returns code of the language of which the entries needs to be included.
        :return: code of the language of which the entries needs to be included.
        :rtype: str

        ==============================

        [Example:]

        >>> entry = entry.locale

        ==============================
        """

        if 'locale' in self.__result_json:
            return self.__result_json['locale']
        else:
            return self.__locale

    @locale.setter
    def locale(self, locale):

        """
        locale accepts code of the language of which the entries needs to be included.
        Only the entries published in this locale will be displayed.
        :param locale: code of the language of which the entries needs to be included.
        :type locale: str
        :return: It does not return any value
        :rtype: Entry

        ==============================

        [Example:]

        >>> entry = entry.locale('en-us')

        ==============================
        """

        if locale is not None and isinstance(locale, str):
            self.__local_params["locale"] = locale
        else:
            raise ValueError('Kindly provide a valid locale')

    @property
    def title(self):

        """
        This method returns title of the entry
        :return: Title of the entry
        :rtype: str

        ==============================

        [Example:]
        
        >>> title = entry.title

        ==============================
        """
        return self.__title

    @property
    def url(self):

        """
        This method returns urls of the entry

        ==============================
        
        [Example:]
        
        >>> url = entry.url
        
        ==============================

        """

        return self.__url

    @property
    def tags(self):

        """
        This method returns list of tags of the entry
        :return: This method returns tags of the entry
        :rtype: list
        
        ==============================
        
        [Example:]
        
        >>> tags = entry.tags
        
        ==============================
        """

        return self.__tags

    @property
    def content_type(self):

        """
        This method returns content_type of the entry
        :return: content_type of the entry
        :rtype: str
        
        ==============================
        
        [Example:]
        
        >>> content_type = entry.content_type
        
        ==============================
        """

        return self.__content_type_id

    @property
    def headers(self):

        """
        This method is useful to get dictionary of the headers
        :return: The method is used to get list of headers.
        :rtype: dict

        ==============================

        [Example:]

        >>> entry = entry.headers

        ==============================
        """

        return self.__entry_headers

    @property
    def uid(self):

        """
        This method returns uid of the entry
        :return: uid of the entry
        :rtype: str
        
        ==============================
        
        [Example:]
        
        >>> uid = entry.uid
        
        ==============================
        """
        return self.__entry_uid

    @property
    def json(self):

        """
        This method returns response of the entry in dictionary formats
        :return: response of the entry in dictionary type
        :rtype: dict
        
        ==============================
        
        [Example:]
        
        >>> json_result = entry.json
        
        ==============================
        """

        if self.__result_json is None:
            return None
        else:
            return self.__result_json

    @property
    def count(self):

        """
        :return: count of the Entry Object
        
        ==============================
        
        [Example:]

        >>> result = entry.count
        
        ==============================
        """
        return self.__count

    @property
    def created_at(self):

        """
        value of creation time of entry.
        [Uses] created_at = entry.get_created_at()
        :return: str

        ==============================

        [Example:]

        >>> result = entry.created_at

        ==============================
        """

        return self.__created_at

    @property
    def created_by(self):

        """
        Get uid who created this entry.
        :return:  uid who created this entry.
        :rtype:str

        ==============================

        [Example:]

        >>> result = entry.get_created_by

        ==============================
        """

        return self.__created_by

    @property
    def updated_at(self):

        """
        value of updating time of entry.
        :return: updating time of entry.
        :rtype: str

        ==============================

        [Example:]

        >>> result = entry.get_updated_at

        ==============================
        """

        return self.__updated_at

    @property
    def updated_by(self):

        """
        Get uid who updated this entry.
        :return: uid who updated entry.
        :rtype: str

        ==============================

        [Example:]

        >>> result = entry.get_updated_by

        ==============================
        """

        return self.__updated_by

    @property
    def created_at(self):

        """
        value of creation time of entry.
        [Uses] created_at = entry.get_created_at()
        :return: str

        ==============================

        [Example:]

        >>> result = entry.created_at

        ==============================
        """

        return self.__created_at

    @property
    def created_by(self):

        """
        Get uid who created this entry.
        :return:  uid who created this entry.
        :rtype:str

        ==============================

        [Example:]

        >>> result = entry.get_created_by

        ==============================
        """

        return self.__created_by

    @property
    def updated_at(self):

        """
        value of updating time of entry.
        :return: updating time of entry.
        :rtype: str

        ==============================

        [Example:]

        >>> result = entry.get_updated_at

        ==============================
        """

        return self.__updated_at

    @property
    def updated_by(self):

        """
        Get uid who updated this entry.
        :return: uid who updated entry.
        :rtype: str

        ==============================

        [Example:]

        >>> result = entry.get_updated_by

        ==============================
        """

        return self.__updated_by

    def set_uid(self, uid):

        """
        the unique ID of the content type of which you wish to retrieve the details.
        The content type UID is generated based on the title of the content type and it is unique across a stack.
        :param uid: The unique ID of the content type of which you wish to retrieve the details
        :type uid: str
        :return: Entry

        ==============================

        [Example:]

        >>> entry = entry.set_uid('uidexamplesomethng')

        ==============================
        """

        if uid is None:
            raise ValueError('Kindly provide a valid entry_uid')
        elif isinstance(uid, str):
            self.__entry_uid = uid
        else:
            raise ValueError('entry_uid should be str type')

        return self

    def get(self, key):

        """
        This method returns value of respective key of the entry
        :param key: key you want to access value
        :type key: str
        :return: json
        :rtype: object

        ==============================

        [Example:]

        >>> result = entry.get('yourKey')

        ==============================
        """

        if key is None:
            raise ValueError('Kindly provide a valid argument')
        elif isinstance(key, str):
            if key in self.__result_json:
                return self.__result_json[key]

    def add_param(self, key, value):

        """
        This method is useful to add additional Query parameters to the entry
        :param key: query param key
        :type key: str
        :param value: query param value
        :type value: str
        :return: self
        :rtype: Entry

        ==============================

        [Example:]

        >>> entry = entry.params('key', 'value')

        ==============================
        """

        if None in (key, value):
            raise ValueError('Kindly provide valid KEY and Value arguments')
        elif isinstance(key, str):
            self.__local_params[key] = value
        else:
            raise ValueError('Params key should be str')

        return self

    def version(self, version):

        """
        Enter the version number of the entry that you want to retrieve. However,
        to retrieve a specific version of an entry, you need to keep the environment parameter blank.
        :param version: version of the entry
        :type version: str
        :return: self
        :rtype: Entry

        ==============================

        [Example:]

        >>> entry = entry.version('7')

        ==============================
        """

        if version is None:
            raise ValueError('Kindly provide valid')
        elif isinstance(version, str):
            self.__local_params["version"] = version
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    def get_string(self, key):

        """
        This method returns str type result of the entry
        :param key: key of the entry
        :type key: str
        :return: value from the dict of respective key
        :rtype: str
        
        ==============================
        
        [Example:]

        >>> result = entry.get_string('entry_key')
        
        ==============================
        """

        value = self.get(key)
        if isinstance(value, str):
            return value
        else:
            return None

    def get_boolean(self, key):

        """
        This method returns bool type result of the entry
        :param key: This is the key of the entry
        :type key: str
        :return: boolean value
        :rtype: bool
        
        ==============================
        
        [Example:]

        >>> result = entry.get_boolean('bool_key')
        
        ==============================
        """

        if isinstance(key, str):
            value = self.get(key)
            if isinstance(value, bool):
                return value
        else:
            raise KeyError('Kindly provide valid KEY')

    def get_json(self, key):

        """
        This method is useful to get result of respective key if result is dict
        :rtype: object
        :param key: This is the key of the entry
        
        ==============================
        
        [Example:]

        >>> result = entry.get_json('key')
        
        ==============================
        """

        value = self.get(key)
        if isinstance(value, dict):
            return value
        else:
            return None

    def get_list(self, key):

        """
        Gets list of data from the entry
        :param key: key of the entry to be accessed
        
        ==============================
        
        [Example:]

        >>> result = entry.get_list('key')
        
        ==============================
        """
        value = self.get(key)
        if isinstance(value, list):
            return value
        else:
            return None

    def asset(self, key):

        """

        Get an asset from the entry on the basis of the key
        :return: Asset of the entry
        :rtype: Asset

        ==============================

        [Example:]

        >>> result = entry.get_asset("key")

        ==============================
        """

        from contentstack import Asset
        asset = Asset()

        if key is None:
            raise KeyError('Kindly provide valid key')
        elif isinstance(key, str):
            result = self.get_json(key)
            if result is not None and isinstance(result, dict):
                asset = asset._configure(result)
            else:
                asset = None
        return asset

    def get_assets(self, key):

        """
        Get an assets from the entry. This works with multiple true fields
        :param key: key of asset
        :type key: str
        :return: list of Asset
        :rtype: list[Asset]
        
        ==============================
        
        [Example:]

        >>> result = entry.get_assets("key")
        
        ==============================
        """
        assets = []
        from contentstack import Asset

        if key is None:
            raise KeyError('Kindly provide valid key')
        elif isinstance(key, str):
            assetlist = self.get_list(key)
            if isinstance(assetlist, list):
                for assetobj in assetlist:
                    if isinstance(assetobj, dict):
                        asset = Asset()
                        model = asset._configure(assetobj)
                        assets.append(model)
        return assets

    def get_all_entries(self, ref_key, ref_content_type):

        """
        Get value for the given reference key.
        :param ref_key: key of a reference field.
        :type ref_key: str
        :param ref_content_type: class uid.
        :type ref_content_type: str
        :return: list of  :Entry instances. Also specified content_type value will be set as class uid for all
        :rtype: list[Entry]
        
        ==============================
        
        [Example:]

        >>> entry = entry.get_all_entries("reference_key", "reference_content_type")
        
        ==============================
        """
        all_entries = []
        if self.__result_json is not None and isinstance(ref_key, str):
            if ref_key in self.__result_json:
                list_entry = self.__result_json[ref_key]
                if isinstance(list_entry, list):
                    for entry_obj in list_entry:
                        entry = self.__stack_instance.content_type(ref_content_type).entry()
                        model = list_entry[entry_obj]
                        entry._configure(model)
                        all_entries.append(entry)
                    return all_entries
                else:
                    return None

    def excepts(self, *field_uid):

        """
        Specifies list of field field_uid that would be excluded from the response.
        :param field_uid: field_uid for variable number of arguments which get excluded from the response.
        *field_uid for variable number of arguments
        :type: str
        :return: self
        :rtype: Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> entry.excepts('title', 'colot', 'price_in_usd')
        
        ==============================
        """
        if field_uid is None:
            raise ValueError('Kindly provide a valid argument')
        self.__except_field = list(field_uid)

        return self

    def except_with_reference_uid(self, reference_field_uid, *field_uid):

        """
        :param: reference_field_uid: Key who has reference to some other class object.
        :type: str:
        :param: field_uid: field_uid for variable number of arguments
        *field_uid for variable number of arguments
        :type: str:
        :return: Entry
        :rtype: Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> entry.except_with_reference_uid('reference_field_uid', "field1", 'field2', 'field3');

        ==============================

        """
        if (reference_field_uid, field_uid) is None:
            raise ValueError('Kindly provide valid arguments')
        elif isinstance(reference_field_uid, str):
            self.__uid_for_except[reference_field_uid] = list(field_uid)
            self.include_reference(reference_field_uid)
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    def include_reference(self, *reference_uid):

        """
        Add a constraint that requires a particular reference key details.
        :param reference_uid: word args reference_field key that to be constrained. 
        *reference_uid for variable number of arguments
        :type reference_uid: str
        :return: self
        :rtype: Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> entry.includeReference("uid1, uid2, uid3")
        
        ==============================
        """

        if reference_uid is None:
            raise ValueError('Kindly provide a valid argument')
        self.__local_params["include[]"] = list(reference_uid)

        return self

    def only(self, *field_uid):

        """
        Specifies an array of only keys in BASE object that would be included in the response.
        :param field_uid: field_uid for variable number of arguments to be included in response.
        *field_uid for variable number of arguments
        :type field_uid: word args
        :return: self
        :rtype: Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> entry.only('field_uid1', 'field_uid2')
        
        ==============================
        """

        if field_uid is None:
            raise KeyError
        for uid in field_uid:
            self.__uid_for_only.append(uid)

        return self

    def only_with_reference_uid(self, reference_field_uid, *field_uid):

        """
        :param reference_field_uid:
        :type reference_field_uid: Key who has reference to some other class object..
        :param field_uid: field_uid for variable number of arguments to be included in response.
        *field_uid for variable number of arguments
        :type field_uid: word args of str type
        :return: self
        :rtype: Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> entry.only_with_reference_uid('reference_uid', 'some_value', 'field_uid1', 'field_uid2', 'field_uid3')
        
        ==============================
        """

        field_value_list = []
        for field in field_uid:
            field_value_list.append(field)
        if reference_field_uid is not None and isinstance(reference_field_uid, str):
            self.__only_dict[reference_field_uid] = field_value_list
            self.include_reference(reference_field_uid)
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    def include_reference_content_type_uid(self):

        """
        description  This method also includes the content type UIDs
        of the referenced entries returned in the response.
        :return: Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

        >>> entry.include_reference_content_type_uid()
        
        ==============================
        """

        self.__local_params['include_reference_content_type_uid'] = 'true'

        return self

    def include_content_type(self):

        """
        Include the details of the content type along with the entry/entries details.
        :return: Entry
        
        ==============================
        
        [Example:]

        >>> entry.include_content_type()
        
        ==============================
        """
        include_content_type = {'include_content_type': 'true', 'include_snippet_schema': 'true'}
        self.__local_params.update(include_content_type)

        return self

    def __set_include_json(self):

        if self.__uid_for_only is not None and len(self.__uid_for_only) > 0:
            self.__local_params["only[BASE][]"] = self.__uid_for_only
            self.__uid_for_only = None

        if self.__except_field is not None and len(self.__except_field) > 0:
            self.__local_params["except[BASE][]"] = self.__except_field
            self.__except_field = None

        if self.__uid_for_except is not None and len(self.__uid_for_except) > 0:
            self.__local_params["except"] = self.__uid_for_except
            self.__uid_for_except = None

        if self.__only_dict is not None and len(self.__only_dict) > 0:
            self.__local_params["only"] = self.__only_dict
            self.__only_dict = None

        return self

    def fetch(self):
        if self.__entry_uid is None:
            raise KeyError('Kindly provide entry uid')
        self.__set_include_json()
        self.__entry_url = '{}{}'.format(self.__entry_url, self.__entry_uid)
        result = self.__http_request.get_result(self.__entry_url, self.__local_params, self.__entry_headers)
        return result
