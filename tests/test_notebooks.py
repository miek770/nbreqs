from nbreqs.cli import process_notebook
from pathlib import Path


# Global variable
ext: str = "ipynb"


def test_basic_imports():
    dir: str = "tests"
    file: str = "basic_imports"

    nb: Path = Path(f"{dir}/{file}.{ext}")
    process_notebook(nb=nb, pin=False)
    with open(f"{dir}/{file}_requirements.txt", "r") as reqs:
        assert reqs.readlines() == [
            "nbconvert\n",
            "numpy\n",
            "pandas\n",
            "rich_click\n",
            "sklearn\n",
            "stdlib_list\n",
        ]


def test_basic_imports_pinned():
    dir: str = "tests"
    file: str = "basic_imports"

    nb: Path = Path(f"{dir}/{file}.{ext}")
    process_notebook(nb=nb, pin=True)
    with open(f"{dir}/{file}_requirements.txt", "r") as reqs:
        assert reqs.readlines() == [
            "nbconvert==7.16.4\n",
            "numpy\n",
            "pandas\n",
            "rich_click==1.8.3\n",
            "sklearn\n",
            "stdlib_list==0.10.0\n",
        ]


def test_latex_cell():
    dir: str = "tests"
    file: str = "latex_cell"

    nb: Path = Path(f"{dir}/{file}.{ext}")
    process_notebook(nb=nb, pin=False)
    with open(f"{dir}/{file}_requirements.txt", "r") as reqs:
        assert reqs.readlines() == [
            "pytest\n",
        ]


def test_latex_cell_pinned():
    dir: str = "tests"
    file: str = "latex_cell"

    nb: Path = Path(f"{dir}/{file}.{ext}")
    process_notebook(nb=nb, pin=True)
    with open(f"{dir}/{file}_requirements.txt", "r") as reqs:
        assert reqs.readlines() == [
            "pytest==8.3.3\n",
        ]
