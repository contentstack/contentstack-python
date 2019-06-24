"""

 * MIT License

 * Copyright (c) 2012 - 2019 Contentstack

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


class Entry(object):

    def __init__(self, entry_uid=None, content_type_id=None, content_type_instance=None):
        self.ct_instance = content_type_instance
        self.local_header = {}
        self.entry_uid = entry_uid
        self.content_type_id = content_type_id
        self._metadata = {}

    def set_content_type_instance(self, content_type_instance):
        return self

    def set_uid(self, entry_uid: str):
        if entry_uid is not None:
            self.entry_uid = entry_uid

    def configure(self, **model):
        # [SET this section after Entry Model setup]
        self._model = model
        self.result_json = {}
        # self._model.jsonObject
        # self.owner_email_id = self._model.ownerEmailId
        # self.owner_uid = self._model.owner_uid
        self.title = 'self._model.title'
        self.url = 'self._model.url'
        # if self._model.owner_map != None:
        self.owner = {}
        if self._metadata != None:
            # self._metadata = self._model._metadata

            # self.uid = model.entryUid;
            # self.set_tags('model.tags')
            # model = null;
            return self

    def set_header(self, key, value):
        ''' [Uses]: header = set_header('key', 'value')'''
        if key != None and value != None:
            self.local_header[key] = value

    def remove_header(self, key):
        ''' [Uses]: header = remove_header('key')'''
        if key in self.local_header:
            self.local_header.pop(key)

    def get_title(self):

        """
        [Uses]: title = get_title()
        """

        return self.title

    def get_url(self):

        """
        [Uses]: url = get_url()
        """
        return self.url

    def get_tags(self):
        ''' [Uses]: url = get_url()'''
        return self.tags

    def set_tags(self, tags_list):
        self.tags = tags_list

    def get_content_type(self):
        return self.content_type_id

    def get_uid(self):
        return self.entry_uid

    def get_metadata(self):
        return self._metadata

    def get_locale(self):
        if self._metadata != None and len(self._metadata) > 0 and 'locale' in self._metadata:
            locale_code = self._metadata['locale']
        if 'locale' in self.result_json:
            locale_code = self.result_json['locale']

        return locale_code

    def get_owner(self):
        if self.owner is not None:
            return self.owner

    def to_json(self):
        if self.result_json is not None:
            return self.result_json

    def get(self, key):
        if self.result_json is not None and key != None:
            if key in self.result_json:
                result = self.result_json[key]

        return result

    def get_string(self, key):
        value = self.get(key)
        if value != None and type(value) == str:
            return value
        else:
            return None
        return value

    def get_boolean(self, key):
        value = self.get(key)
        if value != None and type(value) == bool:
            return value
        else:
            return None
        return False

    def get_json(self, key):
        value = self.get(key)
        if value != None and type(value) == dict:
            return value
        else:
            return None

        return value

    def get_number(self, key):
        value = self.get(key)
        if value != None and type(value) == int:
            return value
        else:
            return None
        return None

    def get_float(self, key):
        value = self.get(key)
        if value != None and type(value) == float:
            return value
        else:
            return None
        return None

    def get_date(self, key):
        value = self.get(key)
        if value != None:
            value = self.parse_date(value)
            return value
        else:
            return None
        return None

    def parse_date(self, raw_date, timezone=None):
        return ''

    def get_created_at(self):
        value = self.get('created_at')
        if value != None:
            value = self.parse_date(value)
        return value

    def get_created_by(self):
        value = self.get('created_at')
        if value != None:
            value = self.parse_date(value)
        return value

    def get_updated_at(self):
        value = self.get('updated_at')
        if value is not None:
            value = self.parse_date(value)
        return value

    def get_updated_by(self):
        value = self.get('updated_at')
        if value is not None:
            value = self.parse_date(value)
        return value

    def get_deleted_at(self):
        value = self.get('deleted_at')
        if value is not None:
            value = self.parse_date(value)
        return value

    def get_deleted_by(self):
        value = self.get('deleted_by')
        if value is not None:
            value = self.parse_date(value)
        return value

    def get_asset(self, key):
        asset_object = self.get_json(key)

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

    def except_eith_reference_uid(sel):
        pass


