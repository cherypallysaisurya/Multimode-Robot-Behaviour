"""Hardware integration layer.

This package deliberately keeps only minimal re-exports so core users
aren't forced to import heavy dependencies unless they opt into
hardware (real robot) features via extras.
"""
try:
    from go1_py import Dog, Mode  # type: ignore
    __all__ = ['Dog', 'Mode']
except Exception:  # pragma: no cover
    # Not installed; hardware extras not available
    Dog = object  # type: ignore
    Mode = object  # type: ignore
    __all__ = []
