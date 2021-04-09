# CDSLab Auth

This API constitutes the authentication module used in CDSLab.

## Environment setup

We recommend using a local python environment to avoid messing with the global
installation. In the following process we will go through the process of
creating such environment (generally known as _virtual environment_) and it will
be named *venv_cdslab_auth*.

---
### Creation of `venv_cdslab_auth`

Whether you use Python installed locally (the usual case for Linux users) or you
prefer to manage your installations using Conda, the creation of the environment
is straight forward, and this guide covers a great amount of the base cases.

The first step to begin this process is to create a folder wherever you prefer,
but it would be better if it is accessible with ease. In our case, we will call
it _venv_cdslab_auth_, as previously mentioned. It will be localized on the same
folder as the one where this repository is located at.

---
After this point, Conda users and Python users have to follow slightly different
steps.
---

#### Conda Users:

The first step is to open a terminal that has access to Conda
* *Windows:* Execute `Conda Prompt` from the start menu.
* *Linux/Mac:* Launch any terminal that you have accessible.

Now, the creation of virtual environment is as easy as just typing the following
commands:

```shell
conda create --name venv_cdslab_auth
conda activate venv_cdslab_auth
```

Which creates a virtual environment inside the folder we created on the previous
section and activates it so that it gets detected by the prompt when you launch
it.

#### Vanilla Python 3 User:

Virtual environments are just as easy to create as when using Conda, there are
only some slightly differences. We will asume the usage of Python 3, as the
library is intended to work on this version. Most Python installation use
`python3` as the command to execute processes within Python 3, but there are
some Linux distribution that prefer the usage of `python`, such as:
* Arch Linux
* Manjaro
* Gentoo

If you are not using any of the previously mentioned distros, then do as follows
(Otherwise change `python3` -> `python`):

```shell
python3 -m venv venv_cdslab_auth
```
This creates a virtual environment on the folder we mentioned previously, after
that we need to activate it so that the prompt has access to it whenever needed.
This gets done by executing:

```shell
src venv_cdslab_auth/bin/activate
```

on Linux/Mac, or

```shell
venv_cdslab_auth\Scripts\activate.bat
```

on Windows.

---
### Installation of required libraries

Now, in order to use the library, we need to install all of the required
packages. `cd` into `venv_cdslab_auth` and follow the steps bellow:

#### Conda

Do `ls` from within the prompt, there should be a list of the files inside the
folder, one of them is called `requirements.yml` this is a _YAML_ file, and it
is in charge of telling Conda which packages to install inside the virtual
environment and which python version to use

```shell
conda env update -n venv_cdslab_auth --file requirements.yml
```

When managing packages locally without Conda, the alternative is to use *Pip*
which is the official way to manage python libraries outside _Python Base_.
Pip comes preinstalled within the Python package for Windows, as for Linux it
can be installed using the package manager of your distro, while on Mac there is
not a unique way of doing it, but internet has lot of wonderful tutorials about
it, be our guest. The process is a little simpler, from the prompt execute:

```shell
pip install -r requirements.txt
```

---
### Database setup

The library uses [MongoDB](https://www.mongodb.com/try/download/community) to
manage the databases. MongoDB is a very mature protocol, so we don't consider
necessary to add extra steps, rather, the basic ideas. Once installed, it is
only needed to run:

```shell
mongod
```

This should start a deamon (server), in case any error appears, consult the
official documentation on how to solve it, otherwise using this library will not
be possible.

---
### Configuration files setup

#### Database configuration file

Connection to the database is done by configuring the parameters inside the file
`.db_config`, an example file called `.db_config_example`, rename it and
add the necessary data, this file includes fields such as `host` and `port`
which are *necessary* for MongoDB to function. Inside this configuration you can
also modify the collections used if needed.

#### Email configuration file

Every time a user gets created, a confirmation emails needs to be issued, in
order to do so, a file called `.email_config` is needed, an example file called
`.email_config_example` is included inside the repo, modify the fields
accordingly.

#### Environment configuration

The `.env` file hosts the endpoint paths used in the main _application_. This
file needs to be modified manually to add the `host` and `port` fields, which
are needed by `uvicorn`. This also allows you to change the name of the
application as desired.

#### Secrets configuration

The `.secrets` file contains the required specifications for both `python-jose`
and `passlib`, this will be used to encrypt the sensible data such as user
_passwords_ and to tokenize the email component.

A **secret* key must be specified, the algorithm which was used to generate it
and the respective expiration time each token should have. Additionally, you can
specify the _cryptcontext_ used by `passlib` (More information on this subject
can be found at: [passlib.context - CryptContext Hash Manager](https://passlib.readthedocs.io/en/stable/lib/passlib.context.html),
[JSON Web Signature](https://python-jose.readthedocs.io/en/latest/jws/index.html)
)

---

Once everything is finished, the application should be ready to run, a final
step is needed to start it. Once again, inside the prompt, we will use `uvicorn`
to start everything, like so:

```shell
uvicorn main:app --host YOUR_HOST --port YOUR_PORT --reload
```
**You're set.**
