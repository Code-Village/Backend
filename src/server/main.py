import os
from flask import Flask
from flask_restx import Api

from src.server.api import *

app = Flask(__name__)

# API 문서 전부 펼치기
# app.config.SWAGGER_UI_DOC_EXPANSION = 'full'

api = Api(
    app,
    version=0.1, 
    title="Code Village", 
    description="API for {Code Village}", 
    terms_url="/",
    contact="dltjrrbs2020@gmail.com", 
    license='BSD 3-Clause "New" or "Revised" License'
)

api.add_namespace(Hello, "/hello")
api.add_namespace(User, "/user")
api.add_namespace(RegistUser, "/user/regist")
api.add_namespace(Team, "/team")
api.add_namespace(RegistTeam, "/team/regist")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
