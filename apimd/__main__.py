# -*- coding: utf-8 -*-

"""The command line launcher of apimd."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2020"
__license__ = "MIT"
__email__ = "pyslvs@gmail.com"

from argparse import ArgumentParser


def main() -> None:
    """Main function."""
    from apimd import __version__
    ver = f"apimd {__version__}"
    parser = ArgumentParser(
        prog=ver,
        description="Compile Python public API into Generic Markdown.",
        epilog=f"{__copyright__} {__license__} {__author__} {__email__}"
    )
    parser.add_argument('-v', '--version', action='version', version=ver)
    parser.add_argument(
        'module',
        default=None,
        nargs='+',
        type=str,
        help="the module name that installed or in the current path, "
             "syntax Module-Name=module_name can specify a package name for it"
    )
    parser.add_argument(
        '-c',
        '--current',
        metavar="DIR",
        default='.',
        nargs='?',
        type=str,
        help="current directory"
    )
    parser.add_argument(
        '-d',
        '--dir',
        metavar="DIR",
        default='docs',
        nargs='?',
        type=str,
        help="output to a specific directory"
    )
    parser.add_argument(
        '--dry',
        action='store_true',
        help="print the result instead write the file"
    )
    arg = parser.parse_args()
    root_names = {}
    for m in arg.module:  # type: str
        n = m.split('=', maxsplit=1)
        if len(n) == 1:
            n.append(n[0])
        if n[1] == "":
            n[1] = n[0]
        root_names[n[0]] = n[1]
    from apimd.loader import gen_api
    gen_api(root_names, arg.current, prefix=arg.dir, dry=arg.dry)


if __name__ == '__main__':
    main()
