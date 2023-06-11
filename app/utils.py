from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto") # Telling pass lib the algo used in hashing password

#hashes user password
def hash (password: str):
    return pwd_context.hash(password)


#function to compare password with hashed password in the db

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

