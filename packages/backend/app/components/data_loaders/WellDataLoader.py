from typing import List, Optional
from sqlalchemy.orm import Session

from app.components import ComponentInput, ComponentData
from app.components.data_loaders import BaseDataLoader


class WellDataLoaderComponent(BaseDataLoader):
    label: str = "Well Data Loader"
    name: str = "WellDataLoader"
    icon: str = "data.svg"
    description: str = "Load well log data"
    inputs: List[ComponentInput] = [
        ComponentInput(
            label="Data File",
            name="dataFile",
            type="file",
            fileType=".pdf",
        )
    ]

    def _load(self, componentData: ComponentData, db: Optional[Session] = None) -> None:
        raise NotImplementedError("load method must be implemented in child class")


WellDataLoader = WellDataLoaderComponent()
