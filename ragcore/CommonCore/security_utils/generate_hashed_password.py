from passlib.context import CryptContext

# Initialize the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_hashed_password(plain_password: str) -> str:
    # Generate the bcrypt hash of the given password
    return pwd_context.hash(plain_password)

# Example usage
plain_password = "POloEON3K61tJ1EJfrJX"
hashed_password = generate_hashed_password(plain_password)

print(f"Plain Password: {plain_password}")
print(f"Hashed Password: {hashed_password}")
