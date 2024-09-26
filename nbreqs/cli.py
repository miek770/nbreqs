import rich_click as click
from pathlib import Path

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
from importlib.metadata import version, PackageNotFoundError

# Global variable
ext: str = ".ipynb"


@click.command()
@click.argument("path")
@click.option(
    "-p",
    "--pin",
    type=bool,
    default=False,
    help="Pin dependencies to the currently installed version, if any.",
)
def main(path: str, pin: bool):
    dir: Path = Path(path)

    if not dir.exists():
        print(f"Invalid path: {dir}")
        return 1  # Exit with error

    explore_directory(dir, pin)


def explore_directory(dir: Path, pin: bool):
    for nb in dir.rglob(f"*{ext}"):
        process_notebook(nb, pin)


def process_notebook(nb: Path, pin: bool):
    with open(nb, "r", encoding="utf-8") as f:
        nb_content = nbformat.read(f, as_version=4)

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
    with open(Path(f"{nb._str.strip(ext)}_requirements.txt"), "w") as req_file:
        for lib in ext_libs:
            if pin:
                lib_version = get_installed_version(lib)
                if lib_version is None:
                    req_file.write(f"{lib}\n")
                else:
                    req_file.write(f"{lib}=={lib_version}\n")
            else:
                req_file.write(f"{lib}\n")


def filter_out_std_libs(imported_libs: set) -> list:
    std_libs = stdlib_list(f"{sys.version_info.major}.{sys.version_info.minor}")
    return sorted([lib for lib in imported_libs if lib not in std_libs])


def get_installed_version(lib_name: str) -> str:
    try:
        return version(lib_name)

    except PackageNotFoundError:
        return None


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
