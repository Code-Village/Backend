import os
from flask import Flask, jsonify
from flask_restx import Api, Resource, reqparse
from dotenv import load_dotenv
from api.hello import Hello

load_dotenv()

app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'full'
api = Api(app, version=0.1, title="Code Village", description="API for {Code Village}", terms_url="/",  contact="dltjrrbs2020@gmail.com", license='BSD 3-Clause "New" or "Revised" License')
api.add_namespace(Hello, '/hello')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    if port == 5000:
        app.run(host="0.0.0.0", port=port, debug=True)
    app.run(host="0.0.0.0", port=port)