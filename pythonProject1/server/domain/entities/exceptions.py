from fastapi import HTTPException

ResourceNotFound = HTTPException(404, "Resource not found!")
