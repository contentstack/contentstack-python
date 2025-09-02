"""
Centralized error messages for the Contentstack Python SDK.
All error messages should be defined here and imported where needed.
"""

class ErrorMessages:
    # BaseQuery errors
    INVALID_KEY = "Invalid key. Provide a valid key and try again."
    INVALID_VALUE = "Invalid value. Provide a valid value and try again."
    INVALID_KEY_OR_VALUE = "Invalid key or value. Provide valid values and try again."

    # ContentType errors
    INVALID_CONTENT_TYPE_UID = "Content type UID is invalid. Provide a valid UID and try again."
    CONTENT_TYPE_UID_REQUIRED = "Content type UID is required. Provide a UID and try again."

    # EntryQueryable errors
    INVALID_FIELD_UID = "Invalid field UID. Provide a valid UID and try again."

    # DeepMergeLp errors
    INVALID_RESPONSE_TYPE = "Invalid input. entry_response and lp_response must be lists of dictionaries. Update the values and try again."

    # Entry errors
    INVALID_ENVIRONMENT = "Invalid environment. Provide a valid environment and try again."
    INVALID_VERSION = "Invalid version. Provide a valid version and try again."
    INVALID_KEY_VALUE_ARGS = "Invalid key or value arguments. Provide valid values and try again."
    REQUESTING_FALLBACK = "Requesting fallback content for the specified locale."
    INVALID_ENTRY_RESPONSE = "Invalid entry_response format. Provide a list of dictionaries, each containing entry data, and try again."
    INVALID_LP_ENTRY = "Invalid lp_entry. Provide a list of dictionaries and try again."
    MISSING_LIVE_PREVIEW_KEYS = "Missing required keys in live preview data. Provide all required keys and try again."

    # Asset errors
    INVALID_UID = "Invalid UID. Provide a valid UID and try again."
    INVALID_PARAMS = "Invalid parameters. Provide valid parameters and try again."

    # Controller errors
    CONNECTION_FAILED = "Connection failed. Unable to connect to {url}. Error: {error}. Check your connection and try again."
    OPERATION_FAILED = "Operation failed. An unexpected error occurred while making request to {url}. Error: {error}. Check your inputs and try again."

    # Query errors
    DEPRECATED_SEARCH = """The search() method is deprecated since version 1.7.0. Use regex() instead.
Example: query.regex("title", "^Blog.*") to search for titles starting with "Blog"."""
    INVALID_JSON = "Invalid JSON. Error: {error}. Provide valid JSON and try again."
    MISSING_ENTRIES_KEY = "Invalid response. The 'entries' key is missing. Include the 'entries' key and try again."
    MISSING_ENTRY_KEY = "Invalid lp_response. The 'entry' key is missing. Include the 'entry' key and try again."

    # Variants errors
    ENTRY_UID_REQUIRED = "Missing entry UID. Provide a valid UID and try again."

    # Stack errors
    INVALID_STACK_UID = "Invalid UID. Provide a valid UID and try again."

    # Utility errors
    INVALID_PARAMS_TYPE = "Invalid params. Provide a dictionary and try again."
    INVALID_URL_PARAMS = "Invalid input. Provide base_url as a string and params as a dictionary, then try again."

    # Stack errors
    INVALID_API_KEY = "Invalid API key. Provide a valid API key and try again."
    INVALID_DELIVERY_TOKEN = "Invalid delivery token. Provide a valid delivery token and try again."
    INVALID_ENVIRONMENT_TOKEN = "Invalid environment. Provide a valid environment and try again."
