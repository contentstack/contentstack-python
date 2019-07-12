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
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 """


class ContentType:

    def __init__(self, content_type_uid: str):
        if isinstance(content_type_uid, str):
            self.__content_type_uid = content_type_uid
        else:
            raise TypeError('Please provide a valid content_type_uid')
        self.__stack_headers = {}

    @property
    def headers(self):
        return self.__stack_headers

    @headers.setter
    def headers(self, local_headers: dict):
        if local_headers is not None:
            self.__stack_headers = local_headers.copy()

    def header(self, key, value):
        if key is not None and value is not None:
            if isinstance(key, str) and isinstance(value, str):
                self.__stack_headers[key] = value
            return self.__stack_headers

    def remove_header(self, key):
        if key is not None and isinstance(key, str):
            if key in self.__stack_headers:
                self.__stack_headers.pop(key)

    def entry(self, entry_uid: str = None):

        """
        An entry is the actual piece of content created using one of the defined content types.
        Read more about Entries. [ https://www.contentstack.com/docs/apis/content-delivery-api/#entries ]
        The Get all entries call fetches the list of all the entries of a particular content type.
        It also returns the content of each entry in JSON format.
        You can also specify the environment and locale of which you wish to get the entries.
        :param entry_uid: uid for specific entry
        :return: {Entry}

        """
        from contentstack import Entry
        entry: Entry = Entry(content_type_id=self.__content_type_uid)
        entry.headers = self.__stack_headers
        if entry_uid is not None:
            entry.set_uid(entry_uid)

        return entry

    def query(self):

        """
        You can add queries to extend the functionality of this API call. 
        Under the URI Parameters section, insert a parameter named query 
        and provide a query in JSON format as the value.
        To learn more about the queries, refer to the Queries section.
        """
        from contentstack.query import Query
        query = Query(self.__content_type_uid)
        query._headers(self.__stack_headers)
        return query

    def fetch(self) -> tuple:

        global error
        import requests
        import contentstack
        payload: dict = {}

        endpoint = contentstack.config.Config().endpoint('content_types')
        url = '{0}/{1}'.format(endpoint, self.__content_type_uid)
        error = None
        response = requests.get(url, params=payload, headers=self.__stack_headers)
        url = response.url
        print(url, response)
        if response.ok:
            response = response.json()
        else:
            error = response.json()

        return response, error


