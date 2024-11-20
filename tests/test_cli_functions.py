from nbreqs.cli import filter_out_std_libs, is_on_pypi, main
from os import mkdir, rmdir
from pathlib import Path
from click.testing import CliRunner, Result


invalid_lib: str = "dasoie;oihag;oiehge"


def test_filter_out_std_libs() -> None:
    libs: set = {
        "numpy",
        "click",
        "pathlib",
    }
    assert filter_out_std_libs(libs) == [
        "click",
        "numpy",
    ]


def test_is_not_on_pypi() -> None:
    assert is_on_pypi(invalid_lib) is False


def test_is_on_pypi() -> None:
    assert is_on_pypi("click") is True


def test_cli_file_path() -> None:
    file_path: str = "tests/cli_file_path.ipynb"
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(main, [file_path])
    assert result.exit_code == 0
