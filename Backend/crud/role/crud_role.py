from sqlalchemy.orm import Session
from Backend.crud.base import CRUDBase
from Backend.model.role.role_model import Role
from Backend.schemas.role.role_schema import RoleCreate, RoleUpdate


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):

    def get_by_name(self, db: Session, name: str):
        return db.query(Role).filter(Role.name == name).first()


role_crud = CRUDRole(Role)
