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

Team = Namespace(
    name="Team",
    description="Team Read,Update,Delete API",
)

get_parser = reqparse.RequestParser()
get_parser.add_argument('teamname', type=str, required=True, help='팀 이름')

post_parser = reqparse.RequestParser()
post_parser.add_argument('teamname', type=str, required=True, help='팀 이름')
post_parser.add_argument('nickname', type=str, required=True, help='팀원 닉네임')

put_parser = reqparse.RequestParser()
put_parser.add_argument('col', type=str, required=True, help='데이터베이스에서 변경할 값이 있는 열')
put_parser.add_argument('old_data', type=str, required=True, help='데이터베이스에서 변경하고자 하는 팀의 이름')
put_parser.add_argument('new_data', type=str, required=True, help='데이터베이스에서 변경할 값')

del_parser = reqparse.RequestParser()
del_parser.add_argument('teamname', type=str, required=True, help='데이터베이스에서 삭제할 팀 이름')

@Team.route('')
class TeamClass(Resource):
    def __init__(self, api=None):
        super().__init__(api)
        self.DB_URL = os.getenv("DB_URL") + "/team"
        self.switch = switch
        
    @Team.doc(
        parser=get_parser,
        responses={
            200: switch(200),
            400: switch(400),
            401: switch(401),
            500: switch(500),
        })
    def get(self):
        """teamname을 통해 team 정보를 가져옴"""
        args = request.args
        try:                                             
            res = requests.get(self.DB_URL, params={'teamname': args['teamname']})
            return res.json(), 200
        except:
            return switch(500), 500
        
    @Team.doc(
        parser=post_parser,
        responses={
            200: switch(200),
            400: switch(400),
            401: switch(401),
            500: switch(500),
        })
    def post(self):
        """user를 team에 추가"""
        args = request.args
        try:                                             
            res = requests.get(self.DB_URL, params={'teamname': args['teamname'],
                                                    'uname': args['nickname']})
            return switch(res.json()), res.json()
        except:
            return switch(500), 500

    @Team.doc(
        parser=put_parser,
        responses={
            200: switch(200),
            400: switch(400),
            500: switch(500),
        })
    def put(self):
        """team 정보를 수정 (단, id 제외)"""
        args = request.args
        try:
            res = requests.put(self.DB_URL, params={'col': args['col'],
                                                    'id': args['old_data'],
                                                    'data': args['new_data']})
            return switch(res.json()), 200
        except:
            return switch(500), 500
        
    @Team.doc(
        parser=del_parser,
        responses={
            200: switch(200),
            400: switch(400),
            500: switch(500),
        })
    def delete(self):
        """해당 teamname을 가진 팀 삭제"""
        args = request.args
        try:      
            res = requests.put(self.DB_URL, params={'teamname': args['teamname']})    
            return switch(res.json()), 200
        except:
            return switch(500), 500
    