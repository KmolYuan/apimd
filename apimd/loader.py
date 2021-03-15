# -*- coding: utf-8 -*-

"""Compiler functions."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2020"
__license__ = "MIT"
__email__ = "pyslvs@gmail.com"

from typing import Sequence
from sys import stdout
from os import mkdir
from os.path import isdir, isfile, join, sep
from logging import getLogger, basicConfig, DEBUG
from pkgutil import walk_packages
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


def loader(root: str, pwd: str, level: int) -> str:
    """Package searching algorithm."""
    p = Parser(level)
    for info in walk_packages([pwd]):
        # PEP561
        name = info.name.replace('-stubs', "")
        if not name.startswith(root):
            continue
        path = info.name.replace('.', sep)
        if info.ispkg:
            path = join(path, "__init__")
        # Load its source or stub
        checked = False
        for ext in ["py", ".pyi"]:
            path_ext = join(pwd, path + "." + ext)
            if not isfile(path_ext):
                continue
            logger.debug(f"{name} <= {path_ext}")
            p.parse(name, _read(path_ext))
            checked = True
        # TODO: Try to load module here
        if not checked:
            logger.warning(f"no source or module for {name}")
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
        if not doc:
            logger.warning(f"'{name}' can not be found")
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
