from copyreg import constructor
from flask import request
from flask_restx import Resource, Namespace, fields
from dotenv import load_dotenv
import requests

load_dotenv()

Nickname = Namespace(
    name="Nickname",
    description="Database로부터 Nickname을 받아오는 API",
)

nickname_put_fields = Nickname.model('Nickname', {  # Model 객체 생성
    'data': fields.String(description='column에서 검색할 값', required=True)
})

@Nickname.route('')
@Nickname.doc(params={'data': 'column에서 검색할 값'})
class NicknameGet(Resource):
    def __init__(self, DB_URL):
        self.DB_URL = DB_URL
        
    @Nickname.response(200, "Success")
    @Nickname.response(500, 'Server Closed')
    def get(self):
        """Database로부터 nickname을 가져옴"""
        args = request.args
        try:                                             
            res = requests.get(f"{self.DB_URL}/user", params={'col': 'nickname',
                                                     'data': args['data']})
            return res, 200
        except:
            return 500
    
