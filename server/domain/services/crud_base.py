from typing import Callable, Generic, Type, TypeVar
from domain.entities.entities import Base
from domain.repos.base_repository import BaseRepository
from domain.deps.deps_interfaces import get_db


ModelType = TypeVar("ModelType", bound=Base)
RepoType = TypeVar("RepoType", bound=BaseRepository)


class CrudBase(Generic[ModelType, RepoType]):

    def __init__(self, model: Type[ModelType], repo: Type[RepoType],
                 get_repo: Callable[[], RepoType]):
        self.model_class = model
        self.repo_class = repo
        self.repo_object = get_repo()

    def create(self, *args):
        model_object = self.model_class(*args)
        ident = self.repo_object.add(model_object)
        with get_db().create_session() as session, session.begin():
            session.add(model_object)
        return ident

    def read(self, uuid: str) -> ModelType:
        return self.repo_object.get(uuid)

    def read_multi(self) -> list[ModelType]:
        return self.repo_object.get_all()

    def update(self, uuid: str, **kwargs):
        obj = self.repo_object.get(uuid)
        obj = self.repo_object.update(obj, kwargs)
        with get_db().create_session() as session, session.begin():
            session.merge(obj)

    def delete(self, uuid: str):
        self.repo_object.delete(self.repo_object.get(uuid))
