# comics

Comic Archive Toolkit

## Setup

The toolkit can be setup in one of the following ways:

- Running [install.sh](./install.sh) on local machine
- Building and running the [Dockerfile](./Dockerfile) 

## Usage

```
usage: omnibus.py [-h] [-p] [-d] path

Create omnibus archive from directory of individual issues.

positional arguments:
  path           path to directory of issues

options:
  -h, --help     show this help message and exit
  -p, --persist  persist logs to disk
  -d, --debug    show debug logs
```

The virtual environment may need to be activated if running outside of Docker.

## Development

[Launch configurations](./.vscode/launch.json) and [extension recommendations](./.vscode/extensions.json) are included for running and debugging with Visual Studio Code.