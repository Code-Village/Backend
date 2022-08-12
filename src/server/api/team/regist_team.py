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
        401: "FAILED_TO_APPEND_TEAM",
        402: "FAILED_TO_APPEND_TEAMLIST",
        500: "SERVER_CONNECTION_ERROR",
    }
    return res_switch.get(arg, "UNKNOWN") 

RegistTeam = Namespace(
    name="RegistTeam",
    description="팀 생성 API",
)

get_parser = reqparse.RequestParser() # 대부분 id, 닉네임 검색
get_parser.add_argument('data', type=str, required=True, help='데이터베이스에서 검색할 값')

post_parser = reqparse.RequestParser()
post_parser.add_argument('teamname', type=str, required=True, help='생성할 팀 이름')
post_parser.add_argument('admin', type=str, required=True, help='생성할 팀의 팀장 nickname')

@RegistTeam.route('')
class RegisterTeamClass(Resource):
    def __init__(self, api=None):
        super().__init__(api)
        self.DB_URL = os.getenv("DB_URL") + "/team/regist"
        self.switch = switch
    
    @RegistTeam.doc(
        parser=get_parser,
        responses={
            200: switch(200),
            201: switch(201),
            401: switch(401),
            402: switch(402),
            500: switch(500),
        })
    def get(self):
        """보낸 params와 일치하는 정보를 가져옴 // 팀 이름 중복 방지용 """
        args = request.args
        try:                                             
            res = requests.get(self.DB_URL, params={'data': args['data']})
            return res.json(), 200
        except:
            return switch(500), 500
    

    @RegistTeam.doc(
        parser=post_parser,
        responses={
            200: switch(200),
            201: switch(201),
            400: switch(400),
            500: switch(500),
        })
    def post(self):
        """teamname과 팀장 nickname을 DB에 전달"""
        args = request.args
        try:
            res = requests.post(self.DB_URL, params={'teamname': args['teamname'],
                                                     'admin': args['admin'],})
            return switch(res.json()), res.json()
        except:
            return switch(500), 500
