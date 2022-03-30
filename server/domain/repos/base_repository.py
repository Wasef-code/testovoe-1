from typing import Any, Generic, Type, TypeVar
from domain.entities.entities import Base
from domain.entities.exceptions import ResourceNotFound
from domain.globals.state import generate_id
ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    __internal: dict[str, ModelType] = {}

    def generate_uuid(self) -> str:
        key = generate_id()
        while key in self.__internal:
            key = generate_id()
        return key

    def __init__(self, model: Type[ModelType]):
        self.model_class = model

    def from_list(self, model_list: list[ModelType]):
        for i in model_list:
            self.__internal[i.uuid] = i

    def add(self, obj: ModelType) -> str:
        obj.uuid = self.generate_uuid()
        self.__internal[obj.uuid] = obj
        return obj.uuid

    def get(self, uuid: str) -> ModelType:
        return self.__internal.get(uuid)

    def get_all(self):
        return self.__internal.values()

    def update(self, obj: ModelType, obj_values: dict[str, Any]) -> ModelType:
        if obj not in self.__internal.values():
            self.add(obj)
        for i in obj_values:
            setattr(obj, i, obj_values[i])
        return obj

    def delete(self, obj: ModelType):
        try:
            self.__internal.pop(obj.uuid)
        except KeyError:
            raise ResourceNotFound
