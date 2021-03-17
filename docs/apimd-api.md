# apimd API

## Module `apimd`

A Python API compiler for universal Markdown syntax.

### gen_api()

*Full name:* `apimd.gen_api`

| root_names | pwd | * | prefix | level | dry | return |
|:----------:|:---:|:---:|:------:|:-----:|:---:|:------:|
| `dict[str, str]` | <code>str &#124; None</code> |   | `str` | `int` | `bool` | `Sequence[str]` |
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
| `str` | `str` | `Iterator[tuple[str, str]]` |

Walk packages without import them.

## Module `apimd.parser`

Data structures.

### code()

*Full name:* `apimd.parser.code`

| doc | return |
|:---:|:------:|
| `str` | `str` |

Escape Markdown charters from code.

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
| `str` | `Iterator[str]` |

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

### list_table()

*Full name:* `apimd.parser.list_table`

| title | listed | return |
|:-----:|:------:|:------:|
| `str` | `Iterator[str]` | `str` |

Create one column table with a title.

### class Parser

*Full name:* `apimd.parser.Parser`

| Decorators |
|:----------:|
| `@dataclasses.dataclass` |

| Members | Type |
|:-------:|:----:|
| `alias` | `dict[str, str]` |
| `b_level` | `int` |
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

| self | root | name | body | return |
|:----:|:----:|:----:|:----:|:------:|
| `Self` | `str` | `str` | `list[ast.stmt]` | `None` |

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

#### Parser.imports()

*Full name:* `apimd.parser.Parser.imports`

| self | root | node | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | <code>ast.Import &#124; ast.ImportFrom</code> | `None` |

Save import names for 'typing.*'.

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

#### Parser.table_annotation()

*Full name:* `apimd.parser.Parser.table_annotation`

| self | root | args | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | `Sequence[ast.arg]` | `str` |

Annotations of the table.

#### Parser.type_alias()

*Full name:* `apimd.parser.Parser.type_alias`

| self | root | node | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | <code>ast.Assign &#124; ast.AnnAssign</code> | `None` |

Set up global type alias and public names.

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

### table_literal()

*Full name:* `apimd.parser.table_literal`

| args | return |
|:----:|:------:|
| <code>Sequence[expr &#124; None]</code> | `str` |

Literals of the table.

### table_split()

*Full name:* `apimd.parser.table_split`

| args | return |
|:----:|:------:|
| `Sequence[ast.arg]` | `str` |

The split line of the table.
