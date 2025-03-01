[![CircleCI](https://circleci.com/gh/digitalfabrik/integreat-cms.svg?style=shield)](https://circleci.com/gh/digitalfabrik/integreat-cms)
[![Pylint](https://img.shields.io/badge/pylint-10.00-brightgreen)](https://www.pylint.org/)
![Coverage](https://img.shields.io/codeclimate/coverage/digitalfabrik/integreat-cms)
[![PyPi](https://img.shields.io/pypi/v/integreat-cms.svg)](https://pypi.org/project/integreat-cms/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Integreat Django CMS

[![Logo](.github/logo.png) Integreat - The mobile guide for newcomers.](https://integreat-app.de/en/) Multilingual. Offline. Open Source.

This content management system helps local integration experts to provide multilingual information for newcomers.

## TL;DR

### Prerequisites

Following packages are required before installing the project (install them with your package manager):

* npm version 7 or higher
* nodejs version 12 or higher
* python3.9 (Debian-based distributions) / python39 (Arch-based distributions)
* python3.7-dev (only on Ubuntu)
* python3-pip (Debian-based distributions) / python-pip (Arch-based distributions)
* pipenv for python3 (if no recent version is packaged for your distro, use `pip3 install pipenv --user`)
* gettext to use the translation features
* Either postgresql **or** docker to run a local database server

### Installation

````
git clone git@github.com:digitalfabrik/integreat-cms.git
cd integreat-cms
./dev-tools/install.sh
````

### Run development server

````
./dev-tools/run.sh
````

* Go to your browser and open the URL `http://localhost:8000`
* Default user is "root" with password "root1234".

## Documentation

For detailed instructions, tutorials and the source code reference have a look at our great documentation:

<p align="center">:notebook: https://digitalfabrik.github.io/integreat-cms/</p>


## License

This project is licensed under the Apache 2.0 License, see [LICENSE.txt](./LICENSE.txt)

All files in [./integreat_cms/static/src/logos/](./integreat_cms/static/src/logos/) are not covered by this license and may only be used with specific permission of the copyright holder.
