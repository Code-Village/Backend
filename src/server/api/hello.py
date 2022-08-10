from flask import request
from flask_restx import Resource, Api, Namespace, fields

Hello = Namespace(
    name="Hello",
    description="테스트를 위해 작성한 API.",
)

hello_fields = Hello.model('Hello', {  # Model 객체 생성
    'data': fields.String(description='a Todo', required=True, example="님이 적은 것")
})

@Hello.route('')
class TodoPost(Resource):
    @Hello.expect(hello_fields)
    @Hello.response(201, "Success")
    def post(self):
        """님이 value에 적은 것을 출력함."""
        data = request.json.get('data')    
        return {
            '님이 적은 것': data
        }, 201
        