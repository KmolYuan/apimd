# apimd API

## Module `apimd`

A Python API compiler for universal Markdown syntax.

### gen_api()

*Full name:* `apimd.gen_api`

| root_names | pwd | * | prefix | level | dry | return |
|:----------:|:---:|:---:|:------:|:-----:|:---:|:------:|
| `dict[str, str]` | <code>str &#124; None</code> |   | `str` | `int` | `bool` | `collections.abc.Sequence[str]` |
|   | `None` |   | <code>&#x27;docs&#x27;</code> | `1` | `False` |   |

Generate API. All rules are listed in the readme.

The path `pwd` is the current path that provided to `pkgutil`,
which allows the "site-packages" directory to be used.

## Module `apimd.__main__`

The command line launcher of apimd.

### main()

*Full name:* `apimd.__main__.main`

| return |
|:------:|
| `None` |

Main function.

## Module `apimd.loader`

| Constants | Type |
|:---------:|:----:|
| `PEP561_SUFFIX` | `str` |

Compiler functions.

### loader()

*Full name:* `apimd.loader.loader`

| root | pwd | level | return |
|:----:|:---:|:-----:|:------:|
| `str` | `str` | `int` | `str` |

Package searching algorithm.

### walk_packages()

*Full name:* `apimd.loader.walk_packages`

| name | path | return |
|:----:|:----:|:------:|
| `str` | `str` | `collections.abc.Iterator[tuple[str, str]]` |

Walk packages without import them.

## Module `apimd.parser`

Data structures.

### code()

*Full name:* `apimd.parser.code`

| doc | return |
|:---:|:------:|
| `str` | `str` |

Escape Markdown charters from code.

### const_type()

*Full name:* `apimd.parser.const_type`

| node | return |
|:----:|:------:|
| `ast.expr` | `str` |

Constant type inference.

### esc_underscore()

*Full name:* `apimd.parser.esc_underscore`

| doc | return |
|:---:|:------:|
| `str` | `str` |

Escape underscore in names.

### interpret_mode()

*Full name:* `apimd.parser.interpret_mode`

| doc | return |
|:---:|:------:|
| `str` | `collections.abc.Iterator[str]` |

Replace doctest as markdown Python code.

Usage:
```python
from apimd.parser import interpret_mode
'\n'.join(interpret_mode(">>> a = \"Hello\""))
```

### is\_public\_family()

*Full name:* `apimd.parser.is_public_family`

| name | return |
|:----:|:------:|
| `str` | `bool` |

Check the name is come from public modules or not.

### parent()

*Full name:* `apimd.parser.parent`

| name | * | level | return |
|:----:|:---:|:-----:|:------:|
| `str` |   | `int` | `str` |
|   |   | `1` |   |

Get parent name with level.

### class Parser

*Full name:* `apimd.parser.Parser`

| Decorators |
|:----------:|
| `@dataclasses.dataclass` |

| Members | Type |
|:-------:|:----:|
| `alias` | `dict[str, str]` |
| `b_level` | `int` |
| `const` | `dict[str, str]` |
| `doc` | `dict[str, str]` |
| `docstring` | `dict[str, str]` |
| `imp` | `dict[str, set[str]]` |
| `level` | `dict[str, int]` |
| `root` | `dict[str, str]` |

AST parser.

Usage:
```python
from apimd.parser import Parser
p = Parser()
with open("pkg_path", 'r') as f:
    p.parse('pkg_name', f.read())
s = p.compile()
```

#### Parser.annotations()

*Full name:* `apimd.parser.Parser.annotations`

| self | root | args | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | `collections.abc.Sequence[ast.arg]` | `collections.abc.Iterator[str]` |

Annotations of the table.

#### Parser.api()

*Full name:* `apimd.parser.Parser.api`

| self | root | node | * | prefix | return |
|:----:|:----:|:----:|:---:|:------:|:------:|
| `Self` | `str` | <code>ast.FunctionDef &#124; ast.AsyncFunctionDef &#124; ast.ClassDef</code> |   | `str` | `None` |
|   |   |   |   | <code>&#x27;&#x27;</code> |   |

