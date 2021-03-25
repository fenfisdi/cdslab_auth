---
# CDSLab Auth
---

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

If you are not using any of the previously mention distros, then do as follows
(Otherwise change `python3` -> `python`):

```shell
python3 -m venv venv_cdslab_auth
```
This creates a virtual environment on the folder we mentioned previously, after
that we need to activate it so that the prompt has access to it whenever needed.
This gets done by executing:

```shell
source venv_cdslab_auth/bin/activate
```

on Linux/Mac, or

```shell
venv_cdslab_auth\Scripts\activate.bat
```

on Windows.

### Required packages installation

Now, in order to use the library, we need to install all of the required
packages. `cd` into `venv_cdslab_auth` and follow the steps bellow:

#### Conda

Do `ls` from within the prompt, there should be a list of the files inside the
folder, one of them is called `requirements.yml` this is a _YAML_ file, and it
is in charge of telling Conda which packages to install inside the virtual
environment and which python version 

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

### Database setup

The library uses [MongoDB](https://www.mongodb.com/try/download/community).

 as the database management,
**CDSLab Auth** requires [MongoDB](https://www.mongodb.com/try/download/community).

Once you install **MongoDB**, just execute it.

```shell
mongod
```

The server should start, if it doesn't then refer to official documentation in
order to solve it, otherwise **CDSLab Auth** won't be able to connect with the
database.

### Configuration files setup

#### Database configuration file

To configure the connection to the database you must enter the parameters in
the file `db_config.cfg`, this includes the `host` and `port` used by `mongodb`
and you can assign a name to the database and to the collection where the users
will be saved.

#### Email configuration file

Now you must configure the `send_email.cfg` file for the automatic sending
registration email to users, for this you must enter the parameters of a gmail
account from which the message will be sent, this includes the password,
the account name, the subject of the message and the answer that you want to
see as a response.

#### Environment configuration

The `.env` file contains the paths of the endpoints used by the main app. In
this file you must configure the `host` and `port` that `uvicorn` will use, and
you can name the application path as you like.

#### Secrets file configuration

The `.secrets` file contains the specifications `python-jose` and `passlib`
will use to encrypt the user password and tokenize the parameters like email.
You must specify your secret key, algorithm and expiration time for the token
generated by `python-jose`, aditional you must specify the cryptcontext
parameters used by `passlib` (for more information please visit
[passlib.context - CryptContext Hash Manager](https://passlib.readthedocs.io/en/stable/lib/passlib.context.html),
[JSON Web Signature](https://python-jose.readthedocs.io/en/latest/jws/index.html)
)

Once you have finished with these configurations, then your app will be ready!!

The final step is run the application with help of uvicorn, for this just type:

```shell
uvicorn main:app --host YOUR_HOST --port YOUR_PORT --reload
```
