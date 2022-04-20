from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")

URL_TASA_ESPECIFICA = "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}"

from balance import routes

