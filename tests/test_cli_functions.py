from nbreqs.cli import filter_out_std_libs, is_on_pypi
from os import mkdir, rmdir
from pathlib import Path


invalid_lib = "dasoie;oihag;oiehge"


def test_filter_out_std_libs():
    libs = {
        "numpy",
        "click",
        "pathlib",
    }
    assert filter_out_std_libs(libs) == [
        "click",
        "numpy",
    ]


def test_is_not_on_pypi():
    assert is_on_pypi(invalid_lib) is False


def test_is_on_pypi():
    assert is_on_pypi("click") is True
