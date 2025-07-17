import json
from urllib import parse
from urllib.parse import quote



class Taxonomy:
    def __init__(self, http_instance):
        self.http_instance = http_instance
        self._filters: dict = {}

    def _add(self, field: str, condition: dict) -> "TaxonomyQuery":
        self._filters[field] = condition
        return self

    def in_(self, field: str, terms: list) -> "TaxonomyQuery":
        return self._add(field, {"$in": terms})

    def or_(self, *conds: dict) -> "TaxonomyQuery":
        return self._add("$or", list(conds))

    def and_(self, *conds: dict) -> "TaxonomyQuery":
        return self._add("$and", list(conds))

    def exists(self, field: str) -> "TaxonomyQuery":
        return self._add(field, {"$exists": True})

    def equal_and_below(self, field: str, term_uid: str, levels: int = 10) -> "TaxonomyQuery":
        cond = {"$eq_below": term_uid, "levels": levels}
        return self._add(field, cond)

    def below(self, field: str, term_uid: str, levels: int = 10) -> "TaxonomyQuery":
        cond = {"$below": term_uid, "levels": levels}
        return self._add(field, cond)

    def equal_and_above(self, field: str, term_uid: str, levels: int = 10) -> "TaxonomyQuery":
        cond = {"$eq_above": term_uid, "levels": levels}
        return self._add(field, cond)

    def above(self, field: str, term_uid: str, levels: int = 10) -> "TaxonomyQuery":
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

