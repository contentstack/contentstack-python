"""
contentstack
Created by Shailesh Mishra on 13/08/19.
Copyright 2019 Contentstack. All rights reserved.

"""


class contentstack(object):

    """
    Below arguments are needed to initialise stack
    
    Arguments:
        api_key {[type]} -- api_key of your target stack.
        access_token {[type]} -- access token for the stack.
        environment {[type]} -- environment of the stack
        config {[type]} -- (optional) contains configuration of the stack
    
    Returns:
        stack -- stack 

    ==============================

        Example:
            >>> stack = contentstack.stack.Stack("api_key", "access_token", "environment_name")

    ==============================
    """

    @staticmethod
    def stack(**kwargs):
        initstack = stack.Stack(**kwargs)
        return initstack




