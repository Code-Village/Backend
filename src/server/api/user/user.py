import os
from flask import request
from flask_restx import Resource, Namespace, reqparse
from dotenv import load_dotenv
import requests

load_dotenv()

User = Namespace(
    name="User",
    description="User Read,Update,Delete API",
)

get_parser = reqparse.RequestParser()
get_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 검색할 값이 있는 열')
get_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 검색할 값')

put_parser = reqparse.RequestParser()
put_parser.add_argument('id', type=str, required=True, help="데이터베이스에서 변경하고자 하는 유저의, 아이디")
put_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 변경할 값이 있는 열')
put_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 변경할 값')

del_parser = reqparse.RequestParser()
del_parser.add_argument('id', type=str, required=True, help='데이터베이스에서 삭제할 아이디')

@User.route('')
class UserClass(Resource):
    def __init__(self, api=None):
        super().__init__(api)
        self.DB_URL = os.getenv("DB_URL") + "/user"
        
    @User.doc(
        parser=get_parser,
        responses={
            200: "CONNECT",
            500: "DB_CONNECTION_ERROR"
        })
    def get(self):
        """user 정보를 가져옴"""
        args = request.args
        try:                                             
            res = requests.get(self.DB_URL, params={'col': args['col'],
                                                    'data': args['data']})
            return res.json(), 200
        except:
            return 500
    

    @User.doc(
        parser=put_parser,
        responses={
            200: "CONNECT",
            500: "DB_CONNECTION_ERROR"
        })
    def put(self):
        """user 정보를 수정함 (단, id 제외)"""
        args = request.args
        try:
            res = requests.put(self.DB_URL, params={'id': args["id"],
                                                    'col': args['col'],
                                                    'data': args["data"]})
            return "SUCCESS", 200
        except:
            return 500
        
    @User.doc(
        parser=del_parser,
        responses={
            200: "CONNECT",
            500: "DB_CONNECTION_ERROR"
        })
    def delete(self):
        """user를 삭제함"""
        args = request.args
        try:      
            res = requests.put(f"{self.DB_URL}/user", params={'id': args["id"]})
            return "SUCCESS", 200
        except:
            return 500
    