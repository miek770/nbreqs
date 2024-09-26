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

# To get libraries' version without importing them
from importlib.metadata import version, PackageNotFoundError


@click.command()
@click.argument("path")
def main(path: str):
    dir: Path = Path(path)
    ext: str = ".ipynb"

    if not dir.exists():
        print(f"Invalid path: {dir}")
        return 1  # Error

    for nb in dir.rglob(f"*{ext}"):
        print(f"Converting {nb} to Python...")

        with open(nb, "r", encoding="utf-8") as f:
            nb_content = nbformat.read(f, as_version=4)

        py_exporter = PythonExporter()
        py_code, _ = py_exporter.from_notebook_node(nb_content)

        tree = ast.parse(py_code)
        imported_libs = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_libs.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_libs.add(node.module.split(".")[0])

        ext_libs = filter_out_std_libs(imported_libs)
        with open(Path(f"{nb._str.strip(ext)}_requirements.txt"), "w") as req_file:
            for lib in ext_libs:
                lib_version = get_installed_version(lib)
                if lib_version is None:
                    req_file.write(f"{lib}\n")
                else:
                    req_file.write(f"{lib}=={lib_version}\n")


def filter_out_std_libs(imported_libs: set) -> set:
    std_libs = stdlib_list(f"{sys.version_info.major}.{sys.version_info.minor}")
    return {lib for lib in imported_libs if lib not in std_libs}


def get_installed_version(lib_name: str) -> str:
    try:
        # Get the installed version of the package
        return version(lib_name)
    except PackageNotFoundError:
        return None


if __name__ == "__main__":
    main()
