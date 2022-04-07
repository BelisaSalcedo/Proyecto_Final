from flask import Flask

app = Flask(__name__)
app.secret_key=b'superguay'

URL_TASA_ESPECIFICA = "https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}"

from balance import routes

