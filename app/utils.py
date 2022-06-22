from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_pasword: str, hashed_password: str):
    return pwd_context.verify(plain_pasword, hashed_password)