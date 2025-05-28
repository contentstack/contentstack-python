"""
Unit tests for GlobalField.fetch method in contentstack.globalfields
"""

import pytest
from unittest.mock import MagicMock
from contentstack.globalfields import GlobalField
from urllib.parse import urlencode


@pytest.fixture
def mock_http_instance():
    """
    Fixture to provide a mock http_instance with required attributes.
    """
    mock = MagicMock()
    mock.endpoint = "https://api.contentstack.io/v3"
    mock.headers = {"environment": "test_env"}
    mock.get = MagicMock(return_value={"global_field": "data"})
    return mock


@pytest.fixture
def global_field_uid():
    """
    Fixture to provide a sample global_field_uid.
    """
    return "sample_uid"


@pytest.fixture
def global_field(mock_http_instance, global_field_uid):
    """
    Fixture to provide a GlobalField instance with a mock http_instance and uid.
    """
    return GlobalField(mock_http_instance, global_field_uid)


class TestGlobalFieldFetch:
    # ------------------- Happy Path Tests -------------------

    def test_fetch_returns_expected_result(self, global_field):
        """
        Test that fetch returns the result from http_instance.get with correct URL and params.
        """
        result = global_field.fetch()
        assert result == {"global_field": "data"}
        assert global_field.local_param["environment"] == "test_env"
        expected_params = urlencode({"environment": "test_env"})
        expected_url = f"https://api.contentstack.io/v3/global_fields/sample_uid?{expected_params}"
        global_field.http_instance.get.assert_called_once_with(expected_url)

    def test_fetch_with_different_environment(self, mock_http_instance, global_field_uid):
        """
        Test fetch with a different environment value in headers.
        """
        mock_http_instance.headers["environment"] = "prod_env"
        gf = GlobalField(mock_http_instance, global_field_uid)
        result = gf.fetch()
        assert result == {"global_field": "data"}
        expected_params = urlencode({"environment": "prod_env"})
        expected_url = f"https://api.contentstack.io/v3/global_fields/sample_uid?{expected_params}"
        mock_http_instance.get.assert_called_once_with(expected_url)

    def test_fetch_preserves_existing_local_param(self, global_field):
        """
        Test that fetch overwrites only the 'environment' key in local_param, preserving others.
        """
        global_field.local_param = {"foo": "bar"}
        result = global_field.fetch()
        assert result == {"global_field": "data"}
        assert global_field.local_param["foo"] == "bar"
        assert global_field.local_param["environment"] == "test_env"
        expected_params = urlencode({"foo": "bar", "environment": "test_env"})
        expected_url = f"https://api.contentstack.io/v3/global_fields/sample_uid?{expected_params}"
        global_field.http_instance.get.assert_called_once_with(expected_url)

    # ------------------- Edge Case Tests -------------------

    def test_fetch_raises_keyerror_when_uid_is_none(self, mock_http_instance):
        """
        Test that fetch raises KeyError if global_field_uid is None.
        """
        gf = GlobalField(mock_http_instance, None)
        with pytest.raises(KeyError, match="global_field_uid can not be None"):
            gf.fetch()

    def test_fetch_raises_keyerror_when_uid_is_explicitly_set_to_none(self, mock_http_instance):
        """
        Test that fetch raises KeyError if global_field_uid is explicitly set to None after init.
        """
        gf = GlobalField(mock_http_instance, "not_none")
        gf._GlobalField__global_field_uid = None  # forcibly set to None
        with pytest.raises(KeyError, match="global_field_uid can not be None"):
            gf.fetch()

    def test_fetch_handles_special_characters_in_params(self, global_field):
        """
        Test that fetch correctly encodes special characters in local_param.
        """
        global_field.local_param = {"foo": "bar baz", "qux": "a&b"}
        result = global_field.fetch()
        assert result == {"global_field": "data"}
        expected_params = urlencode({"foo": "bar baz", "qux": "a&b", "environment": "test_env"})
        expected_url = f"https://api.contentstack.io/v3/global_fields/sample_uid?{expected_params}"
        global_field.http_instance.get.assert_called_once_with(expected_url)

    def test_fetch_raises_keyerror_if_environment_header_missing(self, mock_http_instance, global_field_uid):
        """
        Test that fetch raises KeyError if 'environment' is missing from http_instance.headers.
        """
        del mock_http_instance.headers["environment"]
        gf = GlobalField(mock_http_instance, global_field_uid)
        with pytest.raises(KeyError):
            gf.fetch()

    def test_fetch_propagates_http_instance_get_exception(self, global_field):
        """
        Test that fetch propagates exceptions raised by http_instance.get.
        """
        global_field.http_instance.get.side_effect = RuntimeError("Network error")
        with pytest.raises(RuntimeError, match="Network error"):
            global_field.fetch()

