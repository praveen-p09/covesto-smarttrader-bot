import re

# Validations
def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

def is_valid_mobile(mobile):
    return re.match(r"^\d{10,13}$", mobile)
