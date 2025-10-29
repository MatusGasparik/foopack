"""Tests for foopack-core package."""

import pytest


def test_import():
    """Test that foopack_core can be imported."""
    import foopack_core
    assert foopack_core is not None


def test_version():
    """Test that version is defined."""
    import foopack_core
    assert hasattr(foopack_core, "__version__")
    assert isinstance(foopack_core.__version__, str)
    assert len(foopack_core.__version__) > 0


def test_hello_function():
    """Test hello function exists and returns correct value."""
    from foopack_core import hello
    result = hello()
    assert result == "hello from foopack-core"
    assert isinstance(result, str)


def test_dependencies_numpy():
    """Test that numpy dependency is available."""
    import numpy as np
    assert np is not None
    # Basic numpy functionality test
    arr = np.array([1, 2, 3])
    assert arr.sum() == 6


def test_dependencies_xarray():
    """Test that xarray dependency is available."""
    import xarray as xr
    assert xr is not None
    # Basic xarray functionality test
    da = xr.DataArray([1, 2, 3])
    assert da.sum().item() == 6


def test_all_exports():
    """Test that __all__ is properly defined."""
    import foopack_core
    assert hasattr(foopack_core, "__all__")
    assert "hello" in foopack_core.__all__
