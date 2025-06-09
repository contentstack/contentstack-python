# test_globalfields_find.py

import pytest
from unittest.mock import MagicMock, patch
from contentstack.globalfields import GlobalField

@pytest.fixture
def mock_http_instance():
    """
    Fixture to provide a mock http_instance with headers and endpoint.
    """
    mock = MagicMock()
    mock.headers = {"environment": "test_env"}
    mock.endpoint = "https://api.contentstack.io/v3"
    mock.get = MagicMock(return_value={"global_fields": "data"})
    return mock

@pytest.fixture
def global_field_uid():
    """
    Fixture to provide a sample global_field_uid.
    """
    return "sample_uid"

class TestGlobalFieldFind:
    """
    Unit tests for GlobalField.find method, covering happy paths and edge cases.
    """

    # -------------------- Happy Path Tests --------------------

    def test_find_with_no_params(self, mock_http_instance, global_field_uid):
        """
        Test that find() with no params returns expected result and constructs correct URL.
        """
        gf = GlobalField(mock_http_instance, global_field_uid)
        result = gf.find()
        assert result == {"global_fields": "data"}
        expected_url = (
            "https://api.contentstack.io/v3/global_fields?environment=test_env"
        )
        mock_http_instance.get.assert_called_once_with(expected_url)

    def test_find_with_params(self, mock_http_instance, global_field_uid):
        """
        Test that find() with additional params merges them and encodes URL correctly.
        """
        gf = GlobalField(mock_http_instance, global_field_uid)
        params = {"limit": 10, "skip": 5}
        result = gf.find(params=params)
        # The order of query params in the URL is not guaranteed, so check both possibilities
        called_url = mock_http_instance.get.call_args[0][0]
        assert result == {"global_fields": "data"}
        assert called_url.startswith("https://api.contentstack.io/v3/global_fields?")
        # All params must be present in the URL
        for k, v in {"environment": "test_env", "limit": "10", "skip": "5"}.items():
            assert f"{k}={v}" in called_url

    def test_find_with_empty_params_dict(self, mock_http_instance, global_field_uid):
        """
        Test that find() with an empty params dict behaves like no params.
        """
        gf = GlobalField(mock_http_instance, global_field_uid)
        result = gf.find(params={})
        assert result == {"global_fields": "data"}
        expected_url = (
            "https://api.contentstack.io/v3/global_fields?environment=test_env"
        )
        mock_http_instance.get.assert_called_once_with(expected_url)

   

    def test_find_with_special_characters_in_params(self, mock_http_instance, global_field_uid):
        """
        Test that find() correctly URL-encodes special characters in params.
        """
        gf = GlobalField(mock_http_instance, global_field_uid)
        params = {"q": "name:foo/bar&baz", "limit": 1}
        result = gf.find(params=params)
        called_url = mock_http_instance.get.call_args[0][0]
        # Check that special characters are URL-encoded
        assert "q=name%3Afoo%2Fbar%26baz" in called_url
        assert "limit=1" in called_url
        assert result == {"global_fields": "data"}

    def test_find_with_none_environment_in_headers(self, mock_http_instance, global_field_uid):
        """
        Test that find() handles the case where 'environment' in headers is None.
        """
        mock_http_instance.headers["environment"] = None
        gf = GlobalField(mock_http_instance, global_field_uid)
        result = gf.find()
        called_url = mock_http_instance.get.call_args[0][0]
        # Should include 'environment=None' in the query string
        assert "environment=None" in called_url
        assert result == {"global_fields": "data"}

    def test_find_with_non_string_param_values(self, mock_http_instance, global_field_uid):
        """
        Test that find() handles non-string param values (e.g., int, bool, None).
        """
        gf = GlobalField(mock_http_instance, global_field_uid)
        params = {"int_val": 42, "bool_val": True, "none_val": None}
        result = gf.find(params=params)
        called_url = mock_http_instance.get.call_args[0][0]
        # int and bool should be stringified, None should be 'None'
        assert "int_val=42" in called_url
        assert "bool_val=True" in called_url
        assert "none_val=None" in called_url
        assert result == {"global_fields": "data"}

    def test_find_with_empty_headers(self, global_field_uid):
        """
        Test that find() raises KeyError if 'environment' is missing from headers.
        """
        mock_http_instance = MagicMock()
        mock_http_instance.headers = {}
        mock_http_instance.endpoint = "https://api.contentstack.io/v3"
        mock_http_instance.get = MagicMock(return_value={"global_fields": "data"})
        gf = GlobalField(mock_http_instance, global_field_uid)
        with pytest.raises(KeyError):
            gf.find()


    def test_find_with_mutable_local_param(self, mock_http_instance, global_field_uid):
        """
        Test that local_param is updated and persists between calls.
        """
        gf = GlobalField(mock_http_instance, global_field_uid)
        # First call with a param
        gf.find(params={"foo": "bar"})
        # Second call with a different param
        gf.find(params={"baz": "qux"})
        # local_param should have been updated with the last call's params
        assert gf.local_param["baz"] == "qux"
        assert gf.local_param["environment"] == "test_env"
        # The previous param 'foo' should still be present (since update is cumulative)
        assert gf.local_param["foo"] == "bar"