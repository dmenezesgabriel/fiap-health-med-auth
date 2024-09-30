class UserAlreadyExistsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class UserNotConfirmedException(Exception):
    pass


class UserAlreadyConfirmed(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class ExpiredVerificationCodeException(Exception):
    pass


class InvalidVerificationCodeException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class RequirementsDoesNotMatchException(Exception):
    pass
