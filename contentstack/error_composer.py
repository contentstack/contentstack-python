import requests

def make_api_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP error occurred: {http_error}")
        raise
    except requests.exceptions.Timeout as timeout_error:
        print(f"Timeout error occurred: {timeout_error}")
        raise
    except requests.exceptions.ConnectionError as connection_error:
        print(f"Connection error occurred: {connection_error}")
        raise
    except requests.exceptions.RequestException as request_exception:
        print(f"An error occurred: {request_exception}")
        raise
    else:
        print("API request successful")
        return response.json()
    finally:
        print("API request complete")

# Example usage
try:
    api_data = make_api_request("https://jsonplaceholder.typicode.com/posts")
    print(api_data)
except Exception as e:
    print("Caught exception:", e)
