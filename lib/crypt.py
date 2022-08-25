import bcrypt


class Crypt:
    _salt = bcrypt.gensalt()

    @staticmethod
    def hash(raw_value):
        return bcrypt.hashpw(raw_value.encode('utf-8'), Crypt._salt).decode('utf-8')
    
    @staticmethod
    def compare(raw_value, hashed_value):
        return bcrypt.checkpw(raw_value.encode('utf-8'), hashed_value.encode('utf-8'))
    