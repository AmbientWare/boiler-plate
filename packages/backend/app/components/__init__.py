from typing import List, Optional, Union
import os
import importlib
import sys
import inspect
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from importlib import resources


from app.api.api_v1.routers.schemes import ComponentData
from app.db.session import get_db


# access icon resources with package
def get_icon_path(icon_name: str) -> str:
    return str(resources.files("app.components.icons").joinpath(icon_name))


input_types = Union[
    str,
    int,
    dict,
    list,
    bool,
]


class ComponentInput(BaseModel):
    label: str
    name: str
    type: str
    value: input_types = ""
    default: Optional[str] = ""
    warning: Optional[str] = ""
    options: Optional[List[dict]] = []
    description: Optional[str] = ""
    optional: Optional[bool] = False
    fileType: Optional[str] = ""
    credentialNames: Optional[List[str]] = []


class BaseComponent(BaseModel):
    label: str
    name: str
    category: str
    description: Optional[str] = ""
    icon: Optional[str] = ""
    inputs: List[ComponentInput] = []
    metadata: Optional[dict] = {}

    # entities that are not returned to the client
    _db: Session = Depends(get_db)

    def load(self, componentData: ComponentData, db: Optional[Session] = None):
        """Base load method for all common components types. should be modified in the BASE component class."""
        raise NotImplementedError("load method must be implemented in child class")

    def _load(self, componentData: ComponentData, db: Optional[Session] = None):
        """Load data into document objects. should be modified by all child slasses of the common component."""
        raise NotImplementedError("load method must be implemented in child class")

    def run(self, input: str):
        """Run the component."""
        return "Not implemented"


def load_component_library(component_dir: str):
    """this immported into other modules to get all the components in the directory it is called from."""
    # get the current module
    current_module = sys.modules[__name__]
    # get the current file path
    current_file = inspect.getfile(current_module)
    # get the current file directory
    current_dir = os.path.dirname(current_file)
    current_dir = os.path.join(current_dir, component_dir)

    # get all the files in the current directory
    files = os.listdir(current_dir)
    # get the files that are credential files
    component_files = [
        file for file in files if file.endswith(".py") and file != "__init__.py"
    ]
    # import the initialized credentials from the files
    components = {}
    for file in component_files:
        module_name = class_name = file.replace(".py", "")
        # import the module
        module = importlib.import_module(f"{__name__}.{component_dir}.{module_name}")
        # get the class from the module
        cls = getattr(module, class_name)
        # add the class to the credentials
        components[module_name] = cls

    return components


component_types = [
    "data_loaders",
]

all_components = {}
components_by_type = {}
for component_type in component_types:
    # this is a dictionary of components { name: component }
    typeDict = load_component_library(component_type)
    all_components.update(typeDict)

    # this is a dictionary of dictionaries { type: { name: component } }
    components_by_type[component_type] = typeDict