Create API doc for only functions and classes.
Where `name` is the full name.

#### Parser.class_api()

*Full name:* `apimd.parser.Parser.class_api`

| self | root | name | bases | body | return |
|:----:|:----:|:----:|:-----:|:----:|:------:|
| `Self` | `str` | `str` | `list[ast.expr]` | `list[ast.stmt]` | `None` |

Create class API.

#### Parser.compile()

*Full name:* `apimd.parser.Parser.compile`

| self | return |
|:----:|:------:|
| `Self` | `str` |

Compile documentation.

#### Parser.func_api()

*Full name:* `apimd.parser.Parser.func_api`

| self | root | name | node | returns | return |
|:----:|:----:|:----:|:----:|:-------:|:------:|
| `Self` | `str` | `str` | `ast.arguments` | <code>ast.expr &#124; None</code> | `None` |

Create function API.

#### Parser.globals()

*Full name:* `apimd.parser.Parser.globals`

| self | root | node | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | <code>ast.Assign &#124; ast.AnnAssign</code> | `None` |

Set up globals:

+ Type alias
+ Constants
+ `__all__` filter

#### Parser.imports()

*Full name:* `apimd.parser.Parser.imports`

| self | root | node | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | <code>ast.Import &#124; ast.ImportFrom</code> | `None` |

Save import names for 'typing.*'.

#### Parser.is_public()

*Full name:* `apimd.parser.Parser.is_public`

| self | s | return |
|:----:|:---:|:------:|
| `Self` | `str` | `bool` |

Check the name is public style or listed in `__all__`.

#### Parser.load_docstring()

*Full name:* `apimd.parser.Parser.load_docstring`

| self | root | m | return |
|:----:|:----:|:---:|:------:|
| `Self` | `str` | `types.ModuleType` | `None` |

Load docstring from the module.

#### Parser.parse()

*Full name:* `apimd.parser.Parser.parse`

| self | root | script | return |
|:----:|:----:|:------:|:------:|
| `Self` | `str` | `str` | `None` |

Main parser of the entire module.

#### Parser.resolve()

*Full name:* `apimd.parser.Parser.resolve`

| self | root | node | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | `ast.expr` | `str` |

Search and resolve global names in annotation.

### class Resolver

*Full name:* `apimd.parser.Resolver`

| Bases |
|:-----:|
| `ast.NodeTransformer` |

Annotation resolver.

#### Resolver.\_\_init\_\_()

*Full name:* `apimd.parser.Resolver.__init__`

| self | root | alias | return |
|:----:|:----:|:-----:|:------:|
| `Self` | `str` | `dict[str, str]` | `Any` |

Set root module and alias.

#### Resolver.visit_Attribute()

*Full name:* `apimd.parser.Resolver.visit_Attribute`

| self | node | return |
|:----:|:----:|:------:|
| `Self` | `ast.Attribute` | `ast.AST` |

Remove `typing.*` prefix of annotation.

#### Resolver.visit_Constant()

*Full name:* `apimd.parser.Resolver.visit_Constant`

| self | node | return |
|:----:|:----:|:------:|
| `Self` | `ast.Constant` | `ast.AST` |

Check string is a name.

#### Resolver.visit_Name()

*Full name:* `apimd.parser.Resolver.visit_Name`

| self | node | return |
|:----:|:----:|:------:|
| `Self` | `ast.Name` | `ast.AST` |

Replace global names with its expression recursively.

#### Resolver.visit_Subscript()

*Full name:* `apimd.parser.Resolver.visit_Subscript`

| self | node | return |
|:----:|:----:|:------:|
| `Self` | `ast.Subscript` | `ast.AST` |

Replace `Union[T1, T2, ...]` as T1 | T2 | ...

### table()

*Full name:* `apimd.parser.table`

| *titles | items | return |
|:-------:|:-----:|:------:|
| `str` | <code>collections.abc.Iterable[str &#124; Iterable[str]]</code> | `str` |

Create multi-column table with the titles.

## Module `apimd.pep585`

| Constants | Type |
|:---------:|:----:|
| `PEP585` | `dict[str, str]` |

Implementation of PEP585 deprecated name alias.
