from fastapi import status

from errors import AppError

class UserHasNoPermissionError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    error = "USER_HAS_NO_PERMISSION"
    detail = "O usuário requisitado não possui autorização para realizar essa operação."



class UserNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "USER_NOT_FOUND"
    detail = "O usuário requisitado não foi encontrado. Por favor, tente novamente."



class UserAlreadyExistsError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    error = "USER_ALREADY_EXISTS"
    detail = "Os dados fornecidos já pertencem a um usuário. Por favor, faça login ou tente novamente."



class InvalidUserDataError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_USER_DATA"
    detail = "Os dados fornecidos não podem ser utilizados para criar um usuário. Por favor, tente novamente."