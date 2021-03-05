# CDSLab Auth

This is the Authentication API for CDSLab.

## Environment setup

### Create `venv_cdslab_auth` environment

Create an environment in your local folder that contains the cloned repository

If you are using `conda` package managment type the following comands (please
be aware that `venv_cdslab_auth` is the default environment name of this repo.
Don't change it):

```shell
conda create --name venv_cdslab_auth
conda activate venv_cdslab_auth
```

Otherwise, if you are using `pip` type:

```shell
python3 -m venv venv_cdslab_auth
```

For activating the environment, if you are on Linux or MAC, then type:

```shell
source venv_cdslab_auth/bin/activate
```

Otherwise, if you are on windows, then type:

```shell
venv_cdslab_auth\Scripts\activate.bat
```

### Required packages installation

Install packages used by **CDSLab Auth**

If you are using `conda`, then you must install the packages using
`requirements.yml` file:

```shell
conda env update -n venv_cdslab_auth --file requirements.yml
```

Otherwise, if you are using `pip`, then you must install the packages using 
`requirements.txt` file:

```shell
pip install -r requirements.txt
```

### Database setup

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


To configure the connection to the database you must enter the parameters in the file `db_config.cfg`, this includes the host and port used by mongodb and you can assign a name to the database and to the collection where the users will be hosted

#### Email configuration file

Now you must configure the `send_email.cfg` file for the automatic sending registration email to users, for this you must enter the parameters of a gmail account from which the message will be sent, this includes the password, the account name, the subject of the message and the answer that you want to see as a response.


#### Environment configuration

The `.env` file contains the paths of the endpoints used by the main file, in this file you need to configure the host and port that uvicorn will use, and you can name the application path as you like

#### Secrets file configuration

The `.secrets` file contains the specifications python-jose and passlib will use to encrypt the password user and tokenize the parameters like email, for this you need to specify your secret key, algorithm and expiration time for the token generated by python-jose, aditional you need sepecify the cryptocontext parameters used by passlib, for more information please visit https://passlib.readthedocs.io/en/stable/lib/passlib.context.html, https://python-jose.readthedocs.io/en/latest/jws/index.html

With this your configuration is ready to run the app!!

The final step is run the application with help of uvicorn, for this just type:

```shell
uvicorn main:app --host YOUR_HOST(without quotation marks "") --port YOUR_PORT(without quotation marks "") --reload
```
    
