import json
from urllib.parse import quote

from contentstack.error_messages import ErrorMessages
from contentstack.utility import Utils


class TaxonomyFilter:
    """
    Taxonomy entry-filter queries ($above, $below, $in, $exists, ...).
    Use stack.taxonomy() to instantiate.

    API Reference: https://www.contentstack.com/docs/developers/apis/content-delivery-api/#taxonomies
    """

    def __init__(self, http_instance):
        self.http_instance = http_instance
        self._filters: dict = {}

    def _add(self, field: str, condition: dict) -> "TaxonomyFilter":
        self._filters[field] = condition
        return self

    def in_(self, field: str, terms: list) -> "TaxonomyFilter":
        return self._add(field, {"$in": terms})

    def or_(self, *conds: dict) -> "TaxonomyFilter":
        return self._add("$or", list(conds))

    def and_(self, *conds: dict) -> "TaxonomyFilter":
        return self._add("$and", list(conds))

    def exists(self, field: str) -> "TaxonomyFilter":
        return self._add(field, {"$exists": True})

    def equal_and_below(self, field: str, term_uid: str, levels: int = 10) -> "TaxonomyFilter":
        cond = {"$eq_below": term_uid, "levels": levels}
        return self._add(field, cond)

    def below(self, field: str, term_uid: str, levels: int = 10) -> "TaxonomyFilter":
        cond = {"$below": term_uid, "levels": levels}
        return self._add(field, cond)

    def equal_and_above(self, field: str, term_uid: str, levels: int = 10) -> "TaxonomyFilter":
        cond = {"$eq_above": term_uid, "levels": levels}
        return self._add(field, cond)

    def above(self, field: str, term_uid: str, levels: int = 10) -> "TaxonomyFilter":
        cond = {"$above": term_uid, "levels": levels}
        return self._add(field, cond)

    def find(self, params=None):
        """
        This method fetches entries filtered by taxonomy from the stack.
        """
        self.local_param = {}
        self.local_param['environment'] = self.http_instance.headers['environment']

        # Ensure query param is always present
        query_string = json.dumps(self._filters or {})
        query_encoded = quote(query_string, safe='{}":,[]')  # preserves JSON characters

        # Build the base URL
        endpoint = self.http_instance.endpoint
        url = f'{endpoint}/taxonomies/entries?environment={self.local_param["environment"]}&query={query_encoded}'

        # Append any additional params manually
        if params:
            other_params = '&'.join(f'{k}={v}' for k, v in params.items())
            url += f'&{other_params}'
        return self.http_instance.get(url)


class TaxonomyQuery(TaxonomyFilter):
    """
    stack.taxonomy() — no uid.

    Chain a filter (in_, or_, and_, exists, above, below, equal_and_above,
    equal_and_below) then call find() to fetch entries filtered by taxonomy
    (unchanged legacy behavior, inherited from TaxonomyFilter).

    Call find() directly with nothing chained to list all published
    taxonomies from the Content Delivery API instead.

    Example::

        >>> import contentstack
        >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
        >>> # Legacy: filter entries by taxonomy
        >>> result = stack.taxonomy().in_('taxonomies.color', ['red']).find()
        >>> # New: list all published taxonomies
        >>> result = stack.taxonomy().limit(10).include_count().find()
    """

    def __init__(self, http_instance):
        super().__init__(http_instance)
        self._query_params = {}

    def skip(self, skip: int) -> "TaxonomyQuery":
        """Sets pagination offset for listing taxonomies.
        :param skip: {int} -- number of taxonomies to skip
        :return: TaxonomyQuery, so you can chain this call.
        """
        self._query_params['skip'] = skip
        return self

    def limit(self, limit: int) -> "TaxonomyQuery":
        """Sets the maximum number of taxonomies to return.
        :param limit: {int} -- max number of taxonomies to return
        :return: TaxonomyQuery, so you can chain this call.
        """
        self._query_params['limit'] = limit
        return self

    def include_count(self) -> "TaxonomyQuery":
        """Includes the total count of taxonomies in the response.
        :return: TaxonomyQuery, so you can chain this call.
        """
        self._query_params['include_count'] = 'true'
        return self

    def param(self, key: str, value) -> "TaxonomyQuery":
        """Adds an arbitrary query parameter to the list-taxonomies request
        (e.g. 'locale').
        :param key: {str} -- query parameter key
        :param value: value for the query parameter
        :return: TaxonomyQuery, so you can chain this call.
        """
        if None in (key, value):
            raise KeyError(ErrorMessages.INVALID_KEY_VALUE_ARGS)
        self._query_params[key] = value
        return self

    def find(self, params=None):
        """
        If a filter was chained (in_/or_/and_/exists/above/below/...), fetches
        entries filtered by taxonomy — unchanged legacy behavior.
        GET /taxonomies/entries?environment=...&query=...

        Otherwise, fetches all published taxonomies from the CDA.
        GET /taxonomies

        :return: dict -- filtered entries, or {'taxonomies': [...], 'count'?: n}
        """
        if self._filters:
            return super().find(params)
        if params:
            self._query_params.update(params)
        url = f'{self.http_instance.endpoint}/taxonomies'
        query_str = Utils.do_url_encode(self._query_params)
        return self.http_instance.get(f'{url}?{query_str}' if query_str else url)


