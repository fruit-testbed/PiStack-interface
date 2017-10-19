class CommsError(Exception):
    pass

class InvalidCommandError(CommsError):
    pass

class CrcFailureError(CommsError):
    pass

class InvalidIdError(CommsError):
    pass

class NoResponseError(CommsError):
    pass

class InvalidResponseAddressError(CommsError):
    pass

class InvalidPrefixError(CommsError):
    pass


