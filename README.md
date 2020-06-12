[![Contentstack](https://www.contentstack.com/docs/static/images/contentstack.png)](https://www.contentstack.com/)

<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="99" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="99" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h63v20H0z"/>
        <path fill="#a4a61d" d="M63 0h36v20H63z"/>
        <path fill="url(#b)" d="M0 0h99v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="31.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>
        <text x="31.5" y="14">coverage</text>
        <text x="80" y="15" fill="#010101" fill-opacity=".3">78%</text>
        <text x="80" y="14">78%</text>
    </g>
</svg>

## Python SDK for Contentstack

Contentstack is a headless CMS with an API-first approach. It is a CMS that developers can use to build powerful cross-platform applications in their favorite languages. Build your application frontend, and Contentstack will take care of the rest. [Read More](https://www.contentstack.com/).

Contentstack provides Python SDK to build application on top of Python. Given below is the detailed guide and helpful resources to get started with our Python SDK.

### Prerequisite

You will need python 3 installed on your machine. You can install it from [here](https://www.python.org/ftp/python/3.7.4/python-3.7.4-macosx10.9.pkg).

### Setup and Installation

To use the Contentstack Python SDK to your existing project, perform the steps given below:

**Install contentstack pip**

```
pip install contentstack
```
This is the preferred method to install contentstack, as it will always install the most recent stable release. If you don't have [pip](https://pip.pypa.io/) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process


### Key Concepts for using Contentstack

#### Stack

A stack is like a container that holds the content of your app. Learn more about [Stacks](https://www.contentstack.com/docs/developers/set-up-stack).

#### Content Type

Content type lets you define the structure or blueprint of a page or a section of your digital property. It is a form-like page that gives Content Managers an interface to input and upload content. [Read more](https://www.contentstack.com/docs/developers/create-content-types).

#### Entry

An entry is the actual piece of content created using one of the defined content types. Learn more about [Entries](https://www.contentstack.com/docs/content-managers/work-with-entries).

#### Asset

Assets refer to all the media files (images, videos, PDFs, audio files, and so on) uploaded to Contentstack. These files can be used in multiple entries. Read more about [Assets](https://www.contentstack.com/docs/content-managers/work-with-assets).

#### Environment

A publishing environment corresponds to one or more deployment servers or a content delivery destination where the entries need to be published. Learn how to work with [Environments](https://www.contentstack.com/docs/developers/set-up-environments).



### Contentstack Python SDK: 5-minute Quickstart

#### Initializing your SDK

To initialize the SDK, specify application  API key, access token, and environment name of the stack as shown in the snippet given below (config is optional):

    stack = contentstack.Stack('api_key','delivery_token','environment')


To get the API credentials mentioned above, log in to your Contentstack account and then in your top panel navigation, go to Settings &gt; Stack to view the API Key and Access Token.



#### Querying content from your stack

To retrieve a single entry from a content type use the code snippet given below:

```
stack = contentstack.Stack('api_key','delivery_token','environment')
content_type = stack.content_type("content_type_uid")
entry = content_type.entry("entry_uid")
result = entry.fetch()
```
##### Get Multiple Entries

To retrieve multiple entries of a particular content type, use the code snippet given below:

```
stack = contentstack.Stack('api_key','delivery_token','environment')
query = stack.content_type("content_type_uid").query()
result = query.find()
```


### Advanced Queries

You can query for content types, entries, assets and more using our Java API Reference.

[Python API Reference Doc](https://www.contentstack.com/docs/platforms/python/api-reference/)

### Working with Images

We have introduced Image Delivery APIs that let you retrieve images and then manipulate and optimize them for your digital properties. It lets you perform a host of other actions such as crop, trim, resize, rotate, overlay, and so on.

For example, if you want to crop an image (with width as 300 and height as 400), you simply need to append query parameters at the end of the image URL, such as, https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343/59e0c41ac0eddd140d5a8e3e/download?crop=300,400. There are several more parameters that you can use for your images.

[Read Image Delivery API documentation](https://www.contentstack.com/docs/platforms/python/api-reference/).

You can use the Image Delivery API functions in this SDK as well. Here are a few examples of its usage in the SDK.

```
image = stack.image_transform(url, {'quality': 100}).get_url()
image = stack.image_transform(url, {'width': 100, 'height': 100}).get_url()
image = stack.image_transform(url, {'auto': 'webp'}).get_url()
```

### Using the Sync API with Python SDK

The Sync API takes care of syncing your Contentstack data with your application and ensures that the data is always up-to-date by providing delta updates. Contentstack’s Python SDK supports Sync API, which you can use to build powerful applications.

Read through to understand how to use the Sync API with Contentstack Python SDK.

[Using the Sync API with Python SDK](https://www.contentstack.com/docs/developers/python/using-the-sync-api-with-python-sdk)

### Helpful Links

- [Contentstack Website](https://www.contentstack.com)
- [Official Documentation](https://contentstack.com/docs)
- [Content Delivery API Docs](https://www.contentstack.com/docs/developers/apis/content-delivery-api/)

### The MIT License (MIT)

Copyright © 2012-2019 [Contentstack](https://www.contentstack.com/). All Rights Reserved

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
