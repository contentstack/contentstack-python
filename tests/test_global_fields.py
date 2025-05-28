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

    