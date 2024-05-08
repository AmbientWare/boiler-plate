from pydantic import BaseModel
from typing import List, Optional, Dict, Any

## ----- general schemes -----


class ComponentData(BaseModel):
    label: str = ""
    name: str = ""
    category: str = ""
    credential: Optional[int] = None
    description: Optional[str] = ""
    icon: Optional[str] = ""
    inputs: Dict[str, Any] = {}
    inputParams: Optional[List[dict]] = []
    provider: Optional[str] = ""
    metadata: Optional[dict] = {}


## ----- for the auth router -----


class LoginData(BaseModel):
    email: str
    password: str


class SignUpData(LoginData):
    name: str


## ----- for the credential routers -----


class CreateCredentialData(BaseModel):
    name: str
    credentialName: str
    credentialObj: dict


class UpdateCredentialData(BaseModel):
    name: str
    credentialName: str
    credentialObj: dict
