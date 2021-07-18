from flask_restful import Resource


class BaseResource(Resource):
    @staticmethod
    def response(message: str,
                 status_code: int,
                 name: str = None) -> tuple[dict, int]:
        if name is None:
            return {"message": message}, status_code
        return {"name": name, "message": message}, status_code
