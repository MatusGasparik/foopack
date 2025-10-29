"""
Foopack Diagnostics Dashboard

A Panel dashboard showing diagnostic information about the foopack packages
and visualization stack (panel, holoviews, bokeh).
"""

import platform
import sys
from importlib.metadata import version, PackageNotFoundError

import pandas as pd
import panel as pn

# Enable Panel extensions
pn.extension("tabulator")


def get_package_version(package_name: str) -> str:
    """Get version of a package, return 'Not installed' if not found."""
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "Not installed"


def get_package_info() -> list[dict[str, str]]:
    """Collect information about all relevant packages."""
    packages = [
        # Foopack packages
        ("foopack-core", "Core package"),
        ("foopack-extras", "Extras package"),
        ("foopack-ui", "UI package"),
        # Visualization stack
        ("panel", "Panel framework"),
        ("holoviews", "HoloViews"),
        ("bokeh", "Bokeh"),
        # Dependencies
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("xarray", "Xarray"),
    ]

    package_data = []
    for pkg_name, description in packages:
        pkg_version = get_package_version(pkg_name)
        status = "✓" if pkg_version != "Not installed" else "✗"
        package_data.append(
            {
                "Status": status,
                "Package": pkg_name,
                "Version": pkg_version,
                "Description": description,
            }
        )

    return package_data


def get_system_info() -> list[dict[str, str]]:
    """Collect system information."""
    return [
        {"Property": "Python Version", "Value": sys.version.split()[0]},
        {"Property": "Python Implementation", "Value": platform.python_implementation()},
        {"Property": "Platform", "Value": platform.platform()},
        {"Property": "System", "Value": platform.system()},
        {"Property": "Machine", "Value": platform.machine()},
        {"Property": "Processor", "Value": platform.processor() or "Unknown"},
    ]


def test_imports() -> list[dict[str, str]]:
    """Test importing foopack packages and their functions."""
    results = []

    # Test foopack-core
    try:
        import foopack_core

        result = foopack_core.hello()
        results.append(
            {
                "Package": "foopack-core",
                "Test": "Import & call hello()",
                "Result": "✓ Success",
                "Output": result,
            }
        )
    except Exception as e:
        results.append(
            {
                "Package": "foopack-core",
                "Test": "Import & call hello()",
                "Result": "✗ Failed",
                "Output": str(e),
            }
        )

    # Test foopack-extras
    try:
        import foopack_extras

        result = foopack_extras.hello_extras()
        results.append(
            {
                "Package": "foopack-extras",
                "Test": "Import & call hello_extras()",
                "Result": "✓ Success",
                "Output": result,
            }
        )
    except Exception as e:
        results.append(
            {
                "Package": "foopack-extras",
                "Test": "Import & call hello_extras()",
                "Result": "✗ Failed",
                "Output": str(e),
            }
        )

    # Test foopack-ui
    try:
        import foopack_ui

        result = foopack_ui.hello_ui()
        results.append(
            {
                "Package": "foopack-ui",
                "Test": "Import & call hello_ui()",
                "Result": "✓ Success",
                "Output": result,
            }
        )
    except Exception as e:
        results.append(
            {
                "Package": "foopack-ui",
                "Test": "Import & call hello_ui()",
                "Result": "✗ Failed",
                "Output": str(e),
            }
        )

    return results


def create_dashboard():
    """Create the main dashboard layout."""

    # Header
    header = pn.pane.Markdown(
        """
        # 📦 Foopack Diagnostics Dashboard

        Real-time diagnostic information about the foopack package ecosystem.
        """,
        sizing_mode="stretch_width",
    )

    # Package information table
    package_info = get_package_info()
    package_table = pn.widgets.Tabulator(
        pd.DataFrame(package_info),
        sizing_mode="stretch_width",
        height=350,
        configuration={
            "columnDefaults": {"headerSort": False},
        },
        stylesheets=[
            """
            .tabulator-cell {
                font-family: monospace;
            }
            """
        ],
    )

    # System information table
    system_info = get_system_info()
    system_table = pn.widgets.Tabulator(
        pd.DataFrame(system_info),
        sizing_mode="stretch_width",
        height=250,
        show_index=False,
        configuration={
            "columnDefaults": {"headerSort": False},
        },
    )

    # Import tests table
    import_tests = test_imports()
    import_table = pn.widgets.Tabulator(
        pd.DataFrame(import_tests),
        sizing_mode="stretch_width",
        height=200,
        show_index=False,
        configuration={
            "columnDefaults": {"headerSort": False},
        },
    )

    # Refresh button
    def refresh_data(event):
        package_table.value = pd.DataFrame(get_package_info())
        system_table.value = pd.DataFrame(get_system_info())
        import_table.value = pd.DataFrame(test_imports())

    refresh_button = pn.widgets.Button(
        name="🔄 Refresh Data",
        button_type="primary",
        width=150,
        height=40,
    )
    refresh_button.on_click(refresh_data)

    # Layout
    dashboard = pn.template.FastListTemplate(
        title="Foopack Diagnostics",
        sidebar=[
            pn.pane.Markdown("## About"),
            pn.pane.Markdown(
                """
                This dashboard displays diagnostic information about the foopack
                package installation, including:

                - **Package Versions**: All foopack and dependency versions
                - **System Info**: Python and platform details
                - **Import Tests**: Verify packages work correctly

                Click the refresh button to update the data.
                """
            ),
            refresh_button,
        ],
        main=[
            header,
            pn.pane.Markdown("## 📊 Package Versions"),
            package_table,
            pn.pane.Markdown("## 💻 System Information"),
            system_table,
            pn.pane.Markdown("## ✅ Import Tests"),
            import_table,
        ],
        accent_base_color="#00A170",
        header_background="#00A170",
    )

    return dashboard


# Create and serve the dashboard
dashboard = create_dashboard()


# For serving with panel serve
def view():
    """Entry point for panel serve."""
    return dashboard


if __name__ == "__main__":
    # For running with python -m
    dashboard.show()
elif __name__.startswith("bokeh_app"):
    # For panel serve
    dashboard.servable()
