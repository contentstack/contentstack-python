"""

Created by Shailesh Mishra on 22/06/19.
Copyright 2019 Contentstack. All rights reserved.

contentstack.entry
~~~~~~~~~~~~~~~~~~

API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#entries

"""


class Entry:
    """
    [Note]: If no version is mentioned, this request will retrieve the
    latest published version of the entry.To retrieve a specific version, make use of the version parameter 
    and keep the environment parameter blank.

    ==============================

    [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()

    ==============================

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
        It is useful to accept the API key, access_token of stack of which you wish to retrieve 
        the content types.
        
        Arguments:
            key {str} -- key of header
            value {str} -- value of header
        
        Raises:
            KeyError: If case when key or value is None

            KeyError: key and value type should be str
        
        Returns:
            Entry -- Entry class instance, that helps to chain the call
        
        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.add_header('key', 'value')
            >>> entry = entry.fetch() 

        ==============================

        """

        if None in (key, value):
            raise KeyError
        elif isinstance(key, str) and isinstance(value, str):
            self.__entry_headers[key] = value
        else:
            raise KeyError('key and value type should be str')

        return self

    def remove_header(self, key):

        """
         To remove desired header key
        
        Arguments:
            key {str} -- existing key of header
    
        Raises:
            KeyError: Kindly provide a valid key, key should not be None or str
        
        Returns:
            Entry -- Entry class object so we can chain the call

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.remove_header('key')
            >>> entry = entry.fetch() 
            
        ==============================
        """

        if key is None or not isinstance(key, str):
            raise KeyError('Kindly provide valid KEY')
        elif isinstance(key, str):
            if key in self.__entry_headers:
                self.__entry_headers.pop(key, None)

        return self

    @property
    def uid(self):

        """
        uid of the entry
        
        Returns:
            str -- str type entry uid

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch() 
            >>> entry_uid = entry.uid

        ==============================
        """
        return self.__entry_uid

    @uid.setter
    def uid(self, uid):

        """
        The unique ID of the content type of which you wish to retrieve the details.
        The content type UID is generated based on the title of the content type 
        and it is unique across a stack.
        
        Arguments:
            uid {str} -- entry uid
        
        Raises:
            KeyError: key should not be None or empty str
        
        Returns:
            Entry -- Entry class object so we can chain the call

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry.uid = 'bltsomethingasuid'
            >>> entry = entry.fetch() 

        ==============================

        """

        if uid is None or not isinstance(uid, str):
            raise KeyError('Kindly provide a valid uid')
        self.__entry_uid = uid

        return self

    @property
    def locale(self):

        """
        It returns code of the language of which the entries needs to be included.
        
        Returns:
            str -- language of the entry
        
        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch() 
            >>> locale = entry.locale

        ==============================

        """

        if 'locale' in self.__result_json:
            return self.__result_json['locale']
        else:
            return self.__locale

    @locale.setter
    def locale(self, locale):

        """
        Locale accepts code of the language of which the entries needs to be included.
        Only the entries published in this locale will be displayed.
        
        Arguments:
            locale {str} -- language code
        
        Raises:
            KeyError: locale should not be None or empty, type of locale should be str
        
        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry.locale = 'en-us'
            >>> entry = entry.fetch() 

        ==============================
        """

        if locale is None and not isinstance(locale, str):
            raise KeyError('Kindly provide a valid locale')
        self.__local_params["locale"] = locale

    @property
    def title(self):

        """This method returns title of the entry

        Returns:
            str -- title of the entry

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch() 
            >>> title = entry.title

        ==============================

        """

        return self.__title

    @property
    def url(self):

        """
        This method returns url of the entry

        Returns:
            str -- url of the entry

        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> url = entry.url
        
        ==============================

        """

        return self.__url

    @property
    def tags(self):

        """This method returns list of tags of the entry

        Returns:
            list -- tags of entry
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> tags = entry.tags
        
        ==============================
        """

        return self.__tags

    @property
    def content_type(self):

        """This method returns content_type of the entry

        Returns:
            str -- content_type_uid of the entry
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> content_type = entry.content_type
        
        ==============================

        """

        return self.__content_type_id

    @property
    def headers(self):

        """This method is useful to get dictionary of the headers

        Returns:
            dict -- The method is used to get list of headers.

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> headers = entry.headers

        ==============================

        """

        return self.__entry_headers

    @property
    def json(self):

        """
        This method returns response of the entry in dictionary formats

        Returns:
            dict -- response of the entry
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> result = entry.json
        
        ==============================

        """
        # return None if self.__result_json == None else self.__result_json
        if self.__result_json is None:
            return None
        else:
            return self.__result_json

    @property
    def created_at(self):

        """
        Returns:
            str -- value of creation time of entry

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> created_at = entry.created_at

        ==============================
        """

        return self.__created_at

    @property
    def created_by(self):

        """
        Returns:
            str -- uid who created this entry

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> created_by = entry.created_by

        ==============================
        """

        return self.__created_by

    @property
    def updated_at(self):

        """
        Returns:
            str -- updating time of entry.

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> result = entry.updated_at

        ==============================

        """

        return self.__updated_at

    @property
    def updated_by(self):

        """

        Returns:
            str -- uid who updated entry.

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> result = entry.updated_by

        ==============================
        """

        return self.__updated_by

    def get(self, key):

        """
        This method returns value of respective key of the entry
        
        Arguments:
            key {str} -- field_uid as key

        Returns:
            object -- onject by key you wants to access

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> result = entry.get('key')

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
        
        Arguments:
            key {str} -- key The key as string which needs to be added to an Entry
            value {object} -- value The value as string which needs to be added to an Entry
        
        Raises:
            ValueError: If key or value is None
            ValueError: If key is not type of str
        
        Returns:
            Entry -- So can we chain the call

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> entry = entry.add_param('key', 'value')

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
        Enter the version number of the entry that you want to retrieve. 
        However, to retrieve a specific version of an entry, you need to keep the environment parameter blank.
        
        Arguments:
            version {str} -- version if entry
        
        Raises:
            ValueError: If version is None or not str type

        Returns:
            Entry -- So we can chain the call

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> entry = entry.version('7')

        ==============================
        
        """

        if version is None or not isinstance(version, str):
            raise ValueError('Kindly provide valid')
        elif isinstance(version, str):
            self.__local_params["version"] = version

        return self

    def get_string(self, key):

        """
        This method returns str type result of the entry
        
        Arguments:
            key {str} -- field_uid    

        Returns:
            str -- value from the dict of respective key
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> result = entry.get_string('key')
        
        ==============================
        """

        value = self.get(key)
        if isinstance(value, str):
            return value
        return None

    def get_boolean(self, key):

        """
        This method returns bool type result of the entry
        
        Arguments:
            key {str} -- field_uid 
        
        Raises:
            KeyError: If key instance is not str
        
        Returns:
            bool -- boolean value
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
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

        Arguments:
            key {str} -- field_uid

        Returns:
            dict -- result dict by key
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
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
        It returns the list type data

        Arguments:
            key {str} -- field_uid

        Returns:
            list -- list of data from the entry
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
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

        Arguments:
            key {str} -- field_uid

        Returns:
            Asset -- Asset of the entry

        ==============================

        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> result = entry.asset("key")

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

        return asset

    def get_assets(self, key):

        """
        Get an assets from the entry. This works with multiple true fields

        Arguments:
            key {str} -- field_uid

        Returns:
            list[Asset] -- list of Asset
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
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
        
        Arguments:
            ref_key {str} -- ref_key key of a reference field.
            ref_content_type {str} -- ref_content_type class uid.

        Returns:
            list[Asset] -- Entry instances. Also specified content_type value will be set as class uid for all
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> all_entries = entry.get_all_entries("reference_key", "reference_content_type")
        
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
                return None

    def excepts(self, *field_uid):

        """
        Specifies list of field field_uid that would be excluded from the response.

        Returns:
            Entry -- Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> entry = entry.excepts('title', 'color', 'price_in_usd')
        
        ==============================

        """

        if field_uid is None:
            raise ValueError('Kindly provide a valid argument')
        self.__except_field = list(field_uid)

        return self

    def except_with_reference_uid(self, reference_field_uid, *field_uid):

        """
        Specifies an array of &#39;except&#39; keys that would be excluded in the response.

        Arguments:
            reference_field_uid {str} -- Key who has reference to some other class object.
            field_uid {str}: field_uid for variable number of arguments      
        
        Raises:
            ValueError: reference_field_uid and field_uid should not be None
            ValueError: reference_field_uid should be str type
        
        Returns:
            Entry -- Entry object, so you can chain this call.

        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> entry = entry.except_with_reference_uid('reference_field_uid', "field1", 'field2', 'field3')

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
        
        Raises:
            ValueError: if reference_uid is None
        
        Returns:
            Entry -- Entry object, so you can chain this call.

        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> entry.include_reference('uid1', 'uid2', 'uid3')
        
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
        field_uid for variable number of arguments

        Returns:
            Entry -- Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> entry.only('uid1', 'uid2', 'uid3')

        ==============================
        """

        if field_uid is None:
            raise KeyError
        for uid in field_uid:
            self.__uid_for_only.append(uid)

        return self

    def only_with_reference_uid(self, reference_field_uid, *field_uid):

        """
        Specifies an array of only keys that would be included in the response.
        
        Arguments:
            reference_field_uid {str} -- Key who has reference to some other class object.
            field_uid {comma seprated str objects} -- for variable number of arguments
        
        Raises:
            ValueError: If reference_field_uid is None or not str type
        
        Returns:
            Entry -- Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> entry.only_with_reference_uid('reference_uid', 'uid1', 'uid2', 'uid3')

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
        
        Returns:
            Entry -- Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
            >>> entry.include_reference_content_type_uid()

        ==============================
        """

        self.__local_params['include_reference_content_type_uid'] = 'true'

        return self

    def include_content_type(self):

        """
        Include the details of the content type along with the entry/entries details.
        
        Returns:
            Entry -- Entry object, so you can chain this call.
        
        ==============================
        
        [Example:]

            >>> from stack import Stack
            >>> stack = Stack(api_key='stack_api_key', access_token='stack_access_token', environment='env')
            >>> content_type = stack.content_type('content_type_uid')
            >>> entry = content_type.entry('uid')
            >>> entry = entry.fetch()
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

        """Fetches the latest version of the entries from stack
        
        Raises:
            KeyError: If entry_uid is None
        
        Returns:
            Entry - Entry object, so you can chain this call.

        """

        if self.__entry_uid is None:
            raise KeyError('Kindly provide entry uid')
        self.__set_include_json()
        self.__entry_url = '{}{}'.format(self.__entry_url, self.__entry_uid)
        result = self.__http_request.get_result(self.__entry_url, self.__local_params, self.__entry_headers)
        return result
