from fastapi import Depends
from fastapi import HTTPException

from src.auth.dependencies import get_current_user
from src.auth.permissions import has_permission

def require_permission(
        resource: str,
        action: str
):
    def checker(
            current_user=Depends(
                get_current_user
            )
    ):
        if not has_permission(
                current_user,
                resource,
                action
        ):
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        return current_user

    return checker