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

#import requests
from re import sub
import logging
import stack
import json
import time
import sys
import re
import config
from content_type import ContentType
from config import Config
#import urllib.parse



class Stack(object):

    def __init__(self, api_key, access_token, environment, config = None):
        '''
        A stack is a space that stores the content of a project (a web or mobile property). 
        Within a stack, you can create content structures, content entries, users, etc. 
        related to the project. Read more about Stacks 
        API Reference: [https://www.contentstack.com/docs/guide/stack]
        '''
        self.__api_key      = api_key
        self.__access_token = access_token
        self.__environment  = environment
        self.__configs = Config()
        
        ''' initialise stack '''
        self.__initialise_stack()
 


    def __initialise_stack(self):
            if not self.__api_key:
                return AssertionError('Please enter the API key of stack of which you wish to retrieve the content types.')
            if not self.__access_token:
                return AssertionError('Enter the access token of your stack.')
            if not self.__environment:
                return AssertionError('Environment can not be Empty')
            else:
                self.__stack_query__   = dict()
                self.__local_headers__ = dict()
                self.__local_headers__['api_key'] = self.__api_key
                self.__local_headers__['access_token'] = self.__access_token
                self.__local_headers__['environment'] = self.__environment



    def set_config(self, config):
        # need to verifify his method
        self.__configs.set_host(config.get_host())
        self.__configs.set_host(config.get_host())
        self.__configs.set_environment(config.get_environment())
        return self



    def stack(self, api_key):
        if api_key in self.__local_headers__:
            self.__local_headers__ = { "api_key" : api_key}
            return self



    def __get_url(self, url):
        
        VERSION = self.__configs.get_version()
        http_schema = self.__configs.get_host()
        return "/{0}/{1}/{2}".format(http_schema, VERSION, url)



    def content_type(self, content_type_id):

        """Fetches a Content Type by content_type_id.
        Content type defines the structure or schema of a page or a section of your web or mobile property. 
        To create content for your application, you are required to first create a content type. 
        and then create entries using the content type. Read more about Content Types.
        API Reference: https://www.contentstack.com/docs/apis/content-delivery-api/#content-types
        :param content_type_id: The id of the Content Type.
        :return: :class:`ContentType <contentstack.content_type.ContentType>` object.
        :return type: contentstack.content_type.ContentType

        Usage:
            >>> product_content_type = stack.content_type('product__id_goes_here')
        """
        return ContentType(content_type_id)
        #returns content_type instance
        


    def content_types(self):
        """Fetches all Content Types from the Stack.

        This call returns comprehensive information of all the content types available in a particular stack in your account.
        API Reference: https://www.contentful.com/developers/docs/references/content-delivery-api/#/reference/content-types/content-model/get-the-content-model-of-a-space

        :param query: (optional) Dict with API options.
        :return: List of :class:`ContentType <contentful.content_type.ContentType>` objects.
        :rtype: List of contentful.content_type.ContentType

        Usage:
            >>> content_types = stack.content_types()
        """
        return self.__get_url('content_types?include_count=true')
        



    def get_application_key(self):
        ''' get_application_key() returns stack API_Key '''
        if 'api_key' in self.__local_headers__:
            self.__local_headers__['api_key']
            return self
        


    def get_access_token(self):
        ''' get_access_token() method returns access token '''
        if 'access_token' in self.__local_headers__:
            self.__local_headers__['access_token']
            return self


    def remove_header(self, header_key):
        ''' remove_header() method removes existing header by key '''
        if header_key in self.__local_headers__:
            del self.__local_headers__[header_key]
            return self




    def set_header(self, header_key, header_value):
        ''' set_header() mrthod sets additinal headers to the stack '''
        self.__local_headers__[header_key] = header_value
        return self



    def image_transform(self, image_url, transform_params = { }):
        """
        Contentstack is a headless, API-first content management system (CMS) 
        that provides everything you need to power your web or mobile properties. 
        To learn more about Contentstack, visit our website or refer to our 
        documentation site to understand what we do.
        This document is a detailed reference to Contentstack Image Delivery API 
        and covers the parameters that you can add to the URL to retrieve images. 
        The Image Delivery API is used to retrieve, manipulate and/or convert image 
        files of your Contentstack account and deliver it to your web or mobile properties.

        It is an second parameter in which we want to place different manipulation key and value in array form
        ImageTransform function is define for image manipulation with different
        transform_params in second parameter in array form
        
        """
        self.__image_transform_url = image_url
        self.__image_params = transform_params
        return self.__get_image_url()



    def __get_image_url(self):
        counter = len(self.__image_params)
        
        if counter > 0:
            ''' encode url '''
            pass
            #encoded_url = urllib.parse.urlencode(self.__image_params)
            #return self.__get_url(encoded_url)
        else:
            return self.__image_transform_url




    def get_collaborators(self):
        """ 
        collaborators with whom the stacks are shared. 
        A detailed information about each collaborator is returned.
        """
        self.__stack_query__['include_collaborators']=True
        return self



    def get_included_stack_variables(self):
        """
        Stack variables are extra information about the stack, 
        such as the description, format of date, 
        format of time, and so on. Users can include or exclude stack variables in the response. 
        """
        self.__stack_query__['include_stack_variables']=True
        return self



    def get_included_descrete_variables(self):
        """
        view the access token of your stack.
        """
        self.__stack_query__['include_discrete_variables']=True
        return self



    def include_count(self):
        """
        the total count of entries available in a content type.
        """
        self.__stack_query__['include_count']=True
        return self


    def sync_pagination_token(self, pagination_token):
        """
        If the result of the initial sync (or subsequent sync) contains more than 100 records,
        the response would be paginated. It provides pagination token in the response. However,
        you do not have to use the pagination token manually to get the next batch,
        the SDK does that automatically until the sync is complete.
        Pagination token can be used in case you want to fetch only selected batches.
        It is especially useful if the sync process is interrupted midway (due to network issues, etc.).
        In such cases, this token can be used to restart the sync process from where it was interrupted.
        """
        self.__sync_query__ = dict()
        self.__sync_query__['init']=True
        self.__sync_query__['pagination_token']=pagination_token
        return self.__sync_query__



    def sync_token(self, sync_token):
        """
        You can use the sync token (that you receive after initial sync) 
        to get the updated content next time.
        The sync token fetches only the content that was added after your last sync,
        and the details of the content that was deleted or updated.
        """
        self.__sync_query__ = dict()
        self.__sync_query__['init'] =  True
        self.__sync_query__['sync_token'] = sync_token
        return self.__sync_query__
        
 
        
    

    def sync(self, content_type_uid = None, from_date = None, langauge = None, publish_type = None):

        """
        [content_type_uid] --> You can also initialize sync with entries of 
        only specific content_type. To do this, use syncContentType and specify 
        the content type uid as its value. However, if you do this, 
        the subsequent syncs will only include the entries of the specified content_type.

        [from_date] --> You can also initialize sync with entries published 
        after a specific date. To do this, use from_date 
        and specify the start date as its value.

        [locale] --> You can also initialize sync with entries of only specific locales. 
        To do this, use syncLocale and specify the locale code as its value.
        However, if you do this, the subsequent syncs will only include 
        the entries of the specified locales.

        [publish_type] --> Use the type parameter to get a specific type of content. 
        You can pass one of the following values: 
        asset_published, entry_published, asset_unpublished, asset_deleted, entry_unpublished, entry_deleted,  content_type_deleted.
        If you do not specify any value, it will bring all published entries and published assets.
        """
        self.__sync_query__ = dict()
        self.__sync_query__['init'] = True
        if from_date != None:
            self.__sync_query__["start_from"] = from_date 
        if content_type_uid != None:
            self.__sync_query__["content_type_uid"] = content_type_uid
        if publish_type != None:
            self.__sync_query__["type"] = publish_type
        if langauge != None:
            self.__sync_query__["locale"] = langauge

        return self.__sync_query__


    def print_object(self):
        return self.__sync_query__, self.__stack_query__


class StackException(Exception):
    """StackException Class"""
    pass

