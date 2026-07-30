"""
Unit tests for Taxonomy CDA support (contentstack.taxonomy / contentstack.term).

Mocked http_instance, no network calls — mirrors the pattern used in
tests/test_early_fetch.py and contentstack-dotnet's TaxonomyUnitTests.cs
(ported to Python idiom: query params are inspected directly via the
instance's `_query_params` dict rather than via reflection).

Companion to tests/test_taxonomies.py, which covers the legacy entry-filter
queries and the real-API integration/localisation tests.
"""
import pytest
from unittest.mock import MagicMock
from urllib.parse import urlencode

from contentstack.taxonomy import TaxonomyFilter, TaxonomyQuery, Taxonomy
from contentstack.term import Term, TermQuery


ENDPOINT = "https://api.contentstack.io/v3"


@pytest.fixture
def mock_http_instance():
    mock = MagicMock()
    mock.endpoint = ENDPOINT
    mock.headers = {"environment": "test_env"}
    mock.get = MagicMock(side_effect=lambda url: {"url": url})
    return mock


# ---------------------------------------------------------------------------
# The merge boundary — the one behavior the no-breaking-change design hinges on
# ---------------------------------------------------------------------------

class TestMergeBoundary:

    def test_find_with_filter_chained_routes_to_legacy_entries_endpoint(self, mock_http_instance):
        """A filter chained before find() must still hit /taxonomies/entries (unchanged)."""
        tq = TaxonomyQuery(mock_http_instance)
        result = tq.in_("taxonomies.category", ["test"]).find()
        assert "/taxonomies/entries" in result["url"]
        assert "query=" in result["url"]

    def test_find_with_no_filter_routes_to_new_list_endpoint(self, mock_http_instance):
        """No filter chained before find() must hit the new GET /taxonomies list endpoint."""
        tq = TaxonomyQuery(mock_http_instance)
        result = tq.find()
        base = result["url"].split("?")[0]
        assert base == f"{ENDPOINT}/taxonomies"
        assert "/taxonomies/entries" not in result["url"]

    def test_find_with_no_filter_but_query_params_still_routes_to_list_endpoint(self, mock_http_instance):
        result = TaxonomyQuery(mock_http_instance).skip(0).limit(5).include_count().find()
        base = result["url"].split("?")[0]
        assert base == f"{ENDPOINT}/taxonomies"
        assert "skip=0" in result["url"]
        assert "limit=5" in result["url"]
        assert "include_count=true" in result["url"]

    def test_legacy_taxonomy_filter_class_unchanged(self, mock_http_instance):
        """TaxonomyFilter (the renamed original class) behaves byte-for-byte as before."""
        tf = TaxonomyFilter(mock_http_instance)
        result = tf.above("taxonomies.hierarchy", "parent_uid", levels=2).find()
        assert "/taxonomies/entries" in result["url"]
        assert "environment=test_env" in result["url"]


# ---------------------------------------------------------------------------
# TaxonomyQuery — stack.taxonomy() list chainables
# ---------------------------------------------------------------------------

class TestTaxonomyQueryChainables:

    def test_skip_sets_param_and_returns_self(self, mock_http_instance):
        tq = TaxonomyQuery(mock_http_instance)
        result = tq.skip(5)
        assert result is tq
        assert tq._query_params["skip"] == 5

    def test_limit_sets_param_and_returns_self(self, mock_http_instance):
        tq = TaxonomyQuery(mock_http_instance)
        result = tq.limit(10)
        assert result is tq
        assert tq._query_params["limit"] == 10

    def test_include_count_sets_param_and_returns_self(self, mock_http_instance):
        tq = TaxonomyQuery(mock_http_instance)
        result = tq.include_count()
        assert result is tq
        assert tq._query_params["include_count"] == "true"

    def test_combined_chain_sets_all_params_together(self, mock_http_instance):
        tq = TaxonomyQuery(mock_http_instance).skip(0).limit(10).include_count()
        assert tq._query_params == {"skip": 0, "limit": 10, "include_count": "true"}

    def test_param_sets_arbitrary_key(self, mock_http_instance):
        tq = TaxonomyQuery(mock_http_instance)
        result = tq.param("locale", "fr-fr")
        assert result is tq
        assert tq._query_params["locale"] == "fr-fr"

    def test_param_raises_on_none_key_or_value(self, mock_http_instance):
        tq = TaxonomyQuery(mock_http_instance)
        with pytest.raises(KeyError):
            tq.param(None, "value")
        with pytest.raises(KeyError):
            tq.param("key", None)


