# Fichero env_template 
- copiar el fichero y renombrarlo a .env
- este fichero sirve para indicar en que entorno estamos trabajando, como no tenemos la aplicación subida a un servidor web real poner el entorno development
# Fichero Config
- copiar el config_template.py y renonbrarlo a config.py
- Hay que rellenar una serie de datos:
    * APi Key --> se obtiene en la pagnia de coinappi para obtener una Apikey ir a la página: 'https://www.coinapi.io/'
                        Pegarla en el sitio correspondiente
    * Tienes que añadir tu SECRET_KEY en el config
    * Ruta base de datos:
        - hay un fichero llamado create_table que debes ejutar en tu bbdd para crear la tabla.
        - poner la ruta de la tabla que acabamos de poner en la parte del config.
