class CommsError(Exception):
    pass

class InvalidCommandError(CommsError):
    pass

class CrcFailureError(CommsError):
    pass

class InvalidIdError(CommsError):
    pass
