"""
Security utilities for password hashing and verification.
"""

import hashlib
import secrets


def generate_salt() -> str:
    """
    Generate a random salt for password hashing.
    
    Returns:
        A random 32-character hexadecimal string
    """
    return secrets.token_hex(16) 


def hash_password(password: str, salt: str) -> str:
    """
    Hash a password using PBKDF2 with the given salt.
 
    Args:
        password: The plain text password
        salt: Random salt string
        
    Returns:
        Hexadecimal string of the hashed password
    """
    iterations = 100000  
    
    # Hash the password
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',              
        password.encode(),     
        salt.encode(),         
        iterations             
    )
    
    return password_hash.hex()


def verify_password(password: str, salt: str, password_hash: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: The plain text password to check
        salt: The salt that was used when hashing
        password_hash: The stored hash to compare against
        
    Returns:
        True if password matches, False otherwise
    """
    computed_hash = hash_password(password, salt)
    
    return computed_hash == password_hash