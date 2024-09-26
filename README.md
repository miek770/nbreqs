# nbreqs

***WORK IN PROGRESS - NOT READY FOR USE***

`nbreqs` is a lightweight Python tool designed to extract the external library dependencies from Jupyter notebooks.

I'm working on this tool because I manage repositories of notebooks with `poetry`, whereas users will only use single notebooks and copy them to other directories not managed by `poetry`. They thus need requirement files specific to each notebook instead of the repository's total requirements.

## Features

- Extracts only external dependencies (ignores standard library modules).
- Works on Jupyter notebooks.
- Generates minimal `<notebook>_requirements.txt` files (one per notebook).

## Installation

The preferred way of installing this tool is through `pipx`:

`pipx install nbreqs`

There is currently no other supported installation method.

## Usage

***TO BE DEVELOPPED***

Once installed, the utility is used on the command line; see `--help` for details:

```shell
$ py nbreqs/cli.py --help

 Usage: cli.py [OPTIONS] PATH

╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --pin   -p    Pin dependencies to the currently installed version, if any.                                                                          │
│ --help        Show this message and exit.                                                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Development

Contributions are welcome; please:

- Use `black`.
- Ensure `pytest` runs without failures.
- Be nice.

## License

`nbreqs` is licensed under the MIT License. See LICENSE file for details.
