class LumosException(Exception):
    """Base exception for Lumos."""
    pass

class ShadowRootNotFoundError(LumosException):
    """Raised when a shadow root cannot be found."""
    pass

class ElementNotFoundError(LumosException):
    """Raised when an element cannot be found in the shadow DOM."""
    pass
