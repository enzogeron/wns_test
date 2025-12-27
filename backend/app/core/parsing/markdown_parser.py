import re
from dataclasses import dataclass
from typing import List, Optional

from app.config import settings
from app.core.parsing.base import Parser
from app.core.parsing.types import DocumentMeta


@dataclass(frozen=True)
class MarkdownSection:
    level: int
    title: str
    lines: List[str]

@dataclass(frozen=True)
class MarkdownDocument:
    meta: DocumentMeta
    sections: List[MarkdownSection]

class MarkdownParser(Parser[MarkdownDocument]):
    _header_re = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$")

    def parse(self, path: str, source_name: Optional[str] = None) -> MarkdownDocument:
        meta = self._meta(path, source_name, "MarkdownParser")

        with open(path, "r", encoding=settings.text_encoding) as f:
            lines = f.read().splitlines()

        sections: List[MarkdownSection] = []
        current: Optional[MarkdownSection] = None

        for line in lines:
            m = self._header_re.match(line.strip())
            if m:
                if current is not None:
                    sections.append(current)

                level = len(m.group("hashes"))
                title = m.group("title").strip()

                current = MarkdownSection(
                    level=level,
                    title=title,
                    lines=[]
                )
            else:
                if current is not None:
                    current.lines.append(line)

        if current is not None:
            sections.append(current)

        return MarkdownDocument(meta=meta, sections=sections)