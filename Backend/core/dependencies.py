from fastapi import Depends, HTTPException
from Backend.crud.user.crud_user import user_crud

def require_role(allowed_roles: list[str]):
    def role_checker(user=Depends(user_crud.get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Nicht erlaubt")
        return user
    return role_checker