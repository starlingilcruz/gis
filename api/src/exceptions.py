from fastapi import HTTPException


class PropertyNotFoundException(HTTPException):
    def __init__(self, detail = 'Property not found') -> None:
        super().__init__(404, detail)


class ImageNotFoundException(HTTPException):
    def __init__(self, detail = 'Unable to found property image') -> None:
        super().__init__(500, detail)