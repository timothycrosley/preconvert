"""Defines all exceptions that can be thrown by the preconvert project"""


class Error(Exception):
    """Base class for exceptions thrown from the preconvert project"""

    pass


class ExistingConverter(Error):
    """Should be raised when a converter already exists for a specified type"""

    def __init__(self, kind, existing, new):
        super().__init__(
            self,
            (
                "A new converter ({new}) is being registered for {kind} "
                "but an existing one exists already exists: {existing}. "
                "If intended, use override=True"
            ).format(kind=kind, existing=existing, new=new),
        )

        self.kind = kind
        self.existing = existing
        self.new = new


class Unconvertable(Error):
    """Raised when the provided item is not convertable using the provided converter(s)"""

    def __init__(self, item):
        super().__init__(
            self,
            "Object of type {} is not convertible " "into a serializable type".format(type(item)),
        )
        self.item = item
