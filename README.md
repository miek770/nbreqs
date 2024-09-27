# nbreqs

`nbreqs` is a lightweight Python tool designed to extract the external library dependencies from Jupyter notebooks.

I made this tool because I manage repositories containing several notebooks with `poetry`, whereas users will only use single notebooks and copy them to other directories not themselves managed by `poetry`. They thus need requirement files specific to each notebook instead of the repository's total requirements.

`nbreqs` generates a `<notebook>_requirements.txt` file for each notebook in the same directory as each notebook.

## Features

- Finds notebooks recursively starting at the provided `PATH`.
- Extracts only external dependencies found on PyPI (ignores standard library modules and sources other than PyPI).
- Works on Jupyter notebooks.
- Generates minimal `<notebook>_requirements.txt` files (one per notebook).

## Installation

The preferred way of installing this tool is through `pipx`:

`pipx install nbreqs`

It can also be installed as a library through `pip`; check the tests for examples.

## Usage

Once installed, the utility is used on the command line; see `--help` for details:

[![asciicast](https://asciinema.org/a/677950.svg)](https://asciinema.org/a/677950)

## Development

Contributions are welcome; please:

- Activate `pre-commit` and use `black`.
- Ensure `pytest` runs without failures.
- Be nice.

## License

`nbreqs` is licensed under the MIT License. See LICENSE file for details.
