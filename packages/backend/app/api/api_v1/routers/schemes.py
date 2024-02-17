from pydantic import BaseModel


## ----- for the auth router -----


class LoginData(BaseModel):
    email: str
    password: str


class SignUpData(LoginData):
    name: str
