import hashlib

def generate_hash(value):
    digest = hashlib.sha1()
    digest.update(value)
    return digest.hexdigest()
