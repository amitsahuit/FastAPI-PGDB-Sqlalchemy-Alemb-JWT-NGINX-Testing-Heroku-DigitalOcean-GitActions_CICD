from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verification(plainPass, hashedPassword):
    return pwd_context.verify(plainPass, hashedPassword) 
    """pwd_context.verify has a logic. it will take the plain password, hash it again 
    then the hashed password and the DB hashed password should match. If it does then we are good."""