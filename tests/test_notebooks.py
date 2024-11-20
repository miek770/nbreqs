from nbreqs.cli import process_notebook
from pathlib import Path


# Global variable
ext: str = "ipynb"


def test_basic_imports() -> None:
    dir: str = "tests"
    file: str = "basic_imports"

    nb: Path = Path(f"{dir}/{file}.{ext}")
    process_notebook(nb=nb, quiet=True, verbose=False, dry_run=False)
    with open(f"{dir}/{file}_requirements.txt", "r") as reqs:
        assert reqs.readlines() == [
            "nbconvert\n",
            "numpy\n",
            "pandas\n",
            "rich_click\n",
            "sklearn\n",
            "stdlib_list\n",
        ]


def test_latex_cell() -> None:
    dir: str = "tests"
    file: str = "latex_cell"

    nb: Path = Path(f"{dir}/{file}.{ext}")
    process_notebook(nb=nb, quiet=True, verbose=False, dry_run=False)
    with open(f"{dir}/{file}_requirements.txt", "r") as reqs:
        assert reqs.readlines() == [
            "pytest\n",
        ]


def test_non_pypi_pkg() -> None:
    dir: str = "tests"
    file: str = "non_pypi_pkg"

    nb: Path = Path(f"{dir}/{file}.{ext}")
    process_notebook(nb=nb, quiet=True, verbose=False, dry_run=False)
    with open(f"{dir}/{file}_requirements.txt", "r") as reqs:
        assert reqs.readlines() == []
