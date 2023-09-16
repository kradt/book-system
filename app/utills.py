from fastapi import HTTPException, status


def is_exist(obj, status_code: status = status.HTTP_404_NOT_FOUND, detail: str | None = None) -> bool | None:
    """
        Return True if obj is exist and raise an error when obj is not exist
    """
    if not obj:
        raise HTTPException(status_code=status_code, detail=detail)
    return True