# ---------------------------------------------------------------------------
# Taxonomy — stack.taxonomy(uid) single taxonomy
# ---------------------------------------------------------------------------

class TestTaxonomy:

    def test_constructor_raises_on_none_uid(self, mock_http_instance):
        with pytest.raises(KeyError):
            Taxonomy(mock_http_instance, None)

    def test_constructor_raises_on_empty_uid(self, mock_http_instance):
        with pytest.raises(KeyError):
            Taxonomy(mock_http_instance, "")

    def test_locale_sets_param_and_returns_self(self, mock_http_instance):
        tax = Taxonomy(mock_http_instance, "regions")
        result = tax.locale("fr-fr")
        assert result is tax
        assert tax._query_params["locale"] == "fr-fr"

    def test_include_fallback_sets_param(self, mock_http_instance):
        tax = Taxonomy(mock_http_instance, "regions")
        tax.include_fallback()
        assert tax._query_params["include_fallback"] == "true"

    def test_include_branch_sets_param(self, mock_http_instance):
        tax = Taxonomy(mock_http_instance, "regions")
        tax.include_branch()
        assert tax._query_params["include_branch"] == "true"

    def test_param_sets_arbitrary_key(self, mock_http_instance):
        tax = Taxonomy(mock_http_instance, "regions")
        tax.param("custom_key", "custom_value")
        assert tax._query_params["custom_key"] == "custom_value"

    def test_param_raises_on_none_key_or_value(self, mock_http_instance):
        tax = Taxonomy(mock_http_instance, "regions")
        with pytest.raises(KeyError):
            tax.param(None, "value")
        with pytest.raises(KeyError):
            tax.param("key", None)

    def test_fetch_builds_correct_url_and_unwraps_taxonomy_key(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"taxonomy": {"uid": "regions"}})
        tax = Taxonomy(mock_http_instance, "regions").locale("fr-fr")
        result = tax.fetch()
        expected_params = urlencode({"locale": "fr-fr"})
        mock_http_instance.get.assert_called_once_with(f"{ENDPOINT}/taxonomies/regions?{expected_params}")
        assert result == {"uid": "regions"}

    def test_fetch_without_params_omits_query_string(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"taxonomy": {"uid": "regions"}})
        Taxonomy(mock_http_instance, "regions").fetch()
        mock_http_instance.get.assert_called_once_with(f"{ENDPOINT}/taxonomies/regions")

    def test_fetch_returns_raw_response_when_taxonomy_key_absent(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"error_code": 404})
        result = Taxonomy(mock_http_instance, "regions").fetch()
        assert result == {"error_code": 404}

    def test_term_without_uid_returns_term_query(self, mock_http_instance):
        tax = Taxonomy(mock_http_instance, "regions")
        assert isinstance(tax.term(), TermQuery)

    def test_term_with_uid_returns_term(self, mock_http_instance):
        tax = Taxonomy(mock_http_instance, "regions")
        assert isinstance(tax.term("california"), Term)


# ---------------------------------------------------------------------------
# Term — stack.taxonomy(uid).term(term_uid)
# ---------------------------------------------------------------------------

