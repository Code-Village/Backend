from flask import request
from flask_restx import Resource, Namespace, fields


DATABASE = {"value": "아무튼 빅-데이터"}

Hello = Namespace(
    name="Hello",
    description="테스트를 위해 작성한 API.",
)

hello_fields = Hello.model('Hello', {  # Model 객체 생성

    'data': fields.String(description='value', required=True)

})

@Hello.route('')
class HelloPost(Resource):
    @Hello.expect(hello_fields)
    @Hello.response(201, "Success")
    def post(self):
        """'data'의 value값에 적은 것을 출력함."""
        data = request.json.get('data')    
        return {
            '님이 적은 것': data
        }, 201

@Hello.route('/<string:value>')
@Hello.doc(params={'value': '검색하고 싶은 값'})
class HelloGet(Resource):
    @Hello.response(200, "Success")
    @Hello.response(500, 'Failed')
    def get(self, value):
        """value의 검색값을 출력함."""
        res = DATABASE.get(value)
        if res:
            return {
                'data': res
            }, 200
        else:
            return{
                'data': "그런 거 없음..."
            }, 500
        