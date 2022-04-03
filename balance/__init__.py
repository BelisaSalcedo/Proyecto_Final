from flask import Flask

app = Flask(__name__)
app.secret_key=b'superguay'
from balance import routes