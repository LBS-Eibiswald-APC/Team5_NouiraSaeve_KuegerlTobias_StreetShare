from sqlalchemy import inspect, text

from Backend.core.database import SessionLocal, engine
from Backend.crud.user.crud_user import user_crud
from Backend.env_helper import env
from Backend.model.role.role_model import Role
from Backend.model.user.user_model import User


def ensure_schema_updates():
    inspector = inspect(engine)
    transaction_columns = [column["name"] for column in inspector.get_columns("transactions")]

    if "request_id" not in transaction_columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE transactions ADD COLUMN request_id INTEGER NULL"))


def seed_roles_and_admin():
    db = SessionLocal()

    try:
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)

        user_role = db.query(Role).filter(Role.name == "User").first()
        if not user_role:
            user_role = Role(name="User")
            db.add(user_role)
            db.commit()
            db.refresh(user_role)

        admin_email = env("ADMIN_EMAIL", "admin@streetshare.local")
        admin_display_name = env("ADMIN_DISPLAY_NAME", "admin")
        admin_password = env("ADMIN_PASSWORD", "admin123")

        admin_user = db.query(User).filter(
            (User.email == admin_email) | (User.display_name == admin_display_name)
        ).first()

        if not admin_user:
            admin_user = User(
                first_name=env("ADMIN_FIRST_NAME", "Tobias"),
                last_name=env("ADMIN_LAST_NAME", "Kuegerl"),
                display_name=admin_display_name,
                hashed_pw=user_crud.hash_password(admin_password),
                email=admin_email,
                phone=env("ADMIN_PHONE", "+436601333780"),
                street=env("ADMIN_STREET", "Klunkeraberg"),
                house_nr=env("ADMIN_HOUSE_NR", "7"),
                zip=env("ADMIN_ZIP", "8530"),
                city=env("ADMIN_CITY", "Deutschlandsberg"),
                country=env("ADMIN_COUNTRY", "Oesterreich"),
                role_id=admin_role.id,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
        else:
            changed = False

            if admin_user.role_id != admin_role.id:
                admin_user.role_id = admin_role.id
                changed = True

            if admin_email and admin_user.email != admin_email:
                admin_user.email = admin_email
                changed = True

            if admin_display_name and admin_user.display_name != admin_display_name:
                admin_user.display_name = admin_display_name
                changed = True

            if changed:
                db.add(admin_user)
                db.commit()
                db.refresh(admin_user)
    finally:
        db.close()
