

from stack import Stack
from config import Config
from query import Query


configs = Config()
configs.set_host('stag-cdn.contentstack.io')
stack = Stack('blt20962a819b57e233', 'blt01638c90cc28fb6f', 'development', configs)

#stack_config = stack.set_config(configs)
#print('configs host', stack_config.get_host())
stack.sync(content_type_uid='product', from_date='12-03-2021', langauge='in-eu', publish_type='publish')
#sync_params, stack_param = stack.print_object()
#print(sync_params, stack_param, configs.get_host())
content_type = stack.content_type('product')

get_type = type(content_type)
print('return type', get_type)
