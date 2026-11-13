from fastapi import status

from errors import AppError

class LogNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "LOG_NOT_FOUND"
    detail = "O registro requisitado não foi encontrado. Por favor, tente novamente."



class InvalidLogTypeError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_LOG_TYPE"
    detail = "O tipo de registro fornecido não existe. Por favor, tente novamente, com os valores \"entry\" ou \"exit\"."



class InvalidLogDateTimeError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_LOG_DATETIME"
    detail = "O dia ou horário fornecidos para a consulta são impossíveis. Por favor, tente novamente."
