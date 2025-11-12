import requests
from requests.utils import guess_json_utf
from contentstack.error_messages import ErrorMessages


class RequestError(Exception):
    def __int__(self, error):
        self.error = error['error']
        self.error_code = error['error_code']
        self.error_message = error['error_message']

    pass


def get_request(session, url, headers, timeout):
    try:
        response = session.get(url, verify=True, headers=headers, timeout=timeout)
        if response.encoding is None:
            response.encoding = 'utf-8'
    except requests.exceptions.RequestException as e:
        error = {
            'error': ErrorMessages.CONNECTION_FAILED.format(url=url, error=str(e)),
            'error_code': '400',
            'error_message': {str(e)}
        }
        raise RequestError(error)
    except Exception as e:
        error = {
            'error': ErrorMessages.OPERATION_FAILED.format(url=url, error=str(e)),
            'error_code': '400',
            'error_message': {str(e)}
        }
        raise RequestError(error)
    else:
        return response.json()
