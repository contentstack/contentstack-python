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
import logging
import entry
from config import Config
from query import Query


class ContentType(object):
    
    def __init__(self, content_type_uid):
        self.content_type_id = content_type_uid
        self.__get_url('content_types/{0}'.format(self.content_type_id))
        self.local_header = dict()

    
    def set_stack_instance(self, stack):
        self.stack_instance = stack
        self.local_header   = stack.local_header
    
    
    def set_header(self, key, value):
        """
        Scope is limited to this object and followed classes. 
        """
        self.local_header.update({key: value})


    def remove_header(self, header_key):
        if header_key in self.local_header:
            self.local_header.pop(header_key)
    

    def entry(self, entry_uid = None): 
        entry = entry.Entry(self.content_type_id)
        entry.set_content_type_instance(self)
        if entry_uid != None:
            entry.set_uid(entry_uid)
        return entry
    

    def query(self):
        query =  query.Query(self.content_type_id)
        #query.formHead = 
        #query.setContentTypeInstance(this)
        return query


    def fetch(self, callback):
        
        return self.__get_url(self.content_type_id)
        



    def __get_url(self, url):
        self.__configs = Config()
        VERSION = self.__configs.get_version()
        http_schema = self.__configs.get_host()
        return "/{0}/{1}/content_types/{2}".format(http_schema, VERSION, url)
