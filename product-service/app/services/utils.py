from fastapi import HTTPException, status


def get_404_exception(message: str = "Не найдено!") -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)