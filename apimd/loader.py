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


def loader(name: str, root: str) -> str:
    """Package searching algorithm."""
    p = Parser()
    for info in walk_packages([root]):
        if not info.name.startswith(name):
            continue
        path = join(root, info.name.replace('.', sep))
        if info.ispkg:
            path += sep + "__init__.py"
            if not isfile(path):
                path += "i"
        else:
            path += ".py"
            if not isfile(path):
                path += "i"
        if isfile(path):
            logger.debug(f"{info.name} <= {path}")
            with open(path, 'r') as f:
                p.parser(info.name, f.read())
    return p.compile()


def gen_api(
    root_names: dict[str, str],
    pwd: str = '.',
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
