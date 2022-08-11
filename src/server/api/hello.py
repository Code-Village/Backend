from flask import request
from flask_restx import Resource, Api, Namespace, fields

DATABASE = {"data": "아무튼 빅-데이터"}

Hello = Namespace(
    name="Hello",
    description="테스트를 위해 작성한 API.",
)

hello_fields = Hello.model('Hello', {  # Model 객체 생성
    'data': fields.String(description='a Todo', required=True, example="님이 적은 것")
})

@Hello.route('')
class HelloPost(Resource):
    @Hello.expect(hello_fields)
    @Hello.response(201, "Success")
    def post(self):
        """님이 value에 적은 것을 출력함."""
        data = request.json.get('data')    
        return {
            '님이 적은 것': data
        }, 201

@Hello.route('/<string:data>')
@Hello.doc(params={'data': 'key값'})
class HelloGet(Resource):
    @Hello.response(200, "Success")
    @Hello.response(500, 'Failed')
    def get(self, data):
        """데이터를 출력함."""
        res = DATABASE.get(data)
        if res:
            return {
                'data': res
            }, 200
        else:
            return{
                'data': "그런 거 없음..."
            }, 500
        