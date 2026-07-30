from contentstack.error_messages import ErrorMessages
from contentstack.utility import Utils


class Term:
    """
    Represents a single published taxonomy term.
    Supports hierarchy traversal: ancestors(), descendants(), locales().
    Use stack.taxonomy(uid).term(term_uid) to instantiate.

    Example::

        >>> import contentstack
        >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
        >>> term = stack.taxonomy('regions').term('california')
        >>> result = term.fetch()
    """

    def __init__(self, http_instance, taxonomy_uid: str, term_uid: str):
        if not term_uid:
            raise KeyError(ErrorMessages.INVALID_KEY_OR_VALUE)
        self.http_instance = http_instance
        self._url = f'{http_instance.endpoint}/taxonomies/{taxonomy_uid}/terms/{term_uid}'
        self._query_params = {}

    def depth(self, depth: int) -> "Term":
        """Limits the depth of hierarchy traversal for ancestors()/descendants().
        :param depth: {int} -- maximum hierarchy depth
        :return: Term, so you can chain this call.
        """
        self._query_params['depth'] = depth
        return self

    def locale(self, locale: str) -> "Term":
        """Sets the locale for this term fetch (e.g. 'en-us', 'fr-fr').
        :param locale: {str} -- locale code
        :return: Term, so you can chain this call.
        """
        self._query_params['locale'] = locale
        return self

    def include_fallback(self) -> "Term":
        """Enables locale fallback through the branch hierarchy.
        :return: Term, so you can chain this call.
        """
        self._query_params['include_fallback'] = 'true'
        return self

    def include_branch(self) -> "Term":
        """Includes the _branch field in the response.
        :return: Term, so you can chain this call.
        """
        self._query_params['include_branch'] = 'true'
        return self

    def param(self, key: str, value) -> "Term":
        """Adds an arbitrary query parameter.
        :param key: {str} -- query parameter key
        :param value: value for the query parameter
        :return: Term, so you can chain this call.
        """
        if None in (key, value):
            raise KeyError(ErrorMessages.INVALID_KEY_VALUE_ARGS)
        self._query_params[key] = value
        return self

    def _get(self, suffix: str = '', key: str = None):
        url = f'{self._url}{suffix}'
        query_str = Utils.do_url_encode(self._query_params)
        response = self.http_instance.get(f'{url}?{query_str}' if query_str else url)
        return response.get(key, response) if key else response

    def fetch(self) -> dict:
        """
        Fetches this term.
        GET /taxonomies/{taxonomy_uid}/terms/{term_uid}
        :return: dict -- the term object.
        """
        return self._get(key='term')

    def locales(self) -> dict:
        """
        Fetches all published localized versions of this term.
        GET /taxonomies/{taxonomy_uid}/terms/{term_uid}/locales
        :return: dict -- the localized terms.
        """
        return self._get('/locales', key='terms')

    def ancestors(self) -> list:
        """
        Fetches all ancestor terms up to the root.
        GET /taxonomies/{taxonomy_uid}/terms/{term_uid}/ancestors
        :return: list -- the ancestor terms.
        """
        return self._get('/ancestors', key='terms')

    def descendants(self) -> list:
        """
        Fetches all descendant terms.
        GET /taxonomies/{taxonomy_uid}/terms/{term_uid}/descendants
        :return: list -- the descendant terms.
        """
        return self._get('/descendants', key='terms')


class TermQuery:
    """
    Query builder for fetching all terms in a taxonomy.
    Use stack.taxonomy(uid).term() to instantiate.

    Example::

        >>> import contentstack
        >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
        >>> result = stack.taxonomy('regions').term().locale('en-us').depth(3).find()
    """

    def __init__(self, http_instance, taxonomy_uid: str):
        self.http_instance = http_instance
        self._url = f'{http_instance.endpoint}/taxonomies/{taxonomy_uid}/terms'
        self._query_params = {}

    def depth(self, depth: int) -> "TermQuery":
        """Limits term hierarchy traversal depth.
        :param depth: {int} -- maximum hierarchy depth
        :return: TermQuery, so you can chain this call.
        """
        self._query_params['depth'] = depth
        return self

    def skip(self, skip: int) -> "TermQuery":
        """Sets pagination offset.
        :param skip: {int} -- number of terms to skip
        :return: TermQuery, so you can chain this call.
        """
        self._query_params['skip'] = skip
        return self

    def limit(self, limit: int) -> "TermQuery":
        """Sets the maximum number of terms to return.
        :param limit: {int} -- max number of terms to return
        :return: TermQuery, so you can chain this call.
        """
        self._query_params['limit'] = limit
        return self

    def locale(self, locale: str) -> "TermQuery":
        """Filters terms by locale (e.g. 'en-us', 'fr-fr').
        :param locale: {str} -- locale code
        :return: TermQuery, so you can chain this call.
        """
        self._query_params['locale'] = locale
        return self

    def include_fallback(self) -> "TermQuery":
        """Enables locale fallback through the branch hierarchy.
        :return: TermQuery, so you can chain this call.
        """
        self._query_params['include_fallback'] = 'true'
        return self

    def include_branch(self) -> "TermQuery":
        """Includes the _branch field in the response.
        :return: TermQuery, so you can chain this call.
        """
        self._query_params['include_branch'] = 'true'
        return self

    def include_count(self) -> "TermQuery":
        """Includes the total count of terms in the response.
        :return: TermQuery, so you can chain this call.
        """
        self._query_params['include_count'] = 'true'
        return self

    def param(self, key: str, value) -> "TermQuery":
        """Adds an arbitrary query parameter.
        :param key: {str} -- query parameter key
        :param value: value for the query parameter
        :return: TermQuery, so you can chain this call.
        """
        if None in (key, value):
            raise KeyError(ErrorMessages.INVALID_KEY_VALUE_ARGS)
        self._query_params[key] = value
        return self

    def find(self) -> dict:
        """
        Fetches all terms in the taxonomy.
        GET /taxonomies/{taxonomy_uid}/terms
        :return: dict -- {'terms': [...], 'count'?: n}
        """
        query_str = Utils.do_url_encode(self._query_params)
        return self.http_instance.get(f'{self._url}?{query_str}' if query_str else self._url)
