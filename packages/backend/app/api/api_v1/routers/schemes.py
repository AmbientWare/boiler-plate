from pydantic import BaseModel
from typing import List, Optional, Dict, Any


## ----- general schemes -----


class ComponentData(BaseModel):
    label: str = ""
    name: str = ""
    category: str = ""
    description: Optional[str] = ""
    icon: Optional[str] = ""
    inputs: Dict[str, Any] = {}
    inputParams: Optional[List[dict]] = []
    metadata: Optional[dict] = {}
