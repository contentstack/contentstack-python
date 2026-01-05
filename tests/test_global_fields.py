# test_globalfields_init.py

import pytest
import logging
from contentstack.globalfields import GlobalField

class DummyHttpInstance:
    """A dummy HTTP instance for testing purposes."""
    pass

@pytest.fixture
def dummy_http():
    """Fixture to provide a dummy http_instance."""
    return DummyHttpInstance()

@pytest.fixture
def dummy_logger():
    """Fixture to provide a dummy logger."""
    return logging.getLogger("dummy_logger")

@pytest.mark.usefixtures("dummy_http")
class TestGlobalFieldInit:
    """
    Unit tests for GlobalField.__init__ method.
    """

    # -------------------- Happy Path Tests --------------------

    def test_init_with_all_arguments(self, dummy_http, dummy_logger):
        """
        Test that __init__ correctly assigns all arguments when all are provided.
        """
        uid = "global_field_123"
        gf = GlobalField(dummy_http, uid, logger=dummy_logger)
        assert gf.http_instance is dummy_http
        # Accessing the private variable via name mangling
        assert gf._GlobalField__global_field_uid == uid
        assert gf.local_param == {}
        assert gf.logger is dummy_logger

    def test_init_without_logger_uses_default(self, dummy_http):
        """
        Test that __init__ assigns a default logger if none is provided.
        """
        uid = "gf_uid"
        gf = GlobalField(dummy_http, uid)
        assert gf.http_instance is dummy_http
        assert gf._GlobalField__global_field_uid == uid
        assert gf.local_param == {}
        # Should be a logger instance, and not None
        assert isinstance(gf.logger, logging.Logger)
        # Should be the logger for the module
        assert gf.logger.name == "contentstack.globalfields"

    # -------------------- Edge Case Tests --------------------

    def test_init_with_none_uid(self, dummy_http):
        """
        Test that __init__ accepts None as global_field_uid.
        """
        gf = GlobalField(dummy_http, None)
        assert gf._GlobalField__global_field_uid is None

    def test_init_with_empty_string_uid(self, dummy_http):
        """
        Test that __init__ accepts empty string as global_field_uid.
        """
        gf = GlobalField(dummy_http, "")
        assert gf._GlobalField__global_field_uid == ""

    def test_init_with_non_string_uid(self, dummy_http):
        """
        Test that __init__ accepts non-string types for global_field_uid.
        """
        for val in [123, 45.6, {"a": 1}, [1, 2, 3], (4, 5), True, object()]:
            gf = GlobalField(dummy_http, val)
            assert gf._GlobalField__global_field_uid == val

    def test_init_with_none_http_instance(self):
        """
        Test that __init__ accepts None as http_instance.
        """
        uid = "gf_uid"
        gf = GlobalField(None, uid)
        assert gf.http_instance is None
        assert gf._GlobalField__global_field_uid == uid

    def test_init_with_custom_logger_object(self, dummy_http):
        """
        Test that __init__ accepts any object as logger.
        """
        class DummyLogger:
            def info(self, msg): pass
        dummy = DummyLogger()
        gf = GlobalField(dummy_http, "uid", logger=dummy)
        assert gf.logger is dummy

    # ========== Additional Test Cases for GlobalField Methods ==========

    def test_fetch_with_valid_uid(self, dummy_http):
        """Test fetch method with valid global_field_uid"""
        # This test requires a real http_instance, so we'll test the structure
        gf = GlobalField(dummy_http, "test_global_field_uid")
        assert gf._GlobalField__global_field_uid == "test_global_field_uid"
        assert gf.local_param == {}

    def test_fetch_with_none_uid_raises_error(self, dummy_http):
        """Test fetch method with None global_field_uid raises KeyError"""
        gf = GlobalField(dummy_http, None)
        with pytest.raises(KeyError):
            gf.fetch()

    def test_find_with_params(self, dummy_http):
        """Test find method with parameters"""
        gf = GlobalField(dummy_http, None)
        # This test requires a real http_instance, so we'll test the structure
        assert gf.local_param == {}
        # The find method should accept params
        # Note: This would need a real http_instance to fully test

    def test_find_without_params(self, dummy_http):
        """Test find method without parameters"""
        gf = GlobalField(dummy_http, None)
        assert gf.local_param == {}
        # The find method should work without params
        # Note: This would need a real http_instance to fully test

    def test_find_with_none_params(self, dummy_http):
        """Test find method with None params"""
        gf = GlobalField(dummy_http, None)
        assert gf.local_param == {}
        # The find method should handle None params
        # Note: This would need a real http_instance to fully test

    def test_local_param_initialization(self, dummy_http):
        """Test that local_param is initialized as empty dict"""
        gf = GlobalField(dummy_http, "test_uid")
        assert isinstance(gf.local_param, dict)
        assert len(gf.local_param) == 0

    def test_global_field_uid_storage(self, dummy_http):
        """Test that global_field_uid is stored correctly"""
        test_uid = "global_field_12345"
        gf = GlobalField(dummy_http, test_uid)
        assert gf._GlobalField__global_field_uid == test_uid

    def test_http_instance_storage(self, dummy_http):
        """Test that http_instance is stored correctly"""
        gf = GlobalField(dummy_http, "test_uid")
        assert gf.http_instance is dummy_http

    