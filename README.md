# nbreqs

***WORK IN PROGRESS - NOT READY FOR USE***

`nbreqs` is a lightweight Python tool designed to extract the external library dependencies from Jupyter notebooks.

I'm working on this library because I manage repositories of notebooks with `poetry`, whereas users will only use single notebooks and copy them to other directories not managed by `poetry`. They thus need requirements files specific to each notebook instead of the repository's requirements.

## Features

- Extracts only external dependencies (ignores standard library modules).
- Works on Jupyter notebooks.
- Generates minimal `<notebook>_requirements.txt` files (one per notebook).
  
## Installation

***TO BE DETERMINED***

## How It Works

`nbreqs` parses the Python code in memory, extracts all external libraries using `ast`, and filters out any standard library modules. It then queries the installed version of each library without needing to import them into your environment.

## Development

***MAYBE LATER***

## License

`nbreqs` is licensed under the MIT License.