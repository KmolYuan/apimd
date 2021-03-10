[![Build status](https://img.shields.io/travis/KmolYuan/apimd.svg?logo=travis)](https://travis-ci.org/KmolYuan/apimd)
[![PyPI](https://img.shields.io/pypi/v/apimd.svg)](https://pypi.org/project/apimd/)

# apimd

A Python API compiler for universal Markdown syntax.

Required Python 3.9 and above. (for `ast.unparse` function)

This parser using `ast` standard library to extract the type annotations (without inference) and docstrings, similar to MyPy.
The target module(s) can be come from at least Python 3.0, which is the lowest version with `ast` support.

## Install

Install by pip:

```bash
pip install apimd
```

From Git repository:

```bash
pip install .
```

## Command Line Interface

Following syntax are allowed:

```bash
apimd module_name
apimd Module-Name=module_name
apimd "Module Name=module_name"
```

The first is the readable name of the package;
the second is the name used in import syntax.
Please make sure you can import the package by the given name in current path.

The output path can be choose by "-d" and "--dir" option, default is `docs`.
Multiple modules are supported either.

```bash
apimd module1 module2 -d out_path
```

If you just want to show output, use dry run mode.

```bash
apimd module --dry
```

## Rules

Basically, this compiler can extract docstrings from those "public" names:

+ Modules
+ Functions & Generators (support async version)
+ Classes and its methods

According to PEP 8, "**public**" means a name can't starts with underscore symbol "`_`",
except magic methods. ([Naming Conventions])

Objects has no docstring their owned.
Please pack them into functions or classes such as `Enum`,
or mention them in the docstring of root module `__init__.py`.

A package should list the objects `__all__` to prevent other public style names and wildcard import syntax (`from ... import *`).
If there has any import statements in the package root `__init__.py`, the API can be substitute into a short name, for example, change `a.b.c` to `a.c`.
([Global Variable Names])

Object attributes should be noted in the stub files or use Variable Annotations ([PEP 526]).

[Naming Conventions]: https://www.python.org/dev/peps/pep-0008/#naming-conventions
[Global Variable Names]: https://www.python.org/dev/peps/pep-0008/#global-variable-names
[PEP 526]: https://www.python.org/dev/peps/pep-0526/

## Stubs

If a module has a stub file, the stub file will be loaded instead of the module.
Docstrings should still be written in the module first.

## Inner links

The docstring can refer the names in the same module or same class.
Use `[name]`, `[class.attribute]` or `[attribute]` syntax to refer them.
If attribute name is conflict with global names, the global name is preferred.
