# -*- coding: utf-8 -*-

"""Data structures."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2020"
__license__ = "MIT"
__email__ = "pyslvs@gmail.com"

from typing import Sequence, Iterator, Union, Optional
from dataclasses import dataclass, field
from ast import (
    parse, dump, get_docstring, iter_child_nodes, FunctionDef, ClassDef,
    Assign, AnnAssign, Import, ImportFrom, Name, unparse, arg, expr,
)

_I = Union[Import, ImportFrom]
_G = Union[Assign, AnnAssign]
_API = Union[FunctionDef, ClassDef]
TA = 'typing.TypeAlias'


def is_public_family(name: str) -> bool:
    """Check the name is come from public modules or not."""
    for n in name.split('.'):
        # Magic name
        if n[:2] == n[-2:] == '__':
            continue
        # Local or private name
        if n.startswith('_'):
            return False
    return True


def interpret_mode(doc: str) -> Iterator[str]:
    """Replace doctest as markdown Python code."""
    keep = False
    lines = doc.split('\n')
    for i, line in enumerate(lines):
        signed = line.startswith(">>> ")
        if signed:
            line = line[len(">>> "):]
            if not keep:
                yield "```python"
                keep = True
        elif keep:
            yield "```\n"
            keep = False
        yield line
        if signed and i == len(lines) - 1:
            yield "```\n"
            keep = False


def table_titles(args: Sequence[arg]) -> str:
    """Names of the table."""
    return " | ".join(a.arg for a in args)


def table_split(args: Sequence[arg]) -> str:
    """The split line of the table."""
    return "|".join(":" + '-' * (len(a.arg) if len(a.arg) > 3 else 3) + ":"
                    for a in args)


def table_blank(n: int) -> str:
    """Blanks of the table."""
    return " | ".join(" " for _ in range(n))


def table_literal(args: Sequence[Optional[expr]]) -> str:
    """Literals of the table."""
    return " | ".join([f"{unparse(a)}" if a is not None else " " for a in args])


@dataclass
class Parser:
    doc: dict[str, str] = field(default_factory=dict)
    alias: dict[str, str] = field(default_factory=dict)

    def parser(self, root: str, script: str) -> None:
        """Main parser of the entire module."""
        self.doc[root] = f"## Module `{root}`\n\n"
        root_node = parse(script,
                          type_comments=True,
                          feature_version=annotations.compiler_flag)
        mod_doc = get_docstring(root_node)
        if mod_doc is not None:
            self.doc[root] += '\n'.join(interpret_mode(mod_doc)) + '\n\n'
        for node in iter_child_nodes(root_node):
            if isinstance(node, (Import, ImportFrom)):
                self.imports(root, node)
            if isinstance(node, (Assign, AnnAssign)):
                self.globals(root, node)
            elif isinstance(node, (FunctionDef, ClassDef)):
                self.api(root, node)

    def imports(self, root: str, node: _I) -> None:
        """Save import names for 'typing.TypeAlias'."""
        if isinstance(node, Import):
            for a in node.names:
                if a.name != 'typing.TypeAlias':
                    continue
                if a.asname is None:
                    self.alias[root + '.' + TA] = TA
                else:
                    self.alias[root + '.' + a.asname] = TA
        else:
            if node.module != 'typing':
                return
            for a in node.names:
                if a.name != 'TypeAlias':
                    continue
                if a.asname is None:
                    self.alias[root + '.TypeAlias'] = TA
                else:
                    self.alias[root + '.' + a.asname] = TA

    def globals(self, root: str, node: _G) -> None:
        """Assign globals."""
        if isinstance(node, AnnAssign):
            if (
                isinstance(node.annotation, Name)
                and isinstance(node.target, Name)
                and self.alias.get(root + '.' + node.annotation.id, '') == TA
                and node.value is not None
            ):
                self.alias[root + '.' + node.target.id] = unparse(node.value)
        else:
            for sn in node.targets:
                if isinstance(sn, Name):
                    self.alias[root + '.' + sn.id] = unparse(node.value)

    def api(self, root: str, node: _API, *, prefix: str = '') -> None:
        """Create API doc for only functions and classes.
        Where `name` is the full name.
        """
        doc = ""
        if prefix:
            prefix += '.'
        if isinstance(node, FunctionDef):
            doc += f"### {prefix + node.name}()\n\n"
        else:
            doc += f"### class {prefix + node.name}\n\n"
        full_name = root + '.' + prefix + node.name
        doc += f"*Full name:* `{full_name}`\n\n"
        if node.decorator_list:
            doc += ("| Decorators |\n|:" + '-' * 10 + ":|\n"
                    + '\n'.join(f"| `@{unparse(d)}` |"
                                for d in node.decorator_list)
                    + '\n\n')
        if isinstance(node, FunctionDef):
            args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
            args += [arg(arg='return', annotation=node.returns)]
            default: list[Optional[expr]] = []
            default.extend(node.args.defaults)
            default.extend(node.args.kw_defaults)
            # default = node.args.defaults + node.args.kw_defaults
            doc += ("| " + table_titles(args) + " |\n"
                    + "|" + table_split(args) + "|\n"
                    + "| " + self.table_annotation(root, args) + " |\n")
            if default:
                doc += ("| " + " | ".join(
                    [table_blank(len(args) - len(default) - 1),
                     table_literal(default),
                     table_blank(1)]) + " |\n")
            doc += '\n'
        obj_doc = get_docstring(node)
        if obj_doc is not None:
            doc += '\n'.join(interpret_mode(obj_doc)) + '\n\n'
        if isinstance(node, ClassDef):
            for sub_node in node.body:
                if isinstance(sub_node, (FunctionDef, ClassDef)):
                    self.api(root, sub_node, prefix=node.name)
        self.doc[full_name] = doc

    def table_annotation(self, root: str, args: Sequence[arg]) -> str:
        """Annotations of the table."""
        e = []
        for a in args:
            if a.arg == 'self':
                e.append("`Self`")
            elif a.annotation is not None:
                if isinstance(a.annotation, Name):
                    # TODO: Name resolver
                    name = a.annotation.id
                    e.append(f"`{self.alias.get(root + '.' + name, name)}`")
                else:
                    e.append(f"`{unparse(a.annotation)}`")
            else:
                e.append("`Any`")
        return " | ".join(e)

    def compile(self) -> str:
        """Compile doc."""
        doc = ""
        for name in sorted(self.doc):
            doc += self.doc[name]
        return doc.rstrip() + '\n'
