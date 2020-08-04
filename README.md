[![Build status](https://img.shields.io/travis/KmolYuan/apimd.svg?logo=travis)](https://travis-ci.org/KmolYuan/apimd)
[![PyPI](https://img.shields.io/pypi/v/apimd.svg)](https://pypi.org/project/apimd/)

# apimd

A Python API compiler for universal Markdown syntax.

Required Python 3.7 and above.

## Install

Install by pip:

```bash
pip install apimd
```

From Git repository:

```bash
python setup.py install
```

Run directly:

```bash
python launcher.py --help
```

## Command

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

Basically, this compiler can extract docstrings
from those "public" objects:

+ Modules
+ Functions
+ Generators
+ Classes and its methods

According to PEP 8, "**public**" means a name can't starts with underscore symbol "`_`",
and the magic methods will be excluded, apart from `__init__` method.
([Naming Conventions])

Builtins object (`int`, `str`, `list`, `dict`, etc.) has no docstring their owned.
So even they are public name style or listed in `__all__`,
this compiler will still skip them (like `__version__` or `MY_GLOBAL`).
Please pack them into functions or classes such as `Enum`,
or mention them in the docstring of root module `__init__.py`.

A root package force required a list object `__all__` to show all of global names
to prevent wildcard import syntax (`from ... import *`).
This compiler will not search a non-root package unless add a `__all__` list.
([Global Variable Names])

This compiler can detect properties, class attributes, static methods and abstract methods as well.
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
