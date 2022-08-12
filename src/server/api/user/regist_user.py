import os
from flask import request
from flask_restx import Resource, Namespace, reqparse
from dotenv import load_dotenv
import requests

load_dotenv() # 환경변수 로드

def switch(arg):
    res_switch = {
        200: "SUCCESS",
        201: "DUPLICATE",
        400: "DB_FATAL_ERROR",
        401: "DB_NOT_IN_DATABASE",
        500: "SERVER_CONNECTION_ERROR",
    }
    return res_switch.get(arg, "UNKNOWN") 

RegistUser = Namespace(
    name="RegistUser",
    description="회원가입 API",
)

get_parser = reqparse.RequestParser() # 대부분 id, 닉네임 검색
get_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 검색할 값이 있는 열')
get_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 검색할 값')

post_parser = reqparse.RequestParser()
post_parser.add_argument('id', type=str, required=True, help='가입할 유저의 id')
post_parser.add_argument('pw', type=str, required=True, help='가입할 유저의 pw')
post_parser.add_argument('nickname', type=str, required=True, help='가입할 유저의 닉네임')
post_parser.add_argument('a_id', type=int, required=True, help='가입할 유저의 아바타 번호')

@RegistUser.route('')
class RegisterClass(Resource):
    def __init__(self, api=None):
        super().__init__(api)
        self.DB_URL = os.getenv("DB_URL") + "/user/regist"
        self.switch = switch
        
    @RegistUser.doc(
        parser=get_parser,
        responses={
            200: switch(200),
            201: switch(201),
            500: switch(500),
        })
    def get(self):
        """보낸 params와 일치하는 정보를 가져옴 // 회원가입 중복 방지용 """
        args = request.args
        try:                                             
            res = requests.get(self.DB_URL, params={'col': args['col'],
                                                    'data': args['data']})
            return res.json(), 200
        except:
            return switch(500), 500
    

    @RegistUser.doc(
        parser=post_parser,
        responses={
            200: switch(200),
            201: switch(201),
            400: switch(400),
            500: switch(500),
        })
    def post(self):
        """DB에 회원가입 정보를 전달"""
        args = request.args
        try:
            res = requests.post(self.DB_URL, params={'id': args['id'],
                                                     'pw': args['pw'],
                                                     'nickname': args['nickname'],
                                                     'avartar': args['a_id']})
            return switch(res.json()), res.json()
        except:
            return switch(500), 500
