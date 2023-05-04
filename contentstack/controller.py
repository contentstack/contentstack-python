import requests
from requests.utils import guess_json_utf


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
            'error': f"Failed to connect to {url}: {str(e)}",
            'error_code': '400',
            'error_message': {str(e)}
        }
        raise RequestError(error)
    except Exception as e:
        error = {
            'error': f"An unexpected error while making request to {url}, '400', {str(e)}",
            'error_code': '400',
            'error_message': {str(e)}
        }
        raise RequestError(error)
    else:
        return response.json()
