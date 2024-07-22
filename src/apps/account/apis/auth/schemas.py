from typing import List, Optional
from django.contrib.auth.models import User, Group
from ninja import ModelSchema
from ninja.schema import Schema


class LoginSchema(Schema):
    username: str
    password: str


class LoginToken(Schema):
    token: str
    exp: int


class RegisterSchema(Schema):
    username: str
    password: str
    confirm_password: str
    phone: Optional[str] = None
    full_name: Optional[str] = None
    gender: Optional[str] = None


class GroupSchema(ModelSchema):
    class Config:
        model = Group
        model_fields = ['name']


class UserSchema(ModelSchema):
    groups: List[str]

    class Config:
        model = User
        model_fields = ['id', 'username', 'first_name', 'last_name', 'groups']

    @staticmethod
    def resolve_groups(obj: User):
        return [g.full_name for g in obj.groups.all()]
