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

| name | root | return |
|:----:|:----:|:------:|
| `str` | `str` | `str` |

Package searching algorithm.

## Module `apimd.parser`

Data structures.

### class Parser

*Full name:* `apimd.parser.Parser`

| Decorators |
|:----------:|
| `@dataclass` |

### Parser.api()

*Full name:* `apimd.parser.Parser.api`

| self | name | node | prefix | return |
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

### Parser.parser()

*Full name:* `apimd.parser.Parser.parser`

| self | name | script | return |
|:----:|:----:|:------:|:------:|
| `Self` | `str` | `str` | `None` |

Main parser of the entire module.

### is_public_family()

*Full name:* `apimd.parser.is_public_family`

| name | return |
|:----:|:------:|
| `str` | `bool` |

Check the name is come from public modules or not.

### table_annotation()

*Full name:* `apimd.parser.table_annotation`

| args | return |
|:----:|:------:|
| `Sequence[arg]` | `str` |

Annotations of the table.

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
