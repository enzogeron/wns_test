from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.core.parsing.types import DocumentMeta

T = TypeVar("T")

class Parser(ABC, Generic[T]):
    @abstractmethod
    def parse(self, path: str, source_name: str | None = None) -> T:
        raise NotImplementedError

    def _meta(self, path: str, source_name: str | None, parser_name: str) -> DocumentMeta:
        return DocumentMeta(
            source_name=source_name or path.split("/")[-1],
            source_path=path,
            parser=parser_name,
        )
