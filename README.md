[![Contentstack](https://www.contentstack.com/docs/static/images/contentstack.png)](https://www.contentstack.com/)

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


### Key Concepts for using Contentstack

#### Stack

A stack is like a container that holds the content of your app. Learn more about [Stacks](https://www.contentstack.com/docs/guide/stack).

#### Content Type

Content type lets you define the structure or blueprint of a page or a section of your digital property. It is a form-like page that gives Content Managers an interface to input and upload content. [Read more](https://www.contentstack.com/docs/guide/content-types).

#### Entry

An entry is the actual piece of content created using one of the defined content types. Learn more about [Entries](https://www.contentstack.com/docs/guide/content-management#working-with-entries).

#### Asset

Assets refer to all the media files (images, videos, PDFs, audio files, and so on) uploaded to Contentstack. These files can be used in multiple entries. Read more about [Assets](https://www.contentstack.com/docs/guide/content-management#working-with-assets).

#### Environment

A publishing environment corresponds to one or more deployment servers or a content delivery destination where the entries need to be published. Learn how to work with [Environments](https://www.contentstack.com/docs/guide/environments).



### Contentstack Python SDK: 5-minute Quickstart

#### Initializing your SDK

To initialize the SDK, specify application  API key, access token, and environment name of the stack as shown in the snippet given below (config is optional):
```
stack = contentstack.Stack(api_key='api_key', access_token='access_token', environment='environment', config=config)
```
To get the API credentials mentioned above, log in to your Contentstack account and then in your top panel navigation, go to Settings &gt; Stack to view the API Key and Access Token.



#### Querying content from your stack

To retrieve a single entry from a content type use the code snippet given below:

```
content_type = stack.content_type("content_type_uid")
entry = content_type.entry("entry_uid")
result = entry.fetch()
```
##### Get Multiple Entries

To retrieve multiple entries of a particular content type, use the code snippet given below:

```
#stack is an instance of Stack class
query = stack.content_type("content_type_uid").query()
result = query.find()
```


### Advanced Queries

You can query for content types, entries, assets and more using our Python API Reference.

[Python API Reference Doc](https://www.contentstack.com/docs/platforms/python/api-reference/)

### Working with Images

We have introduced Image Delivery APIs that let you retrieve images and then manipulate and optimize them for your digital properties. It lets you perform a host of other actions such as crop, trim, resize, rotate, overlay, and so on.

For example, if you want to crop an image (with width as 300 and height as 400), you simply need to append query parameters at the end of the image URL, such as, https://images.contentstack.io/v3/assets/blteae40eb499811073/bltc5064f36b5855343/59e0c41ac0eddd140d5a8e3e/download?crop=300,400. There are several more parameters that you can use for your images.

[Read Image Delivery API documentation](https://www.contentstack.com/docs/apis/image-delivery-api/).

You can use the Image Delivery API functions in this SDK as well. Here are a few examples of its usage in the SDK.

```
#set the image quality to 100
image_params = {'quality': 100}
imageUrl = stack.image_transform(image_url, **image_params);

#resize the image by specifying width and height
image_params = {'width': 100, 'height': 100}
imageUrl = stack.image_transform(imageUrl, **image_params);

#enable auto optimization for the image
image_params = {'auto': 'webp'}
imageUrl = stack.image_transform(imageUrl, **imageParams);
```



### Helpful Links

- [Contentstack Website](https://www.contentstack.com)
- [Official Documentation](https://contentstack.com/docs)
- [Content Delivery API Docs](https://contentstack.com/docs/apis/content-delivery-api/)

