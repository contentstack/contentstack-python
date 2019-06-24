"""
   MIT License

   Copyright (c) 2012 - 2019 Contentstack
 
     Permission is hereby granted, free of charge, to any person obtaining a copy
     of this software and associated documentation files (the "Software"), to deal
     in the Software without restriction, including without limitation the rights
     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
     copies of the Software, and to permit persons to whom the Software is
     furnished to do so, subject to the following conditions:

     The above copyright notice and this permission notice shall be included in all
     copies or substantial portions of the Software.
 
     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
     SOFTWARE.
 """
import contentstack
from contentstack.entry import Entry
from contentstack.query import Query


class ContentType(object):

    # _entry_instance: Entry
    # _query_instance: Query
    # _stack_instance: Stack

    def __init__(self, content_type_uid):
        self._stack_instance: contentstack.Stack
        self._entry_instance: Entry
        self._query_instance: Query
        self.content_type_id = content_type_uid
        self.local_header = dict()

    def set_stack_instance(self, _stack= None):
        self.local_header = _stack.local_headers

    def set_header(self, key, value):
        self.local_header[key] = value

    def remove_header(self, header_key):
        if header_key in self.local_header:
            self.local_header.pop(header_key)

    def entry(self, entry_uid: str = None, content_type_id: str = None):

        """
        About: An entry is the actual piece of content created using one of the defined content types.
            Read more about Entries [https://www.contentstack.com/docs/apis/content-delivery-api/#single-entry].
        
        Single Entry: The Get a single entry request fetches a particular entry of a content type.
            [API Reference] : https://www.contentstack.com/docs/apis/content-delivery-api/#single-entry
            Implementation:
            single_entry = stack.content_type('product').entry('entry_uid')
        
        All Entries:
            The Get all entries call fetches the list of all the entries
            of a particular content type. It also returns the content of
            each entry in JSON format. You can also specify the environment
            and locale of which you wish to get the entries.
            [API Reference] : https://www.contentstack.com/docs/apis/content-delivery-api/#entries

        Uses:
            >>>> entry  = self.stack_instance.content_types().entry()
        """
        if content_type_id is not None:
            self.content_type_id = content_type_id
        if entry_uid is not None:
            self._entry_instance.set_uid(entry_uid)

        self._entry_instance = contentstack.Entry(entry_uid=entry_uid, content_type_id=self.content_type_id)
        self._entry_instance.set_content_type_instance(self)
        print('return type', type(self.entry_instance))
        return self._entry_instance

    def query(self) -> Query:

        """
        You can add queries to extend the functionality of this API call. 
        Under the URI Parameters section, insert a parameter named query 
        and provide a query in JSON format as the value.
        To learn more about the queries, refer to the Queries section.
        """

        self._query_instance = Query(self.content_type_id)
        # query.formHead =
        # query.setContentTypeInstance(this)
        print('type', type(self._query_instance))
        return self._query_instance

    def fetch(self):
        pass
