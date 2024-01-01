import os, datetime, jwt

access_secret_key = str(os.environ.get("ACCESS_SECRET_KEY"))
refresh_secret_key = str(os.environ.get("REFRESH_SECRET_KEY"))

def generate_access_token(id):
    payload = {
        "id": id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(
        payload,
        access_secret_key,
        algorithm="HS256"
    )


def generate_refresh_token(id):
    payload = {
        "id": id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(
        payload,
        refresh_secret_key,
        algorithm="HS256"
    )


def decode_access_token(token):
    try:
        payload = jwt.decode(token, access_secret_key, algorithms=["HS256"])
        return payload["id"]
    except:
        return None


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, refresh_secret_key, algorithms=["HS256"])
        return payload["id"]
    except:
        return None
