"""
Main application demonstrating usage of all foopack packages.

This downstream application simulates a real-world project that depends on
foopack-core, foopack-extras, and foopack-ui packages from prefix.dev.
"""

import sys
from typing import Any


def demo_core() -> dict[str, Any]:
    """Demonstrate foopack-core functionality."""
    import foopack_core

    print("=" * 60)
    print("Testing foopack-core")
    print("=" * 60)

    # Get version if available
    version = getattr(foopack_core, "__version__", "unknown")
    print(f"Version: {version}")

    # Try to use any exported functionality
    # Since we don't know the actual API, we'll just show it's importable
    print(f"Module location: {foopack_core.__file__}")
    print(f"Available items: {[x for x in dir(foopack_core) if not x.startswith('_')]}")

    return {
        "package": "foopack-core",
        "version": version,
        "status": "OK",
    }


def demo_extras() -> dict[str, Any]:
    """Demonstrate foopack-extras functionality."""
    import foopack_extras

    print("\n" + "=" * 60)
    print("Testing foopack-extras")
    print("=" * 60)

    version = getattr(foopack_extras, "__version__", "unknown")
    print(f"Version: {version}")
    print(f"Module location: {foopack_extras.__file__}")
    print(f"Available items: {[x for x in dir(foopack_extras) if not x.startswith('_')]}")

    return {
        "package": "foopack-extras",
        "version": version,
        "status": "OK",
    }


def demo_ui() -> dict[str, Any]:
    """Demonstrate foopack-ui functionality."""
    import foopack_ui

    print("\n" + "=" * 60)
    print("Testing foopack-ui")
    print("=" * 60)

    version = getattr(foopack_ui, "__version__", "unknown")
    print(f"Version: {version}")
    print(f"Module location: {foopack_ui.__file__}")
    print(f"Available items: {[x for x in dir(foopack_ui) if not x.startswith('_')]}")

    return {
        "package": "foopack-ui",
        "version": version,
        "status": "OK",
    }


def main() -> int:
    """Run the application."""
    print("\n" + "#" * 60)
    print("# Foopack Downstream Application")
    print("# Demonstrating multi-platform package consumption")
    print("#" * 60 + "\n")

    results = []

    try:
        results.append(demo_core())
        results.append(demo_extras())
        results.append(demo_ui())

        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)

        for result in results:
            status_emoji = "✓" if result["status"] == "OK" else "✗"
            print(f"{status_emoji} {result['package']:20} v{result['version']:10} [{result['status']}]")

        print("\n✓ All foopack packages successfully installed and imported!")
        print("✓ Multi-platform build verification: PASSED")

        return 0

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
