class PlaceholderException(Exception):
    """Inherit all custom exceptions we raise from this one.

    We tell our API layer to capture any PlaceholderException exceptions instances.
    Regarding exceptions as control flow in python: https://stackoverflow.com/a/16138864/11014993
    """
