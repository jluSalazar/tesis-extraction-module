class ExtractionException(Exception):
    """Clase base para excepciones del dominio de extracción."""
    pass

class ExtractionValidationError(ExtractionException):
    """Error cuando una regla de negocio de validación falla."""
    pass

class ExtractionNotFound(ExtractionException):
    """Error cuando no se encuentra el recurso."""
    pass

class UnauthorizedExtractionAccess(ExtractionException):
    """Error de permisos a nivel de dominio."""
    pass