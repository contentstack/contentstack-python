[![Contentstack](https://www.contentstack.com/docs/static/images/contentstack.png)](https://www.contentstack.com/)

## WebApp Example for Contentstack-python-sdk

### Prerequisite

You will need python 3 installed on your machine. You can install it from [here](https://www.python.org/ftp/python/3.7.4/python-3.7.4-macosx10.9.pkg).

### Setup and Installation

To use the Contentstack Python SDK to your existing project, perform the steps given below:

*Install pip contentstack*

```
pip contentstack
```

Creating **webapp** using flask and contentstack

Initialise. Flask and contentstack

    flask and contentstack initialisation: 
    >>> pip flask
    >>> pip contentstack
create a directory named contentstack-webapp, create a python file inside name app.py or anything of your liking.

put below structure provided by [flask]([https://palletsprojects.com/p/flask/](https://palletsprojects.com/p/flask/))

    from flask import Flask
    from contentstack import Stack
    
    app = Flask(__name__)

	stack = Stack(api_key='api_key', access_token='access_token', environment='environment')
	query = stack.content_type('content_type_id').query()
	response = query.find()
    
    @app.route('/')
    def hello():
        return 'Hello world'

Run the project by following command:

    $ env FLASK_APP=hello.py flask run
     * Serving Flask app "hello"
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) 



That's It. 

Thank you