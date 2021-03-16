# -*- coding: utf-8 -*-

"""Compiler functions."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2020-2021"
__license__ = "MIT"
__email__ = "pyslvs@gmail.com"

from typing import Sequence
from sys import stdout
from os import mkdir
from os.path import isdir, isfile, join, sep
from logging import getLogger, basicConfig, DEBUG
from pkgutil import walk_packages
from importlib.abc import Loader
from importlib.machinery import EXTENSION_SUFFIXES
from importlib.util import spec_from_file_location, module_from_spec
from .parser import Parser

basicConfig(stream=stdout, level=DEBUG, format="%(message)s")
logger = getLogger()


def _read(path: str) -> str:
    """Read the script from file."""
    with open(path, 'r') as f:
        return f.read()


def _write(path: str, doc: str) -> None:
    """Write text to the file."""
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(doc)


def _load_module(name: str, path: str, p: Parser) -> bool:
    """Load module directly."""
    s = spec_from_file_location(name, path)
    if s is not None and isinstance(s.loader, Loader):
        m = module_from_spec(s)
        s.loader.exec_module(m)
        p.load_docstring(name, m)
        return True
    return False


def loader(root: str, pwd: str, level: int) -> str:
    """Package searching algorithm."""
    p = Parser(level)
    for info in walk_packages([pwd]):
        # PEP561
        name = info.name.replace('-stubs', "")
        if not name.startswith(root):
            continue
        path = join(pwd, info.name.replace('.', sep))
        if info.ispkg:
            path += sep + "__init__"
        # Load its source or stub
        pure_py = False
        for ext in [".py", ".pyi"]:
            path_ext = path + ext
            if not isfile(path_ext):
                continue
            logger.debug(f"{name} <= {path_ext}")
            p.parse(name, _read(path_ext))
            if ext == ".py":
                pure_py = True
        if pure_py or name in p.docstring:
            continue
        logger.warning(f"! not fully documented, loading extension module")
        # Try to load module here
        for ext in EXTENSION_SUFFIXES:
            path_ext = path + ext
            if not isfile(path_ext):
                continue
            logger.debug(f"{name} <= {path_ext}")
            if _load_module(name, path_ext, p):
                break
        else:
            logger.warning(f"! no module for {name}")
    return p.compile()


def gen_api(
    root_names: dict[str, str],
    pwd: str = '.',
    *,
    prefix: str = 'docs',
    level: int = 1,
    dry: bool = False
) -> Sequence[str]:
    """Generate API. All rules are listed in the readme.

    The path `pwd` is the current path that provided to `pkgutil`,
    which allows the "site-packages" directory to be used.
    """
    if not isdir(prefix):
        logger.debug(f"Create directory: {prefix}")
        mkdir(prefix)
    docs = []
    for title, name in root_names.items():
        logger.debug(f"Load root: {name} ({title})")
        doc = loader(name, pwd, level)
        if not doc.strip():
            logger.warning(f"! '{name}' can not be found")
            continue
        doc = '#' * level + f" {title} API\n\n" + doc
        path = join(prefix, f"{name.replace('_', '-')}-api.md")
        logger.debug(f"Write file: {path}")
        if dry:
            logger.debug(doc)
        else:
            _write(path, doc)
        docs.append(doc)
    return docs
