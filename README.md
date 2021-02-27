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

Now, you need to configure the .env file, for this please remove the "_example" from the .env_examples file, do the same with the .secrets_example and config_examples.cfg

    * Inside .env file please configure the host and the port that you want to use, if you dont know wich host and port will use, you can type the next comand on your comand window

            uvicorn main:app --reload
    
    After that the first line gives you the host and port that uvicorn uses by defult on your machine. You can assign any string that you want to the endpoints paths

    * Inside config.cfg write the host and port that mongo will use, aditional specify the database and collection that the API will use, finally configure the sended email as you want changing only the fileds written in capital letters

    * Inside .secrets file you need the sepecifications schemes and keys used by passlib and python-jose libraries, please chek the next documentation for more information.
    https://passlib.readthedocs.io/en/stable/lib/passlib.context.html
    https://python-jose.readthedocs.io/en/latest/jws/index.html

With this your configuration is ready to run the app!!
The final step is run the main.py script in the browser just add /docs to your uvicorn path to 
    
