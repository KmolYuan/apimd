# -*- coding: utf-8 -*-

"""Data structures."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2020"
__license__ = "MIT"
__email__ = "pyslvs@gmail.com"

from typing import cast, Sequence, Iterator, Union, Optional
from dataclasses import dataclass, field
from html import escape
from ast import (
    parse, unparse, get_docstring, AST, FunctionDef, AsyncFunctionDef, ClassDef,
    Assign, AnnAssign, Import, ImportFrom, Name, Expr, Subscript, BinOp, BitOr,
    Tuple, Constant, Load, Attribute, arg, expr, stmt, arguments,
    NodeTransformer,
)

_I = Union[Import, ImportFrom]
_G = Union[Assign, AnnAssign]
_API = Union[FunctionDef, AsyncFunctionDef, ClassDef]
TA = 'typing.TypeAlias'


def _m(*names: str) -> str:
    """Get module names"""
    return '.'.join(names)


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


def names_cmp(s: str) -> tuple[bool, str]:
    """Name comparison function."""
    return (not s.islower(), s.lower())


def code(doc: str) -> str:
    """Escape Markdown charters from code."""
    doc = escape(doc).replace('|', '&#124;')
    if '&' in doc:
        return f"<code>{doc}</code>"
    else:
        return f"`{doc}`"


def esc_usc(doc: str) -> str:
    """Escape underscore in names."""
    if doc.count('_') > 1:
        return doc.replace('_', r"\_")
    else:
        return doc


def interpret_mode(doc: str) -> Iterator[str]:
    r"""Replace doctest as markdown Python code.

    Usage:
    >>> from apimd.parser import interpret_mode
    >>> '\n'.join(interpret_mode(">>> print(\"Hello\")"))
    """
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
            yield "```"
            keep = False
        yield line
        if signed and i == len(lines) - 1:
            yield "```"
            keep = False


def table_split(args: Sequence[arg]) -> str:
    """The split line of the table."""
    return "|".join(":" + '-' * (len(a.arg) if len(a.arg) > 3 else 3) + ":"
                    for a in args)


def table_literal(args: Sequence[Optional[expr]]) -> str:
    """Literals of the table."""
    return " | ".join([f"{unparse(a)}" if a is not None else " " for a in args])


def list_table(title: str, listed: Iterator[str]) -> str:
    """Create one column table with a title."""
    return (f"| {title} |\n|:" + '-' * len(title) + ":|\n"
            + '\n'.join(f"| {code(e)} |" for e in listed)) + '\n\n'


class Resolver(NodeTransformer):
    """Annotation resolver."""

    def __init__(self, root: str, alias: dict[str, str]):
        super(Resolver, self).__init__()
        self.root = root
        self.alias = alias

    def visit_Constant(self, node: Constant) -> AST:
        """Check string is a name."""
        if not isinstance(node.value, str):
            return node
        try:
            e = cast(Expr, parse(node.value).body[0])
        except SyntaxError:
            return node
        else:
            return self.visit(e.value)

    def visit_Name(self, node: Name) -> AST:
        """Replace global names with its expression recursively."""
        name = _m(self.root, node.id)
        if name in self.alias:
            e = cast(Expr, parse(self.alias[name]).body[0])
            return self.visit(e.value)
        else:
            return node

    def visit_Subscript(self, node: Subscript) -> AST:
        """Replace `Union[T1, T2, ...]` as T1 | T2 | ..."""
        if not isinstance(node.value, Name):
            return node
        name = node.value.id
        idf = self.alias.get(_m(self.root, name), name)
        if idf == 'typing.Union':
            if not isinstance(node.slice, Tuple):
                return node.slice
            b = node.slice.elts[0]
            for e in node.slice.elts[1:]:
                b = BinOp(b, BitOr(), e)
            return b
        elif idf == 'typing.Optional':
            return BinOp(node.slice, BitOr(), Constant(None))
        else:
            return node

    def visit_Attribute(self, node: Attribute) -> AST:
        """Remove `typing.*` prefix of annotation."""
        if not isinstance(node.value, Name):
            return node
        if node.value.id == 'typing':
            return Name(node.attr, Load())
        else:
            return node


@dataclass
class Parser:
    doc: dict[str, str] = field(default_factory=dict)
    docstring: dict[str, str] = field(default_factory=dict)
    # TODO: Support __all__
    all: set[str] = field(default_factory=set)
    alias: dict[str, str] = field(default_factory=dict)

    def parser(self, root: str, script: str) -> None:
        """Main parser of the entire module."""
        self.doc[root] = f"## Module `{root}`\n\n"
        root_node = parse(script, type_comments=True)
        doc = get_docstring(root_node)
        if doc is not None:
            self.docstring[root] = '\n'.join(interpret_mode(doc))
        for node in root_node.body:
            if isinstance(node, (Import, ImportFrom)):
                self.imports(root, node)
            if isinstance(node, (Assign, AnnAssign)):
                self.type_alias(root, node)
            elif isinstance(node, (FunctionDef, AsyncFunctionDef, ClassDef)):
                self.api(root, node)

    def imports(self, root: str, node: _I) -> None:
        """Save import names for 'typing.*'."""
        if isinstance(node, Import):
            for a in node.names:
                if a.asname is None:
                    self.alias[_m(root, a.name)] = a.name
                else:
                    self.alias[_m(root, a.asname)] = a.name
        else:
            for a in node.names:
                if a.asname is None:
                    self.alias[_m(root, a.name)] = _m(node.module, a.name)
                else:
                    self.alias[_m(root, a.asname)] = _m(node.module, a.name)

    def type_alias(self, root: str, node: _G) -> None:
        """Set up global type alias."""
        if isinstance(node, AnnAssign):
            if (
                isinstance(node.annotation, Name)
                and isinstance(node.target, Name)
                and self.alias.get(_m(root, node.annotation.id), '') == TA
                and node.value is not None
            ):
                self.alias[_m(root, node.target.id)] = unparse(node.value)
        else:
            if (
                node.type_comment is None
                or self.alias.get(node.type_comment) == TA
            ):
                for sn in node.targets:
                    if isinstance(sn, Name):
                        self.alias[_m(root, sn.id)] = unparse(node.value)

    def api(self, root: str, node: _API, *, prefix: str = '') -> None:
        """Create API doc for only functions and classes.
        Where `name` is the full name.
        """
        level = '#' * 3
        if prefix:
            prefix += '.'
            level += '#'
        name = _m(root, prefix + node.name)
        shirt_name = esc_usc(prefix + node.name)
        if isinstance(node, FunctionDef):
            self.doc[name] = level + f" {shirt_name}()\n\n"
        elif isinstance(node, AsyncFunctionDef):
            self.doc[name] = level + f" async {shirt_name}()\n\n"
        else:
            self.doc[name] = level + f" class {shirt_name}\n\n"
        self.doc[name] += f"*Full name:* `{name}`\n\n"
        if isinstance(node, ClassDef) and node.bases:
            self.doc[name] += list_table("Bases", (f"{unparse(d)}"
                                                   for d in node.bases))
        if node.decorator_list:
            self.doc[name] += list_table("Decorators", (f"@{unparse(d)}"
                                                        for d in
                                                        node.decorator_list))
        if isinstance(node, (FunctionDef, AsyncFunctionDef)):
            self.func_api(root, name, node.args, node.returns)
        else:
            self.class_api(name, node.body)
        doc = get_docstring(node)
        if doc is not None:
            self.docstring[name] = '\n'.join(interpret_mode(doc))
        if isinstance(node, ClassDef):
            for e in node.body:
                if isinstance(e, (FunctionDef, AsyncFunctionDef, ClassDef)):
                    self.api(root, e, prefix=node.name)

    def func_api(self, root: str, name: str, node: arguments,
                 returns: Optional[expr]) -> None:
        """Create function API."""
        args = []
        default: list[Optional[expr]] = []
        if node.posonlyargs:
            args.extend(node.posonlyargs)
            args.append(arg('/'))
            default.extend([None] * len(node.posonlyargs))
        args.extend(node.args)
        default.extend([None] * (len(node.args) - len(node.defaults)))
        default.extend(node.defaults)
        if node.vararg is not None:
            args.append(arg('*' + node.vararg.arg, node.vararg.annotation))
        elif node.kwonlyargs:
            args.append(arg('*'))
        default.append(None)
        args.extend(node.kwonlyargs)
        default.extend([None] * (len(node.kwonlyargs) - len(node.kw_defaults)))
        default.extend(node.kw_defaults)
        if node.kwarg is not None:
            args.append(arg('**' + node.kwarg.arg, node.kwarg.annotation))
            default.append(None)
        args.append(arg('return', returns))
        default.append(None)
        self.doc[name] += (
            "| " + " | ".join(a.arg for a in args) + " |\n"
            + "|" + table_split(args) + "|\n"
            + "| " + self.table_annotation(root, args) + " |\n")
        if not all(d is None for d in default):
            self.doc[name] += f"| {table_literal(default)} |\n"
        self.doc[name] += '\n'

    def class_api(self, name: str, body: list[stmt]) -> None:
        """Create class API."""
        members = {}
        for e in body:
            if isinstance(e, AnnAssign) and isinstance(e.target, Name):
                members[e.target.id] = unparse(e.annotation)
        if not members:
            return
        self.doc[name] += (
            "| Members | Type |\n|:" + '-' * 7 + ":|:" + '-' * 4 + ":|\n"
            + '\n'.join(f"| `{n}` | {code(members[n])} |"
                        for n in sorted(members))
            + '\n\n')

    def table_annotation(self, root: str, args: Sequence[arg]) -> str:
        """Annotations of the table."""
        e = []
        for a in args:
            if a.arg == 'self':
                e.append("`Self`")
            elif a.arg in {'*', '**'}:
                e.append(" ")
            elif a.annotation is not None:
                e.append(code(self.resolve(root, a.annotation)))
            else:
                e.append("`Any`")
        return " | ".join(e)

    def resolve(self, root: str, old_node: expr) -> str:
        """Search and resolve global names in annotation."""
        r = Resolver(root, self.alias)
        return unparse(r.generic_visit(r.visit(old_node)))

    def compile(self) -> str:
        """Compile doc."""
        return "\n\n".join((self.doc[n] + self.docstring.get(n, "")).rstrip()
                           for n in sorted(self.doc, key=names_cmp)
                           if is_public_family(n)) + '\n'
