# import document loaders
from langchain_core.documents import Document
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from app.components import load_component_library
from app.components import BaseComponent, ComponentData



class BaseDataLoader(BaseComponent):
    category: str = "Data Loaders"

    def load(
        self, componentData: ComponentData, collection: str
    ) -> None:
        """Load data into objects"""
        raise NotImplementedError("load method must be implemented in child class")


    def _load(
        self, componentData: ComponentData, db: Optional[Session] = None
    ) -> None:
        """Load data into objects"""
        raise NotImplementedError("load method must be implemented in child class")


# load all the data loaders
data_loaders = load_component_library("data_loaders")
