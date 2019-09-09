#  Entry
#  contentstack
#
#  Created by Shailesh Mishra on 22/06/19.
#  Copyright © 2019 Contentstack. All rights reserved.


from typing import List, Any


class Entry:

    """
    contentstack.entry
    This Get a single entry request fetches a particular entry of a content type.
    ~~~~~~~~~~~~~~~~~~
    This module implements the Entry class.
    API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#entries

    [ Note: If no version is mentioned, this request will retrieve the
    latest published version of the entry.
    To retrieve a specific version,
    make use of the version parameter and keep the environment parameter blank.]

    """

    def __init__(self, content_type_id=None):

        """

        The content type uid is useful to fetch a particular entry of a content type
        :param content_type_id: is used to get entry of respected content_type
        :type content_type_id: str

        Example:

         ```
         entry = stack.ContentType('product').entry()

         ```

        """
        self.__content_type_id = content_type_id
        self.__stack_instance = None
        self.__http_request = None
        self.__config = None
        self.__entry_url = None

        self.__local_params: dict = {}
        self.__stack_headers: dict = {}
        self.__only_dict: dict = {}
        self.__result_json: dict = {}
        self.__other_post_dict: dict = {}

        self.__uid_for_except: list = []
        self.__uid_for_only: list = []
        self.__except_dic: list = []
        self.__tags = list
        self.__reference_list: list = []

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

    def instance(self, stack_instance):

        """
        This method is useful to setup instance of stack and httpConnection, It is used to form a complete url.

        :param stack_instance: stack_instance con't be None
        :type stack_instance: Stack
        :return: self
        :rtype: Entry

        Example:

        ```
            entry = stack.content_type('product').entry()
            entry = stack.instance(stack_instance)
        ```

        """

        self.__stack_instance = stack_instance
        self.__config = self.__stack_instance.config
        self.__stack_headers.update(self.__stack_instance.headers)
        self.__entry_url = self.__config.endpoint
        if self.__content_type_id is not None:
            self.__entry_url = '{}/content_types/{}/entries/'.format(self.__entry_url, self.__content_type_id)
        if self.__stack_headers is not None:
            if 'environment' in self.__stack_headers:
                self.__local_params['environment'] = self.__stack_headers['environment']
        self.__http_request = self.__stack_instance.get_http_instance

        return self

    @property
    def headers(self):

        """
        This method is useful to get dictionary of the headers
        :return: The method is used to get list of headers.
        :rtype: dict

        Example:

        ```
            headers: dic = entry.headers
        ```

        """
        return self.__stack_headers

    @property
    def uid(self):

        """

        :return:
        :rtype:
        """
        return self.__entry_uid

    def set_uid(self, entry_uid):

        """
        the unique ID of the content type of which you wish to retrieve the details.
        The content type UID is generated based on the title of the content type and it is unique across a stack.

        :param entry_uid: The unique ID of the content type of which you wish to retrieve the details
        :type entry_uid: str
        :return: self
        :rtype: Entry

        Example:

        ```
            entry = self.stack_entry.content_type('product').entry(entry_uid)
            entry.set_uid('btlsomeuniqueid')

        ```

        """
        if entry_uid is not None and isinstance(entry_uid, str):
            self.__entry_uid = entry_uid
        else:
            raise ValueError('Kindly provide a valid entry_uid')

        return self

    def params(self, key, value):

        """

        This mwthod is useful to add additional Query parameters to the entry
        :param key: query param key
        :type key: str
        :param value: query param value
        :type value: str
        :return: self
        :rtype: Entry

        Example:

        ```
            entry = self.stack_entry.content_type('product').entry(entry_uid)
            entry.params('key', 'value')
        ```

        """
        if key and value is not None:
            if isinstance(key, str):
                self.__local_params[key] = value
            else:
                raise ValueError('Params key should be str')
        else:
            raise ValueError('Kindly provide a valid arguments')

        return self

    def version(self, version: str):

        """
        Enter the version number of the entry that you want to retrieve. However,
        to retrieve a specific version of an entry, you need to keep the environment parameter blank.

        :param version:
        :type version:
        :return:
        :rtype:

        Example:

        ```
            entry = self.stack_entry.content_type('product').entry(entry_uid)
            entry.version('7')
        ```
        """
        if version is not None and isinstance(version, str):
            self.__local_params["version"] = version
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    @property
    def locale(self):

        """
        It returns code of the language of which the entries needs to be included.
        :return: code of the language of which the entries needs to be included.
        :rtype: str

        Example: en-us

        ```
            entry = self.stack_entry.content_type('product').entry(entry_uid)
            locale = entry.locale
        ```

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

        Example:

        ```
            entry = self.stack_entry.content_type('product').entry(entry_uid)
            locale = entry.locale

        ```

        """
        if locale is not None and isinstance(locale, str):
            self.__local_params["locale"] = locale
        else:
            raise ValueError('Kindly provide a valid locale')

    def configure(self, model):

        """
        It accepts entry dictionary to parse and set respective fields
        :param model: entry dictionary
        :type model: dict
        :return: self
        :rtype: Entry

        Example:

        ```
            _entry = entry.configure(response)

        ```

        """
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

        """
        It is useful to accept the API key, access_token of stack of which you wish to retrieve the content types.

        :param key: key of the header
        :type key: str
        :param value: value of respected key header
        :type value: str
        :return: self
        :rtype: Entry

        Example:

        ```
            entry = self.stack_entry.content_type('product').entry(entry_uid)
            entry = entry.set_header('someKey', 'some_value')

        ```

        """
        if key and value is not None:
            if isinstance(key, str) and isinstance(value, str):
                self.__stack_headers[key] = value
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

        Example:

            ```
                header = remove_header('key')

            ```
        """

        if key is not None and isinstance(key, str):
            if key in self.__stack_headers:
                self.__stack_headers.pop(key)
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    @property
    def title(self):

        """
        This method returns title of the entry
        :return: Title of the entry
        :rtype: str

        Example.

        ```
            title = entry.title
        ```
        """
        return self.__title

    @property
    def urls(self):

        """
        This method returns urls of the entry
        :return:
        :rtype:

        Example.

         ```
            url = entry.urls
         ```

        """
        return self.__url

    @property
    def tags(self):

        """
        This method returns list of tags of the entry
        :return: This method returns tags of the entry
        :rtype: list

        Example.

        ```
         ags = entry.tags

        ```
        """
        return self.__tags

    @property
    def content_type(self):

        """
        This method returns content_type of the entry
        :return: content_type of the entry
        :rtype: str

        Example.

        ```
            content_type = get_content_type

        ```

        """
        return self.__content_type_id

    @property
    def uid(self):

        """
        This method returns uid of the entry
        :return: uid of the entry
        :rtype: str

        Example.

        ```
            uid = get_uid

        ```

        """
        return self.__entry_uid

    @property
    def to_json(self):

        """
        This method returns response of the entry in dictionary formats
        :return: response of the entry in dictionary type
        :rtype: dict

        Example.

        ```
            entry = entry.to_json

        ```
        """
        if self.__result_json is not None:
            return self.__result_json

    def get(self, key):

        """
        This method returns value of respective key of the entry
        :param key: key you want to access value
        :type key: str
        :return: json
        :rtype: object

        Example.

        ```
            entry.get('yourKey')

        ```
        """
        if self.__result_json is not None:
            if key is not None and isinstance(key, str) and key in self.__result_json:
                return self.__result_json[key]
            else:
                return None
        else:
            return None

    def get_string(self, key):

        """
        This method returns str type result of the entry
        :param key: key of the entry
        :type key: str
        :return: value from the dict of respective key
        :rtype: str

        Example.

        ```
            entry.get_string('entry_key')

        ```
        """
        value = self.get(key)
        if isinstance(value, str):
            return value
        else:
            return None

    def get_boolean(self, key: str):

        """
        This method returns bool type result of the entry
        :param key: key of the entry
        :type key: str
        :return: boolean value
        :rtype: bool

        Example.

        ```
            entry.get_boolean('bool_key')

        ```

        """
        value = self.get(key)
        if isinstance(value, bool):
            return value
        else:
            return None

    def get_json(self, key):

        """
        This method is useful to get result of respective key if result is dict
        :param key: key
        :type key:
        :return:
        :rtype:

        """
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
        :return:  uid who created this entry.
        :rtype:str

        Example. created_by = entry.get_created_by

        """
        return self.__created_by

    @property
    def updated_at(self):

        """
        value of updating time of entry.
        :return: updating time of entry.
        :rtype: str

        Example updated_at = entry.get_updated_at
        """

        return self.__updated_at

    @property
    def updated_by(self):

        """
        Get uid who updated this entry.
        :return: uid who updated entry.
        :rtype: str

        Example.  updated_by = entry.get_updated_by()
        """
        return self.__updated_by

    def asset(self, key):

        """
        Get an asset from the entry
        :return: asset uid
        :rtype: str

        Example. asset = entry.get_asset("key")

        """
        from contentstack import Asset
        asset = Asset()

        if key is not None:
            if isinstance(key, str):
                result = self.get_json(key)
                if result is not None and isinstance(result, dict):
                    asset = asset.configure(result)
            else:
                raise ValueError('Kindly provide valid KEY')
        return asset

    def get_assets(self, key: str) -> list:

        """

        Get an assets from the entry. This works with multiple true fields
        :param key: key of asset
        :type key: str
        :return: list of Asset
        :rtype: list[Asset]

        Example. assets = entry.get_assets("key")

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

    def get_all_entries(self, ref_key: str, ref_content_type: str):

        """

        :param ref_key: key of a reference field.
        :type ref_key: str
        :param ref_content_type:  class uid.
        :type ref_content_type: str
        :return: list of  :Entry instances. Also specified content_type value will be set as class uid for all
        :rtype: list[Entry]

        Example.

        ```
            cs_query = stack.contentType("content_type_uid").query()
            cs_query.include_reference("for_bug")
            result = cs_query.find()
            if result is not None:
            list_query = cs_query.get_dict
            for entry in list_query:
                 task_entry = entry.get_all_entries("for_task", "task")
        ```

        """
        from contentstack import ContentType

        if self.__result_json is not None and isinstance(self.__result_json[ref_key], list):
            list_of_entries: list = self.__result_json[ref_key]
            for entry in list_of_entries:
                if ref_content_type is not None:
                    entry_instance = ContentType(ref_content_type).entry()

    def except_field_uid(self, *argv):

        """
        Specifies list of field uids that would be &#39excluded&#39 from the response.
        stack = contentstack.stack("blt5d4sample2633b", "blt6d0240b5sample254090d", "stag")
        entry = stack.content_type.ContentType("content_type_uid").entry("entry_uid")
        entry.except_field_uid('name', 'description')

        :param argv: field uid  which get excluded from the response.
        :type: str
        :return: self
        :rtype: Entry object, so you can chain this call.

        Example.

        ```
            entry.except_field_uid('name', 'description', 'many', 'more')

        ```
        """
        for arg in argv:
            self.__uid_for_except.append(arg)
        return self

    def include_reference(self, *argv):

        """
        Add a constraint that requires a particular reference key details.
        :param argv: word args reference_field key that to be constrained.
        :type argv: str
        :return: self
        :rtype: Entry object, so you can chain this call.

        Example.

        ```
            entry.includeReference("reference_uid")
        ```
        """
        if argv is not None:
            for arg in argv:
                self.__reference_list.append(arg)
            self.__other_post_dict["include[]"] = self.__reference_list
        return self

    def only(self, *field_uid):

        """
        Specifies an array of only keys in BASE object that would be &#39;included&#39; in the response.
        :param field_uid: word args  of the only reference keys to be included in response.
        :type field_uid: word args
        :return: self
        :rtype: Entry object, so you can chain this call.

        Example.

        ```
            field_uid: entry.only('name', 'description')

        ```
        """
        if field_uid is not None and len(field_uid) > 0:
            for field in field_uid:
                self.__uid_for_only.append(field)
        return self

    def only_with_reference_uid(self, reference_field_uid, *field_uid):

        """
        :param reference_field_uid:
        :type reference_field_uid: Key who has reference to some other class object..
        :param field_uid: word args the only reference keys to be included in response.
        :type field_uid: word args of str type
        :return: self
        :rtype: Entry object, so you can chain this call.

        Example.
        ```
            entry.only_with_reference_uid('reference_uid', 'some_value', som another value)

        ```
        """
        field_value_list: list = []
        for field in field_uid:
            field_value_list.append(field)
        if reference_field_uid is not None and isinstance(reference_field_uid, str):
            self.__only_dict[reference_field_uid] = field_value_list
            self.include_reference(reference_field_uid)
        else:
            raise ValueError('Kindly provide a valid input')

        return self

    def except_with_reference_uid(self, reference_field_uid, *field_uid):

        """
        :param reference_field_uid: field_uid word args str type value that except reference
        keys to be excluded in response.
        :type reference_field_uid:
        :param field_uid:
        :type field_uid:
        :return:
        :rtype:
        """

        """
        :param field_uid: field_uid list of the &#39;except&#39; reference keys to be excluded in response.
        :param reference_field_uid: Key who has reference to some other class object.
        :return: Entry object, so you can chain this call.

        stack = contentstack.stack( "blt5d4sample2633b", "blt6d0240b5sample254090d", "stag");
        entry = stack.contentType("content_type_uid").entry("entry_uid")
        array.append("description")
        array.append("name")
        entry.except_with_reference_uid(array, "reference_uid");
        """
        field_value_list: list = []
        for field in field_uid:
            field_value_list.append(field)
        if reference_field_uid is not None and isinstance(reference_field_uid, str):
            self.__uid_for_except[reference_field_uid] = field_value_list
            self.include_reference(reference_field_uid)
        else:
            raise ValueError('Kindly provide a valid input')

        return self

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

    def fetch(self):

        from contentstack.errors import ContentstackError
        if self.__entry_uid is None:
            raise ContentstackError('Kindly provide entry uid')
        # Example:
        # https://cdn.contentstack.io/v3/content_types/product/entries/blt9965f5f9840923ba?version=7&environment=production&locale=en-us
        self.__entry_url = '{}{}'.format(self.__entry_url, self.__entry_uid)
        result = self.__http_request.get_result(self.__entry_url, self.__local_params, self.__stack_headers)
        return result
