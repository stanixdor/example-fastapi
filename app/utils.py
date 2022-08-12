from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

def Verify(plainPassword, hashedPassword):
    return pwd_context.verify(plainPassword,hashedPassword)