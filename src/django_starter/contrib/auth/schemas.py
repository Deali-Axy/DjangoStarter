from ninja import Schema

class LoginToken(Schema):
    token: str
    exp: int
