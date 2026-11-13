from fastapi import status

class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = "APP_ERROR"
    detail = "Um erro inesperado ocorreu no servidor. Por favor, tente novamente."