class Taxonomy:
    """
    Represents a single published taxonomy from the Content Delivery API.
    Use stack.taxonomy(uid) to instantiate.

    Example::

        >>> import contentstack
        >>> stack = contentstack.Stack('api_key', 'delivery_token', 'environment')
        >>> taxonomy = stack.taxonomy('regions').locale('fr-fr').include_fallback()
        >>> result = taxonomy.fetch()
    """

    def __init__(self, http_instance, taxonomy_uid: str):
        if not taxonomy_uid:
            raise KeyError(ErrorMessages.INVALID_KEY_OR_VALUE)
        self.http_instance = http_instance
        self._taxonomy_uid = taxonomy_uid
        self._url = f'{http_instance.endpoint}/taxonomies/{taxonomy_uid}'
        self._query_params = {}

    def term(self, term_uid: str = None):
        """
        Without term_uid: returns TermQuery for listing all terms in this taxonomy.
        With term_uid: returns Term for a specific term.

        :param term_uid: {str} -- (optional) unique identifier of the term.
        :return: Term or TermQuery
        """
        from contentstack.term import Term, TermQuery
        if term_uid:
            return Term(self.http_instance, self._taxonomy_uid, term_uid)
        return TermQuery(self.http_instance, self._taxonomy_uid)

    def locale(self, locale: str) -> "Taxonomy":
        """Sets the locale for this taxonomy fetch (e.g. 'en-us', 'fr-fr').
        :param locale: {str} -- locale code
        :return: Taxonomy, so you can chain this call.
        """
        self._query_params['locale'] = locale
        return self

    def include_fallback(self) -> "Taxonomy":
        """Enables locale fallback through the branch hierarchy.
        If the taxonomy is not published in the requested locale, falls back
        to the parent locale in the branch hierarchy.
        :return: Taxonomy, so you can chain this call.
        """
        self._query_params['include_fallback'] = 'true'
        return self

    def include_branch(self) -> "Taxonomy":
        """Includes the _branch field in the response.
        :return: Taxonomy, so you can chain this call.
        """
        self._query_params['include_branch'] = 'true'
        return self

    def param(self, key: str, value) -> "Taxonomy":
        """Adds an arbitrary query parameter.
        :param key: {str} -- query parameter key
        :param value: value for the query parameter
        :return: Taxonomy, so you can chain this call.
        """
        if None in (key, value):
            raise KeyError(ErrorMessages.INVALID_KEY_VALUE_ARGS)
        self._query_params[key] = value
        return self

    def fetch(self) -> dict:
        """
        Fetches this taxonomy from the CDA.
        GET /taxonomies/{taxonomy_uid}

        :return: dict -- the taxonomy object.
        """
        query_str = Utils.do_url_encode(self._query_params)
        url = f'{self._url}?{query_str}' if query_str else self._url
        response = self.http_instance.get(url)
        return response.get('taxonomy', response)
