# -*- coding: utf-8 -*-

"""Data structures."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2020"
__license__ = "MIT"
__email__ = "pyslvs@gmail.com"

from typing import Sequence, Union, Optional
from dataclasses import dataclass, field
from ast import (
    parse, dump, get_docstring, iter_child_nodes, FunctionDef, ClassDef,
    unparse, arg, expr,
)


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


def table_titles(args: Sequence[arg]) -> str:
    """Names of the table."""
    return " | ".join(a.arg for a in args)


def table_annotation(args: Sequence[arg]) -> str:
    """Annotations of the table."""
    e = []
    for a in args:
        if a.arg == 'self':
            e.append("`Self`")
        elif a.annotation is not None:
            e.append(f"`{unparse(a.annotation)}`")
        else:
            e.append("`Any`")
    return " | ".join(e)


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
    # TODO: Alias and global names
    alias: dict[str, str] = field(default_factory=dict)

    def parser(self, name: str, script: str) -> None:
        """Main parser of the entire module."""
        self.doc[name] = f"## Module `{name}`\n\n"
        root = parse(script,
                     type_comments=True,
                     feature_version=annotations.compiler_flag)
        mod_doc = get_docstring(root)
        if mod_doc is not None:
            self.doc[name] += mod_doc + '\n\n'
        for node in iter_child_nodes(root):
            if isinstance(node, (FunctionDef, ClassDef)):
                self.api(name + '.' + node.name, node)

    def api(self, name: str, node: Union[FunctionDef, ClassDef], *,
            prefix: str = '') -> None:
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
        doc += f"*Full name:* `{name}`\n\n"
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
                    + "| " + table_annotation(args) + " |\n")
            if default:
                doc += ("| " + " | ".join(
                    [table_blank(len(args) - len(default) - 1),
                     table_literal(default),
                     table_blank(1)]) + " |\n")
            doc += '\n'
        obj_doc = get_docstring(node)
        if obj_doc is not None:
            doc += obj_doc + '\n\n'
        if isinstance(node, ClassDef):
            for sub_node in node.body:
                if isinstance(sub_node, (FunctionDef, ClassDef)):
                    self.api(name + '.' + sub_node.name, sub_node,
                             prefix=node.name)
        self.doc[name] = doc

    def compile(self) -> str:
        """Compile doc."""
        doc = ""
        for name in sorted(self.doc):
            doc += self.doc[name]
        return doc.rstrip() + '\n'
