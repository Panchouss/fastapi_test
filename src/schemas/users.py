from pydantic import BaseModel


class UserLogitSchema(BaseModel):
    username: str
    password: str