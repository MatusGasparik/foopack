"""Tests for foopack-ui package."""

import pytest


def test_import():
    """Test that foopack_ui can be imported."""
    import foopack_ui

    assert foopack_ui is not None


def test_hello_ui_function():
    """Test hello_ui function exists and returns correct value."""
    from foopack_ui import hello_ui

    result = hello_ui()
    assert result == "hello from foopack-core + ui"
    assert isinstance(result, str)


def test_core_dependency():
    """Test that foopack_core dependency is available."""
    import foopack_core

    assert foopack_core is not None
    # Verify we can call core's hello function
    assert foopack_core.hello() == "hello from foopack-core"


def test_dependencies_panel():
    """Test that panel dependency is available."""
    import panel as pn

    assert pn is not None
    # Basic panel version check
    assert hasattr(pn, "__version__")


def test_dependencies_bokeh():
    """Test that bokeh dependency is available."""
    import bokeh

    assert bokeh is not None
    # Basic bokeh version check
    assert hasattr(bokeh, "__version__")


def test_inherits_core_dependencies():
    """Test that core dependencies (numpy, xarray) are also available."""
    import numpy as np
    import xarray as xr

    assert np is not None
    assert xr is not None
