from werkzeug.security import generate_password_hash, check_password_hash

def generate_hash(password):
    return generate_password_hash(password)

def check_hash(password, hashed_password):
    return check_password_hash(hashed_password, password)

if __name__ == "__main__":
    # Example usage
    password = "Admin123"
    hashed_password = generate_hash(password)
    print("Hashed password:", hashed_password)

    # Now let's check if a provided password matches the hashed password
    provided_password = "Admin123"
    is_matched = check_hash(provided_password, hashed_password)

    if is_matched:
        print("Password match!")
    else:
        print("Password does not match.")
