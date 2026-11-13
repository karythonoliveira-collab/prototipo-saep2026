from fastapi import status

from errors import AppError

class ProductNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "PRODUCT_NOT_FOUND"
    detail = "O produto requisitado não foi encontrado. Por favor, tente novamente."



class InvalidProductValueError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_PRODUCT_VALUE"
    detail = "O valor fornecido para o produto é impossível. Por favor, tente novamente."



class InvalidQueryError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_QUERY"
    detail = "Os parâmetros passados não podem retornar nenhum resultado como estão. Por favor, tente novamente."



class InvalidProductQuantityError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_PRODUCT_QUANTITY"
    detail = "A quantidade fornecida para o produto é impossível. Por favor, tente novamente."