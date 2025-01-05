from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(passw: str) -> str:
    return pwd_context.hash(passw)


def verify_password(plain_password: str, hashed_passw: str) -> bool:
    return pwd_context.verify(plain_password, hashed_passw)





