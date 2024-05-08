from app.components import load_component_library, BaseComponent


class BaseCredential(BaseComponent):
    category: str = "Credentials"


INPUT_TYPES = [
    "boolean",
    "string",
    "password",
    "number",
    "json",
    "oauth",
    "options",
]


all_credentials = load_component_library("credentials")
