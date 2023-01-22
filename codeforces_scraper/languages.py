try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
from pydantic import BaseModel, parse_obj_as
from typing import List, Iterable, Optional
from . import assets
import json


class LanguageCompiler(BaseModel):
    """Model containing information about compiler"""
    id: int
    name: str
    extensions: List[str]


ALL_LANGUAGE_COMPILERS = parse_obj_as(
    List[LanguageCompiler],
    json.loads(pkg_resources.read_text(assets, 'all_language_compilers.json'))
)


def compiler_by_name(name: str) -> LanguageCompiler:
    """Return compiler model by name"""
    return next(filter(lambda comp: comp.name == name, ALL_LANGUAGE_COMPILERS))


def compiler_by_id(id: int) -> LanguageCompiler:
    """Return compiler model by id"""
    return next(filter(lambda comp: comp.id == id, ALL_LANGUAGE_COMPILERS))


def all_compilers_by_ext(extension: str) -> Iterable[LanguageCompiler]:
    """Returns ALL compiler supporting given extension
    """
    return filter(lambda comp: extension in comp.extensions,
                  ALL_LANGUAGE_COMPILERS)


def some_compiler_by_ext(extension: str) -> Optional[LanguageCompiler]:
    """Returns some compiler for extension, or None if not supported
    """
    if extension == '.cpp':
        return compiler_by_id(73)
    if extension == '.py':
        return compiler_by_id(70)
    if extension == '.c':
        return compiler_by_id(43)
    if extension == '.hs':
        return compiler_by_id(12)
    return None