class TestTerm:

    def test_constructor_raises_on_none_term_uid(self, mock_http_instance):
        with pytest.raises(KeyError):
            Term(mock_http_instance, "regions", None)

    def test_depth_sets_param_and_returns_self(self, mock_http_instance):
        term = Term(mock_http_instance, "regions", "california")
        result = term.depth(3)
        assert result is term
        assert term._query_params["depth"] == 3

    def test_locale_sets_param(self, mock_http_instance):
        term = Term(mock_http_instance, "regions", "california")
        term.locale("en-us")
        assert term._query_params["locale"] == "en-us"

    def test_include_fallback_sets_param(self, mock_http_instance):
        term = Term(mock_http_instance, "regions", "california")
        term.include_fallback()
        assert term._query_params["include_fallback"] == "true"

    def test_include_branch_sets_param(self, mock_http_instance):
        term = Term(mock_http_instance, "regions", "california")
        term.include_branch()
        assert term._query_params["include_branch"] == "true"

    def test_depth_then_include_branch_chains_both(self, mock_http_instance):
        term = Term(mock_http_instance, "regions", "california").depth(2).include_branch()
        assert term._query_params == {"depth": 2, "include_branch": "true"}

    def test_fetch_builds_correct_url_and_unwraps_term_key(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"term": {"uid": "california"}})
        result = Term(mock_http_instance, "regions", "california").fetch()
        mock_http_instance.get.assert_called_once_with(f"{ENDPOINT}/taxonomies/regions/terms/california")
        assert result == {"uid": "california"}

    def test_locales_hits_locales_suffix_and_unwraps_terms_key(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"terms": [{"uid": "california"}]})
        result = Term(mock_http_instance, "regions", "california").locales()
        mock_http_instance.get.assert_called_once_with(
            f"{ENDPOINT}/taxonomies/regions/terms/california/locales")
        assert result == [{"uid": "california"}]

    def test_ancestors_hits_ancestors_suffix_and_unwraps_terms_key(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"terms": [{"uid": "laptops"}]})
        result = Term(mock_http_instance, "regions", "san-francisco").depth(5).ancestors()
        expected_params = urlencode({"depth": 5})
        mock_http_instance.get.assert_called_once_with(
            f"{ENDPOINT}/taxonomies/regions/terms/san-francisco/ancestors?{expected_params}")
        assert result == [{"uid": "laptops"}]

    def test_descendants_hits_descendants_suffix_and_unwraps_terms_key(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"terms": [{"uid": "gaming_laptops"}]})
        result = Term(mock_http_instance, "electronics", "laptops").descendants()
        mock_http_instance.get.assert_called_once_with(
            f"{ENDPOINT}/taxonomies/electronics/terms/laptops/descendants")
        assert result == [{"uid": "gaming_laptops"}]


# ---------------------------------------------------------------------------
# TermQuery — stack.taxonomy(uid).term()
# ---------------------------------------------------------------------------

class TestTermQuery:

    def test_skip_limit_include_count_depth_include_branch_chain_all_together(self, mock_http_instance):
        tq = TermQuery(mock_http_instance, "regions") \
            .skip(0).limit(10).include_count().depth(2).include_branch()
        assert tq._query_params == {
            "skip": 0, "limit": 10, "include_count": "true",
            "depth": 2, "include_branch": "true",
        }

    def test_locale_sets_param(self, mock_http_instance):
        tq = TermQuery(mock_http_instance, "regions")
        tq.locale("en-us")
        assert tq._query_params["locale"] == "en-us"

    def test_include_fallback_sets_param(self, mock_http_instance):
        tq = TermQuery(mock_http_instance, "regions")
        tq.include_fallback()
        assert tq._query_params["include_fallback"] == "true"

    def test_param_sets_arbitrary_key(self, mock_http_instance):
        tq = TermQuery(mock_http_instance, "regions")
        tq.param("custom_key", "custom_value")
        assert tq._query_params["custom_key"] == "custom_value"

    def test_find_builds_correct_url(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"terms": []})
        TermQuery(mock_http_instance, "regions").locale("en-us").depth(3).find()
        expected_params = urlencode({"locale": "en-us", "depth": 3})
        mock_http_instance.get.assert_called_once_with(
            f"{ENDPOINT}/taxonomies/regions/terms?{expected_params}")

    def test_find_without_params_omits_query_string(self, mock_http_instance):
        mock_http_instance.get = MagicMock(return_value={"terms": []})
        TermQuery(mock_http_instance, "regions").find()
        mock_http_instance.get.assert_called_once_with(f"{ENDPOINT}/taxonomies/regions/terms")
