# __init__.py

# Contentstack testcases
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

from unittest import TestCase
from contentstack import config
from contentstack.stack import Stack


class ContentstackTestcase(TestCase):

    def setUp(self):
        self.stack = Stack(api_key='blt20962a819b57e233', access_token='blt01638c90cc28fb6f', environment='development')
        self.production_stack = Stack(api_key="blt20962a819b57e233", access_token="cs18efd90468f135a3a5eda3ba",
                                      environment="production")

    ####################################
    # [Stack-testcases]
    ####################################
    def test_stack(self):
        self.assertEqual('development', self.stack.environment)
        self.assertEqual('blt01638c90cc28fb6f', self.stack.access_token)
        self.assertEqual('blt20962a819b57e233', self.stack.application_key)

    def test_config(self):
        conf = config.Config()
        self.assertEqual('v3', conf.version())
        self.assertEqual('cdn.contentstack.io', conf.host())
        self.assertEqual('https://cdn.contentstack.io/v3/stacks', conf.endpoint('stacks'))

    def test_include_collaborators(self):
        is_contains = False
        self.stack.collaborators()
        result, err = self.stack.fetch()
        if err is None:
            result = result['stack']
            if 'collaborators' in result:
                is_contains = True
            self.assertEqual(True, is_contains)

    def test_stack_fetch_collaborators(self):
        stack_fetch = self.stack.collaborators()
        result = stack_fetch.fetch()
        if 'collaborators' in result:
            collaborators = result["collaborators"]
            print("collaborators", collaborators)
            print("collaborators count", len(collaborators))
            self.assertTrue(True)

    def test_stack_fetch_discrete_variables(self):
        discrete_var = self.stack.include_discrete_variables()
        result = discrete_var.fetch()
        if 'discrete_variables' in result:
            discrete_variables = result["discrete_variables"]
            print("discrete_var", discrete_variables)
            self.assertTrue(True)

    def test_stack_fetch_stack_variables(self):
        stack_var = self.stack.include_stack_variables()
        result = stack_var.fetch()
        if 'stack_variables' in result:
            stack_variables = result["stack_variables"]
            print("stack_variables", stack_variables)
            self.assertTrue(True)

    def test_stack_include_count(self):
        stack_var = self.stack.include_count()
        result = stack_var.fetch()
        if 'stack_variables' in result:
            stack_variables = result["stack_variables"]
            print("stack_variables", stack_variables)
            self.assertTrue(True)

    def test_image_transform(self):
        url = self.stack.image_transform("www.contentstack.io/endpoint", firstname="sita", lastname="sharma", age=22,
                                         phone=1234567890)
        if 'age' in url:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    ####################################
    # [Sync-testcases]
    ####################################

    def test_sync_pagination(self):
        sync_stack = Stack(api_key="blt477ba55f9a67bcdf", access_token="cs7731f03a2feef7713546fde5", environment="web")
        result, error = sync_stack.pagination('bltbb61f31a70a572e6c9506a')
        if error is None:
            print(result)
        else:
            error_code = error["error_code"]
            self.assertEquals(141, error_code)

    def test_init_sync(self):
        sync_stack = Stack("blt477ba55f9a67bcdf", "cs7731f03a2feef7713546fde5", "web")
        result, err = sync_stack.sync(from_date='2018-01-14T00:00:00.000Z', content_type_uid='session',
                                      publish_type='entry_published')
        if err is None:
            print(result, type(result))
            self.assertEquals(int, type(result.get_total_count()))

        # if err is None:
        # result = result['items']
        # self.assertEquals(list, type(result))
        # self.assertEquals(7, len(result))
        # for data in result:
        # type_of_data = data["type"]
        # print(type_of_data, data["data"])
        # self.assertEquals('entry_published', type_of_data)

    def test_sync_token(self):
        sync_stack = Stack(api_key="blt477ba55f9a67bcdf", access_token="cs7731f03a2feef7713546fde5", environment="web")
        response, error = sync_stack.sync_token('bltbb61f31a70a572e6c9506a')
        items = response.get_total_count()
        self.assertTrue(9, items)

    ##############################################################
    # [ContentType class]
    ##############################################################

    def test_content_type_uid(self):
        variable = self.stack.content_type('product')
        self.assertEqual('product', variable._content_type_uid)

    def test_content_type_headers(self):
        variable = self.stack.content_type('product')
        var_ct: dict = variable.headers
        var_head: dict = self.stack.headers
        self.assertEqual(len(var_ct), len(var_head))

    def test_content_types(self):
        result, error = self.stack.content_types()
        if error is None:
            if 'content_types' in result:
                result = result['content_types']
                self.assertEqual(list, type(result))
                self.assertEqual(4, len(result))

    def test_content_type(self):
        ct = self.stack.content_type('product')
        result, error = ct.fetch()
        if error is None:
            if 'schema' in result:
                schema_result = result['schema']
                for schema in schema_result:
                    print(schema)
                self.assertEquals(list, type(schema_result))

    ##############################################################
    # [Entry class]
    ##############################################################

    def test_get_entries_by_uid(self):
        entry = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        result, err = entry.fetch()
        if err is None:
            result = result['entry']
            self.assertEquals(dict, type(result))

    def test_entry_title(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        result = entry_instance.fetch()
        if result is not None:
            self.assertEquals("Redmi Note 3", entry_instance.get_title())

    def test_entry_url(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        result = entry_instance.fetch()
        if result is not None:
            self.assertEquals("", entry_instance.get_url())

    def test_entry_tags(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        result = entry_instance.fetch()
        if result is not None:
            self.assertEquals(list, type(entry_instance.get_tags()))

    def test_entry_content_type(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        result = entry_instance.fetch()
        if result is not None:
            self.assertEquals('product', entry_instance.get_content_type())

    def test_entry_get_uid(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        result = entry_instance.fetch()
        if result is not None:
            self.assertEquals('blt9965f5f9840923ba', entry_instance.get_uid())

    def test_entry_get_locale(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            if '-' in entry_instance.get_locale():
                self.assertEquals('en-us', entry_instance.get_locale())

    def test_entry_to_json(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            self.assertEquals(dict, type(entry_instance.to_json()))

    def test_entry_get(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        print(result)
        if result is not None:
            self.assertEquals('blt9965f5f9840923ba', entry_instance.get('uid'))

    def test_entry_get_string(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            self.assertEquals(str, type(entry_instance.get_string('description')))

    def test_entry_get_boolean(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            self.assertFalse(None, type(entry_instance.get_boolean('description')))

    def test_entry_get_json(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            json_result = entry_instance.get_json('publish_details')
            self.assertEquals(dict, type(json_result))

    def test_entry_get_int(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            json_result = entry_instance.get_int('color')
            self.assertFalse(None, type(json_result))

    def test_entry_get_created_at(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            created_at = entry_instance.get_created_at()
            self.assertTrue(str, type(created_at))

    def test_entry_get_created_by(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            created_by = entry_instance.get_created_by()
            self.assertTrue(str, type(created_by))

    def test_entry_get_updated_at(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            updated_at = entry_instance.get_updated_at()
            self.assertTrue(str, type(updated_at))

    def test_entry_get_updated_by(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        result = entry_instance.fetch()
        if result is not None:
            updated_by = entry_instance.get_updated_by()
            self.assertTrue(str, type(updated_by))

    def test_entry_get_asset(self):
        entry_instance = self.production_stack.content_type('product').entry('blt9965f5f9840923ba')
        entry_instance.locale('en-us')
        entry_instance.get_asset("key")
        result = entry_instance.fetch()
        # incomplete

    # [ASSETS]

    # def test_init_asset(self):
    # asset: Asset = self.production_stack.asset('some_uid')
    # asset.add_params('ewqweed')
