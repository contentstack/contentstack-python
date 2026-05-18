"""
Unit tests for Variants branch support in contentstack.variants
"""

import pytest
from unittest.mock import MagicMock
from urllib.parse import urlencode

from contentstack.variants import Variants


@pytest.fixture
def mock_http_instance():
    mock = MagicMock()
    mock.endpoint = "https://cdn.contentstack.io/v3"
    mock.headers = {
        "api_key": "api_key",
        "access_token": "delivery_token",
        "environment": "test_env",
    }
    mock.get = MagicMock(return_value={"entries": []})
    return mock


@pytest.fixture
def variants(mock_http_instance):
    return Variants(
        http_instance=mock_http_instance,
        content_type_uid="faq",
        entry_uid="entry_uid",
        variant_uid="variant_uid",
    )


def _capture_headers_on_get(mock_http_instance):
    captured = {}

    def _get(url):
        captured["headers"] = mock_http_instance.headers.copy()
        return {"entries": []}

    mock_http_instance.get.side_effect = _get
    return captured


class TestVariantsBranch:
    def test_fetch_sets_variant_and_branch_headers(self, mock_http_instance):
        captured = _capture_headers_on_get(mock_http_instance)
        variants = Variants(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid="entry_uid",
            variant_uid="variant_uid",
            branch="dev_branch",
        )
        variants.fetch()

        assert captured["headers"]["x-cs-variant-uid"] == "variant_uid"
        assert captured["headers"]["branch"] == "dev_branch"

    def test_fetch_multiple_variant_uids_with_branch(self, mock_http_instance):
        captured = _capture_headers_on_get(mock_http_instance)
        variants = Variants(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid="entry_uid",
            variant_uid=["variant1", "variant2"],
            branch="dev_branch",
        )
        variants.fetch()

        assert captured["headers"]["x-cs-variant-uid"] == "variant1,variant2"
        assert captured["headers"]["branch"] == "dev_branch"

    def test_find_sets_variant_and_branch_headers(self, mock_http_instance):
        captured = _capture_headers_on_get(mock_http_instance)
        variants = Variants(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid=None,
            variant_uid="variant_uid",
            branch="dev_branch",
        )
        variants.find()

        assert captured["headers"]["x-cs-variant-uid"] == "variant_uid"
        assert captured["headers"]["branch"] == "dev_branch"

    def test_fetch_restores_stack_branch_after_request(self, mock_http_instance):
        mock_http_instance.headers["branch"] = "main"
        variants = Variants(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid="entry_uid",
            variant_uid="variant_uid",
            branch="dev_branch",
        )
        variants.fetch()

        assert "x-cs-variant-uid" not in mock_http_instance.headers
        assert mock_http_instance.headers["branch"] == "main"

    def test_fetch_removes_branch_when_stack_had_none(self, mock_http_instance):
        variants = Variants(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid="entry_uid",
            variant_uid="variant_uid",
            branch="dev_branch",
        )
        variants.fetch()

        assert "branch" not in mock_http_instance.headers
        assert "x-cs-variant-uid" not in mock_http_instance.headers

    def test_fetch_without_branch_uses_stack_branch(self, mock_http_instance):
        mock_http_instance.headers["branch"] = "main"
        variants = Variants(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid="entry_uid",
            variant_uid="variant_uid",
        )
        variants.fetch()

        assert mock_http_instance.headers["branch"] == "main"
        assert "x-cs-variant-uid" not in mock_http_instance.headers

    def test_fetch_cleans_up_variant_header_only(self, variants, mock_http_instance):
        variants.fetch()

        assert "x-cs-variant-uid" not in mock_http_instance.headers
        assert mock_http_instance.headers["environment"] == "test_env"

    def test_fetch_builds_expected_url(self, variants, mock_http_instance):
        variants.fetch()
        expected_url = (
            "https://cdn.contentstack.io/v3/content_types/faq/entries/entry_uid?"
        )
        mock_http_instance.get.assert_called_once()
        assert mock_http_instance.get.call_args[0][0].startswith(expected_url)

    def test_find_builds_expected_url(self, mock_http_instance):
        variants = Variants(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid=None,
            variant_uid="variant_uid",
            branch="dev_branch",
        )
        variants.find(params={"locale": "en-us"})
        expected_params = urlencode({"locale": "en-us"})
        expected_url = (
            f"https://cdn.contentstack.io/v3/content_types/faq/entries?{expected_params}"
        )
        mock_http_instance.get.assert_called_once_with(expected_url)

    def test_entry_variants_passes_branch(self, mock_http_instance):
        from contentstack.entry import Entry

        entry = Entry(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid="entry_uid",
        )
        result = entry.variants("variant_uid", "dev_branch")
        assert isinstance(result, Variants)
        assert result.branch == "dev_branch"
        assert result.variant_uid == "variant_uid"

    def test_content_type_variants_passes_branch(self, mock_http_instance):
        from contentstack.contenttype import ContentType

        content_type = ContentType(mock_http_instance, "faq")
        result = content_type.variants(["variant1", "variant2"], "dev_branch")
        assert isinstance(result, Variants)
        assert result.branch == "dev_branch"
        assert result.variant_uid == ["variant1", "variant2"]

    def test_variants_backward_compatible_params_kwarg(self, mock_http_instance):
        from contentstack.entry import Entry

        entry = Entry(
            http_instance=mock_http_instance,
            content_type_uid="faq",
            entry_uid="entry_uid",
        )
        result = entry.variants("variant_uid", params={"locale": "en-us"})
        assert result.branch is None
        assert result.entry_param == {"locale": "en-us"}
