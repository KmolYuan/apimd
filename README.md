[![Build status](https://img.shields.io/travis/KmolYuan/apimd.svg?logo=travis)](https://travis-ci.org/KmolYuan/apimd)
[![PyPI](https://img.shields.io/pypi/v/apimd.svg)](https://pypi.org/project/apimd/)

# apimd

A Python API compiler for universal Markdown syntax.

Required Python 3.9 and above. (for `ast.unparse` function)

This parser using `ast` standard library to extract the type annotations (without inference) and docstrings, similar to MyPy.
The target modules must be from at least Python 3.0, which is the lowest version with `ast` support.

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

The first is the readable name of the package,
and the second is the name used in import syntax.

The output path can be chosen by "-d" or "--dir" option, default is `docs`.
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

According to PEP 8, "**public**" means a name can't start with underscore symbol "`_`",
except magic methods. ([Naming Conventions])

Normal objects are no docstring their owned.
Please pack them into functions or classes such as `Enum`,
or mention them in the docstring of root module `__init__.py`.
The type inference for global names is not yet supported.

A package should list the objects `__all__` to prevent other public style names.
In this parser, wildcard import syntax (`from ... import *`) will be ignored,
which will cause the name from the statement will lose its parent module.
If there has any import statements in the package root `__init__.py`, the API can be substituted into a short name, for example, change `a.b.c` to `a.c`.
([Global Variable Names])

Object attributes should be noted in the stub files or use Variable Annotations. ([PEP 526])

[Naming Conventions]: https://www.python.org/dev/peps/pep-0008/#naming-conventions
[Global Variable Names]: https://www.python.org/dev/peps/pep-0008/#global-variable-names
[PEP 526]: https://www.python.org/dev/peps/pep-0526/

## Stubs

If a module has a stub file (`.pyi`), the stub file will be loaded for annotations once again.
Docstrings should still be written in the module first.
For extensions (`.so`, `.pyd` or `.dylib` with Python version suffix), this tool will try to load the docstrings from module
if `.py` file is not found.
