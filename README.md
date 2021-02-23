# cdslab_auth
CDSLab authentication API.  

## How to use it
1. Create an environment in your local folder that contains the cloned repository
    * For conda package managment type the following comands:
    
            -conda create --name myenv
            -conda activate myenv
    
    * For pip type:

            -python3 -m venv myenv

        *  To activate the environment, if you are on Linux or MAC type:

                -source <myenv>/bin/activate
        
        * To activate on windows type:

                -<myenv>\Scripts\activate.bat

2. Install the packages that use the authentication API
    * For conda you need to install the packages on yml file, for this type:

            -conda env update -n my_env --file cdslab_auth.yaml

    * For pip you need use the packages on requirements.txt, for that type:

            -pip install -r requirements.txt

3. The authentication API works with mongodb as a database, for this you need install mongodb      https://www.mongodb.com/try/download/community. once installed mongo just type in another comand window:

        -mongod

    You can see how the database server starts, if don´t make this, the API will never be able to conect with the database.

4. The next step is create a database and within this create the collection that will contain the user registry, for that please check the mongo documentation https://docs.mongodb.com/manual/core/databases-and-collections/#databases

5. Now, you need to configure the .env file, for this please remove the "_example" from the .env_examples file, do the same with the .secrets_example and config_examples.cfg

    * Inside .env file please configure the host and the port that you want to use, if you dont know wich host and port will use, you can type the next comand on your comand window

            uvicorn main:app --reload
    
    After that the first line gives you the host and port that uvicorn uses by defult on your machine. You can assign any string that you want to the endpoints paths

    * Inside config.cfg write the host and port that mongo will use, aditional specify the database and collection that the API will use, finally configure the sended email as you want changing only the fileds written in capital letters

    * Inside .secrets file you need the sepecifications schemes and keys used by passlib and python-jose libraries, please chek the next documentation for more information.
    https://passlib.readthedocs.io/en/stable/lib/passlib.context.html
    https://python-jose.readthedocs.io/en/latest/jws/index.html

With this your configuration is ready to run the app!!!!
    
