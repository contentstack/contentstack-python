"""
contentstack
Created by Shailesh Mishra on 13/08/19.
Copyright 2019 Contentstack. All rights reserved.

"""
import stack


class contentstack(object):

    """
    :param api_key: api_key of your target stack.
    :param access_token: access token for the stack.
    :param environment: environment of the stack
    :param config: (optional) contains configuration of the stack
    """

    @staticmethod
    def stack(**kwargs):
        initstack = stack.Stack(**kwargs)
        return initstack




