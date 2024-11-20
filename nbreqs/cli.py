import rich_click as click
from pathlib import Path
from typing import Optional

# To convert the notebook to Python
import nbformat
from nbconvert import PythonExporter

# To find imported modules
import ast

# To filter out standard libraries
import sys
from stdlib_list import stdlib_list

# To fitler out non-standard libraries that aren't on PyPI
import requests

# To get libraries' version without importing them
from subprocess import run

# Global variable
ext: str = ".ipynb"


@click.command()
@click.argument("path")
@click.option(
    "--quiet/--no-quiet",
    default=False,
    help="Hide non-error mesages.",
    show_default=True,
)
@click.option(
    "--verbose/--no-verbose",
    default=False,
    help="Print details during execution (overrides --quiet).",
    show_default=True,
)
@click.option(
    "--dry-run/--no-dry-run",
    default=False,
    help="Execute without creating the requirements files (implies --verbose).",
    show_default=True,
)
def main(path: str, quiet: bool, verbose: bool, dry_run: bool):
    dir: Path = Path(path)

    if not dir.exists():
        print(f"Invalid path: {dir}")
        exit(1)  # Exit with error

    # --verbose is implied with --dry-run
    if dry_run:
        verbose = True

    # --verbose overrides --quiet
    if verbose:
        quiet = False

    if dir.is_file():
        process_notebook(dir, quiet, verbose, dry_run)
    else:
        explore_directory(dir, quiet, verbose, dry_run)


def explore_directory(dir: Path, quiet: bool, verbose: bool, dry_run: bool):
    for nb in dir.rglob(f"*{ext}"):
        process_notebook(nb, quiet, verbose, dry_run)


def process_notebook(nb: Path, quiet: bool, verbose: bool, dry_run: bool):
    if not quiet:
        print(f"Generating requirements from: {nb}")

    with open(nb, "r", encoding="utf-8") as f:
        nb_content = nbformat.read(f, as_version=nbformat.NO_CONVERT)

    # Filter out anything that isn't code
    # (to prevent `ast` parsing failures)
    for cell in nb_content.cells:
        if cell.cell_type != "code":
            cell.source = ""

    py_exporter = PythonExporter()
    py_code, _ = py_exporter.from_notebook_node(nb_content)

    tree = ast.parse(py_code)
    imported_libs = set()

    # Find all imported packages
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_libs.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_libs.add(node.module.split(".")[0])

    # Remove standard packages
    ext_libs = filter_out_std_libs(imported_libs)

    # Remove non-PyPI packages
    ext_libs = [p for p in ext_libs if is_on_pypi(p)]

    # Create the requirements file
    if len(ext_libs) and not dry_run:
        with open(
            Path(f"{nb.as_posix().strip(ext)}_requirements.txt"), "w"
        ) as req_file:
            for lib in ext_libs:
                req_file.write(f"{lib}\n")

    # Print the result
    if verbose:
        if len(ext_libs):
            for lib in ext_libs:
                print(f" - {lib}")
        else:
            print(f" - No requirement from PyPI")


def filter_out_std_libs(imported_libs: set) -> list:
    std_libs = stdlib_list(f"{sys.version_info.major}.{sys.version_info.minor}")
    return sorted([lib for lib in imported_libs if lib not in std_libs])


def is_on_pypi(package_name: str) -> bool:
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code == 200:
        return True

    elif response.status_code == 404:
        return False

    else:
        raise Exception(f"Error checking package on PyPI: {response.status_code}")


if __name__ == "__main__":
    main()
