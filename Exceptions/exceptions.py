class InvalidLicensePlateError(Exception):
    pass


class InvalidMileageError(Exception):
    pass


class InvalidDateError(Exception):
    pass


class DuplicateLicensePlateError(Exception):
    pass


class InvalidIDError(Exception):
    pass


class DuplicateIDError(Exception):
    pass


class InvalidAgeError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class VehicleNotFoundError(Exception):
    pass


class ClientAlreadyHasVehicleError(Exception):
    pass


class InvalidRoleError(Exception):
    pass


class UnauthorizedActionError(Exception):
    pass


class InvalidRentalPeriodError(Exception):
    pass


class RentalAlreadyFinishedError(Exception):
    pass


class RentalNotFoundError(Exception):
    pass


class KmsExceededError(Exception):
    pass


class InvalidKmsAllowedError(Exception):
    pass


class VehicleAlreadyRentedError(Exception):
    pass