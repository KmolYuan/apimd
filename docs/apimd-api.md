# apimd API

## Module `apimd`

A Python API compiler for universal Markdown syntax.

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

### find()

*Full name:* `apimd.loader.find`

| path | return |
|:----:|:------:|
| `str` | `str` |

Return file path if existed.

### gen_api()

*Full name:* `apimd.loader.gen_api`

| root_names | pwd | * | prefix | dry | return |
|:----------:|:---:|:---:|:------:|:---:|:------:|
| `dict[str, str]` | `str` |   | `str` | `bool` | `Sequence[str]` |
|   | '.' |   | 'docs' | False |   |

Generate API. All rules are listed in the readme.

### loader()

*Full name:* `apimd.loader.loader`

| root_name | root | return |
|:---------:|:----:|:------:|
| `str` | `str` | `str` |

Package searching algorithm.

## Module `apimd.parser`

Data structures.

### code()

*Full name:* `apimd.parser.code`

| doc | return |
|:---:|:------:|
| `str` | `str` |

Escape Markdown charters from code.

### esc_usc()

*Full name:* `apimd.parser.esc_usc`

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
'\n'.join(interpret_mode(">>> print(\"Hello\")"))
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

### names_cmp()

*Full name:* `apimd.parser.names_cmp`

| s | return |
|:---:|:------:|
| `str` | `tuple[bool, str]` |

Name comparison function.

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

### class Parser

*Full name:* `apimd.parser.Parser`

| Decorators |
|:----------:|
| `@dataclass` |

| Members | Type |
|:-------:|:----:|
| `alias` | `dict[str, str]` |
| `all` | `set[str]` |
| `doc` | `dict[str, str]` |
| `docstring` | `dict[str, str]` |

#### Parser.api()

*Full name:* `apimd.parser.Parser.api`

| self | root | node | * | prefix | return |
|:----:|:----:|:----:|:---:|:------:|:------:|
| `Self` | `str` | <code>ast.FunctionDef &#124; ast.AsyncFunctionDef &#124; ast.ClassDef</code> |   | `str` | `None` |
|   |   |   |   | '' |   |

Create API doc for only functions and classes.
Where `name` is the full name.

#### Parser.class_api()

*Full name:* `apimd.parser.Parser.class_api`

| self | name | body | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | `list[ast.stmt]` | `None` |

Create class API.

#### Parser.compile()

*Full name:* `apimd.parser.Parser.compile`

| self | return |
|:----:|:------:|
| `Self` | `str` |

Compile doc.

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

#### Parser.parser()

*Full name:* `apimd.parser.Parser.parser`

| self | root | script | return |
|:----:|:----:|:------:|:------:|
| `Self` | `str` | `str` | `None` |

Main parser of the entire module.

#### Parser.resolve()

*Full name:* `apimd.parser.Parser.resolve`

| self | root | old_node | return |
|:----:|:----:|:--------:|:------:|
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

Set up global type alias.

### class Resolver

*Full name:* `apimd.parser.Resolver`

| Bases |
|:-----:|
| `NodeTransformer` |

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

Remove `typing.*` annotation.

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
