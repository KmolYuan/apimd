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

### gen_api()

*Full name:* `apimd.loader.gen_api`

| root_names | pwd | prefix | dry | return |
|:----------:|:---:|:------:|:---:|:------:|
| `dict[str, str]` | `str` | `str` | `bool` | `Sequence[str]` |
|   | '.' | 'docs' | False |   |

Generate API. All rules are listed in the readme.

### loader()

*Full name:* `apimd.loader.loader`

| name | stubs | root | return |
|:----:|:-----:|:----:|:------:|
| `str` | `str` | `str` | `str` |

Package searching algorithm.

## Module `apimd.parser`

Data structures.

### class Parser

*Full name:* `apimd.parser.Parser`

| Decorators |
|:----------:|
| `@dataclass` |

| Members | Type |
|:-------:|:----:|
| `alias` | `dict[str, str]` |
| `doc` | `dict[str, str]` |

### Parser.api()

*Full name:* `apimd.parser.Parser.api`

| self | root | node | prefix | return |
|:----:|:----:|:----:|:------:|:------:|
| `Self` | `str` | `Union[FunctionDef, ClassDef]` | `str` | `None` |
|   |   |   | '' |   |

Create API doc for only functions and classes.
Where `name` is the full name.

### Parser.compile()

*Full name:* `apimd.parser.Parser.compile`

| self | return |
|:----:|:------:|
| `Self` | `str` |

Compile doc.

### Parser.globals()

*Full name:* `apimd.parser.Parser.globals`

| self | root | node | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | `Union[Assign, AnnAssign]` | `None` |

Assign globals.

### Parser.imports()

*Full name:* `apimd.parser.Parser.imports`

| self | root | node | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | `Union[Import, ImportFrom]` | `None` |

Save import names for 'typing.TypeAlias'.

### Parser.parser()

*Full name:* `apimd.parser.Parser.parser`

| self | root | script | return |
|:----:|:----:|:------:|:------:|
| `Self` | `str` | `str` | `None` |

Main parser of the entire module.

### Parser.table_annotation()

*Full name:* `apimd.parser.Parser.table_annotation`

| self | root | args | return |
|:----:|:----:|:----:|:------:|
| `Self` | `str` | `Sequence[arg]` | `str` |

Annotations of the table.

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

### is_public_family()

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

One column table.

### table_blank()

*Full name:* `apimd.parser.table_blank`

| n | return |
|:---:|:------:|
| `int` | `str` |

Blanks of the table.

### table_literal()

*Full name:* `apimd.parser.table_literal`

| args | return |
|:----:|:------:|
| `Sequence[Optional[expr]]` | `str` |

Literals of the table.

### table_split()

*Full name:* `apimd.parser.table_split`

| args | return |
|:----:|:------:|
| `Sequence[arg]` | `str` |

The split line of the table.

### table_titles()

*Full name:* `apimd.parser.table_titles`

| args | return |
|:----:|:------:|
| `Sequence[arg]` | `str` |

Names of the table.
