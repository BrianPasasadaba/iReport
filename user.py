from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        print("Entered password:", password)
        print("Stored password hash:", self.password_hash)
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def get_by_email(cls, email, mysql):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM admins WHERE email = %s"  # Update table name if needed
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        print("Fetched user:", result)

        if result:
            return cls(result[5], result[6])  # Update column indexes if needed
        else:
            return None

        cursor.close()
