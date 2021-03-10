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
from setuptools import find_packages
from pkgutil import walk_packages
from .parser import Parser

basicConfig(stream=stdout, level=DEBUG, format="%(message)s")
logger = getLogger()


def find(path: str) -> str:
    """Return file path if existed."""
    return path if isfile(path) else ""


def loader(root_name: str, root: str) -> str:
    """Package searching algorithm."""
    p = Parser()
    for info in walk_packages([root]):
        # PEP561
        name = info.name.replace('-stubs', "")
        if not name.startswith(root_name):
            continue
        path = info.name.replace('.', sep)
        if info.ispkg:
            path = join(path, "__init__")
        path = find(join(root, path + ".pyi")) or find(join(root, path + ".py"))
        if path:
            logger.debug(f"{name} <= {path}")
            with open(path, 'r') as f:
                p.parse(name, f.read())
        else:
            logger.warning(f"no Python source for {name}")
    return p.compile()


def gen_api(
    root_names: dict[str, str],
    pwd: str = '.',
    *,
    prefix: str = 'docs',
    dry: bool = False
) -> Sequence[str]:
    """Generate API. All rules are listed in the readme."""
    if not isdir(prefix):
        logger.debug(f"Create directory: {prefix}")
        mkdir(prefix)
    docs = []
    for title, name in root_names.items():
        logger.debug(f"Load root: {name} ({title})")
        if not find_packages(pwd, include=[name]):
            logger.warning(f"'{name}' can not be found")
            continue
        doc = f"# {title} API\n\n" + loader(name, pwd)
        path = join(prefix, f"{name.replace('_', '-')}-api.md")
        logger.debug(f"Write file: {path}")
        if dry:
            logger.debug(doc)
        else:
            with open(path, 'w+', encoding='utf-8') as f:
                f.write(doc)
        docs.append(doc)
    return docs
