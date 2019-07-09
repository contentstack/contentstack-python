# contentstack-python
##Python SDK for Contentstack's Content Delivery API





###Advanced Concepts

####Logging
To use the logger, use the standard library logging module:
```
import logging
logging.basicConfig(level=logging.DEBUG)
```
####Proxy example

```html
config = contentstack.Config(
    'blt43745745855',
    '3908457575775',
    proxy_host='127.0.0.1',
    proxy_port=8000,
)
```