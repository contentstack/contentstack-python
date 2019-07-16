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

import logging
from unittest import TestCase
from contentstack.stack import Stack


class ContentstackTestcase(TestCase):
    log = logging.getLogger(__name__)

    def setUp(self):

        self.stack = Stack(api_key='blt20962a819b57e233', access_token='blt01638c90cc28fb6f', environment='development')
        self.stack_asset = Stack(api_key='blt20962a819b57e233', access_token='blt01638c90cc28fb6f',
                                 environment='production')
        self.stack_entry = Stack(api_key="blt20962a819b57e233", access_token="cs18efd90468f135a3a5eda3ba",
                                 environment="production")
        self.stack_query = Stack(api_key='blt20962a819b57e233', access_token='blt01638c90cc28fb6f',
                                 environment='production')

    # [Stack]

    def test_stack(self):
        self.assertEqual('development', self.stack.environment)
        self.assertEqual('blt01638c90cc28fb6f', self.stack.access_token)
        self.assertEqual('blt20962a819b57e233', self.stack.application_key)

    def test_config(self):
        from contentstack import Config
        conf = Config()
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

    # [Sync]

    def test_sync_pagination(self):
        sync_stack = Stack(api_key="blt477ba55f9a67bcdf", access_token="cs7731f03a2feef7713546fde5", environment="web")
        result, error = sync_stack.pagination('bltbb61f31a70a572e6c9506a')
        if error is None:
            print(result)
        else:
            error_code = error["error_code"]
            self.assertEqual(141, error_code)

    def test_init_sync(self):
        sync_stack = Stack("blt477ba55f9a67bcdf", "cs7731f03a2feef7713546fde5", "web")
        result, err = sync_stack.sync(from_date='2018-01-14T00:00:00.000Z', content_type_uid='session',
                                      publish_type='entry_published')
        if err is None:
            print(result, type(result))
            self.assertEqual(int, type(result.count))

    def test_sync_token(self):
        sync_stack = Stack(api_key="blt477ba55f9a67bcdf", access_token="cs7731f03a2feef7713546fde5", environment="web")
        response, error = sync_stack.sync_token('bltbb61f31a70a572e6c9506a')
        items = response.count
        self.assertTrue(9, items)

    # [ContentType class]

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
        content_type = self.stack.content_type('product')
        result, error = content_type.fetch()
        if error is None:
            if 'schema' in result:
                schema_result = result['schema']
                for schema in schema_result:
                    print(schema)
                self.assertEqual(list, type(schema_result))

    # [Entry]

    def test_entry_by_uid(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        result, err = _entry.fetch()
        if err is None:
            self.assertEqual(dict, type(result))

    def test_entry_title(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        result = _entry.fetch()
        if result is not None:
            self.assertEqual("Redmi Note 3", _entry.title)

    def test_entry_url(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        result = _entry.fetch()
        if result is not None:
            self.assertEqual("", _entry.urls)

    def test_entry_tags(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        result = _entry.fetch()
        if result is not None:
            self.assertEqual(list, type(_entry.tags))

    def test_entry_content_type(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        result = _entry.fetch()
        if result is not None:
            self.assertEqual('product', _entry.content_type)

    def test_is_entry_uid_correct(self):
        entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        result = entry.fetch()
        if result is not None:
            self.assertEqual('blt9965f5f9840923ba', entry.uid)

    def test_entry_locale(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            if '-' in _entry.locale:
                self.assertEqual('en-us', _entry.locale)

    def test_entry_to_json(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            self.assertEqual(dict, type(_entry.to_json))

    def test_entry_get(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            self.assertEqual('blt9965f5f9840923ba', _entry.get('uid'))

    def test_entry_string(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            self.assertEqual(str, type(_entry.get_string('description')))

    def test_entry_boolean(self):
        entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        entry.locale = 'en-us'
        result = entry.fetch()
        if result is not None:
            self.assertFalse(None, type(entry.get_boolean('description')))

    def test_entry_json(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            json_result = _entry.get_json('publish_details')
            self.assertEqual(dict, type(json_result))

    def test_entry_get_int(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            json_result = _entry.get_int('color')
            self.assertFalse(None, type(json_result))

    def test_entry_get_created_at(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            created_at = _entry.created_at
            self.assertTrue(str, type(created_at))

    def test_entry_get_created_by(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            created_by = _entry.created_by
            self.assertTrue(str, type(created_by))

    def test_entry_get_updated_at(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            updated_at = _entry.updated_at
            self.assertTrue(str, type(updated_at))

    def test_entry_get_updated_by(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        result = _entry.fetch()
        if result is not None:
            updated_by = _entry.updated_by
            self.assertTrue(str, type(updated_by))

    def test_entry_get_asset(self):
        _entry = self.stack_entry.content_type('product').entry('blt9965f5f9840923ba')
        _entry.locale = 'en-us'
        # incomplete
        # some more testcases required

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # #############################################
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # [ASSETS]
    def test_asset(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        _asset.version(1)
        _asset.relative_urls()
        _asset.include_dimension()
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual(16, len(result))
            logging.debug(result)

    def test_asset_relative_urls(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        _asset.relative_urls()
        result, error = _asset.fetch()
        if error is None:
            self.assertNotIn('images.contentstack.io/', _asset.url)
            logging.debug(result)

    def test_asset_version(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        _asset.version(1)
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual(1, _asset.get_version)
            logging.debug(result)

    def test_asset_include_dimension(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        _asset.include_dimension()
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual(tuple, type(_asset.dimension))
            logging.debug('tuple dimension is %s ' + _asset.dimension.__str__())

    def test_asset_remove_header(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        _asset.remove_header('access_token')
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual(2, 22)
        else:
            self.assertEqual(105, error['error_code'], 'mean to fail. Fail is expected output')

    def test_asset_uid(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual('blt91af1e5af9c3639f', _asset.asset_uid)

    def test_asset_filetype(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual('image/png', _asset.filetype)

    def test_asset_file_size(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual('63430', _asset.filesize)

    def test_asset_filename(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual('.png', _asset.filename[-4:])

    def test_asset_url(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual('.png', _asset.url[-4:])

    def test_asset_to_json(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual(dict, type(_asset.to_json))

    def test_asset_create_at(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            sallie: str = _asset.create_at
            var_shailesh, fileid = sallie.split('T')
            self.assertEqual('2017-01-10', var_shailesh)

    def test_asset_create_by(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            sallie: str = _asset.create_by
            var_shailesh, fileid = sallie.split('_')
            self.assertEqual('sys', var_shailesh)

    def test_asset_update_at(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            sallie: str = _asset.update_at
            var_shailesh, fileid = sallie.split('T')
            self.assertEqual('2017-01-10', var_shailesh)

    def test_asset_update_by(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            sallie: str = _asset.update_by
            var_shailesh, fileid = sallie.split('_')
            self.assertEqual('sys', var_shailesh)

    def test_asset_tags(self):
        _asset = self.stack_asset.asset('blt91af1e5af9c3639f')
        result, error = _asset.fetch()
        if error is None:
            self.assertEqual(list, type(_asset.tags))

    def test_assets(self):
        _asset = self.stack_asset.asset()
        result, error = _asset.fetch_all()
        if error is None:
            self.assertEqual(list, type(result))

    # [Asset Library]

    def test_asset_library(self):
        _asset_library = self.stack_asset.asset_library()
        result, error = _asset_library.fetch_all()
        if error is None:
            self.assertEqual(list, type(result))

    # [QUERY]

    def test_query_content_type(self):
        query = self.stack_query.content_type('product').query()
        self.assertEqual('product', query.content_type)

    def test_query_headers(self):
        query = self.stack_query.content_type('product').query()
        headers = query.headers
        self.assertEqual(3, len(headers))

    def test_query_remove_headers(self):
        query = self.stack_query.content_type('product').query()
        headers = query.remove_header('environment')
        self.assertEqual(2, len(headers))

    def test_query_add_headers(self):
        query = self.stack_query.content_type('product').query()
        headers = query.add_header('env', 'mishra')
        self.assertEqual(4, len(headers))

    def test_query_where(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us').where("title", "Redmi 3S")
        result, error = query.find()
        if error is None:
            self.assertEqual(1, len(result))

    def test_query_add_query(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        query.add_query("limit", "8")
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_remove_query(self):
        query = self.stack_query.content_type('product').query()
        query.locale('en-us')
        query.add_query("limit", "3")
        query.remove_query('limit')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_and_query(self):

        content_type = self.stack_query.content_type('product')
        base_query = content_type.query()
        base_query.locale('en-us')
        # query where title is equals to Redmi Note 3
        query = content_type.query()
        query.where("title", "Redmi Note 3")
        # query where color is equals to Gold
        sub_query = content_type.query()
        sub_query.where("color", "Gold")
        # adding query in list
        list_array = [query, sub_query]
        # passing query list in and_query
        base_query.and_query(list_array)
        result, error = base_query.find()
        if error is None:
            self.assertEqual(1, len(result))

    def test_query_or_query(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        # query where title is equals to Redmi Note 3
        query1 = content_type.query()
        query1.where("color", "Black")
        # query where color is equals to Gold
        query2 = content_type.query()
        query2.where("color", "Gold")
        # adding query in list
        list_array = [query1, query2]
        # passing query list in and_query
        query.or_query(list_array)
        result, error = query.find()
        if error is None:
            self.assertEqual(5, len(result))

    def test_query_less_than(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.less_than('price_in_usd', 600)
        result, error = query.find()
        if error is None:
            self.assertEqual(5, len(result))

    def test_query_less_than_or_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.less_than_or_equal_to('price_in_usd', 146)
        result, error = query.find()
        if error is None:
            self.assertEqual(4, len(result))

    def test_query_greater_than(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.greater_than('price_in_usd', 146)
        result, error = query.find()
        if error is None:
            self.assertEqual(3, len(result))

    def test_query_greater_than_or_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.greater_than_or_equal_to('price_in_usd', 146)
        result, error = query.find()
        if error is None:
            self.assertEqual(4, len(result))

    def test_query_not_equal_to(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.not_equal_to('price_in_usd', 146)
        result, error = query.find()
        if error is None:
            self.assertEqual(6, len(result))

    def test_query_contained_in(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        in_list = [101, 749]
        query.contained_in('price_in_usd', in_list)
        result, error = query.find()
        if error is None:
            self.assertEqual(2, len(result))

    def test_query_not_contained_in(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        in_list = [101, 749]
        query.not_contained_in('price_in_usd', in_list)
        result, error = query.find()
        if error is None:
            self.assertEqual(5, len(result))

    def test_query_exists(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.exists('price_in_usd')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_not_exists(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.not_exists('price_in_usd')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

    def test_query_include_reference(self):

        content_type = self.stack_query.content_type('product')
        query = content_type.query()
        query.locale('en-us')
        query.include_reference('categories')
        result, error = query.find()
        if error is None:
            self.assertEqual(7, len(result))

