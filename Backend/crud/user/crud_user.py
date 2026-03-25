from fastapi import HTTPException, Depends, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from Backend.core.database import get_db
from Backend.crud.base import CRUDBase
from Backend.model.user.user_model import User
from Backend.schemas.user.user_schema import UserRegister, UserUpdate

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "Pcb#o£v3,al(7]OW[5E]6)jI&j()bDy."
ALGORITHM = "HS256"


class CRUDUser(CRUDBase[User, UserRegister, UserUpdate]):
    def create(self, db: Session, obj_in: UserRegister) -> User:
        existing_email = db.query(User).filter(User.email == obj_in.email).first()
        existing_display_name = db.query(User).filter(User.display_name == obj_in.display_name).first()

        errors = {}

        if existing_email:
            errors["email"] = "Diese E-Mail wird bereits verwendet."

        if existing_display_name:
            errors["display_name"] = "Dieser Anzeigename ist bereits vergeben."

        if errors:
            raise HTTPException(status_code=409, detail=errors)

        return super().create(db, obj_in)

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def update_password(self, db: Session, db_user: User, new_password: str):
        db_user.hashed_pw = self.hash_password(new_password)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in.model_dump(exclude_unset=True)

        errors = {}

        new_email = update_data.get("email")
        new_display_name = update_data.get("display_name")

        if new_email and new_email != db_obj.email:
            existing_email = db.query(User).filter(User.email == new_email).first()
            if existing_email:
                errors["email"] = "Diese E-Mail wird bereits verwendet."

        if new_display_name and new_display_name != db_obj.display_name:
            existing_display_name = db.query(User).filter(User.display_name == new_display_name).first()
            if existing_display_name:
                errors["display_name"] = "Dieser Anzeigename ist bereits vergeben."

        if errors:
            raise HTTPException(status_code=409, detail=errors)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
    ):
        token = request.cookies.get("access_token")
        print("COOKIES:", request.cookies)
        print("TOKEN:", token)

        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")

            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")

            user = db.query(User).filter(User.id == int(user_id)).first()

            if user is None:
                raise HTTPException(status_code=401, detail="User not found")

            return user

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")


user_crud = CRUDUser(User)