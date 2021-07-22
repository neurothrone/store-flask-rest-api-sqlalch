from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from src.models.item import ItemModel


class ItemListResource(Resource):
    @jwt_required()
    def get(self) -> tuple[dict, int]:
        if items := ItemModel.all_to_json():
            return {"items": items}, 200
        return ItemResource.response(
            message="There are no items.",
            status_code=404)


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    @jwt_required()
    def get(self, name: str) -> tuple[dict, int]:
        if not name:
            return ItemResource.response(
                message="Failed to create item, name is missing.",
                status_code=400)

        try:
            if item := ItemModel.find_by_name(name):
                return item.to_json(), 200
        except:
            return ItemResource.response(
                message="An error occured requesting the item.",
                status_code=500)
        return ItemResource.response(
            message=f"There is no item by the name '{name}'.",
            status_code=404)

    @jwt_required()
    def post(self, name: str) -> tuple[dict, int]:
        if not name:
            return ItemResource.response(
                message="Failed to create item, name is missing.",
                status_code=400)

        if ItemModel.find_by_name(name):
            return ItemResource.response(
                message=f"An item with the name '{name}' already exists.",
                status_code=400)

        args = ItemResource.parser.parse_args()
        if not args["price"]:
            return ItemResource.response(
                message="Missing value on price field.",
                status_code=400)
        try:
            item = ItemModel(name, **args)
            item.save_to_db()

            return ItemResource.response(
                message="Item created.",
                status_code=201,
                name=item.name)
        except:
            return ItemResource.response(
                message="An error occured creating the item.",
                status_code=500)

    @jwt_required()
    def put(self, name: str) -> tuple[dict, int]:
        if not name:
            return ItemResource.response(
                message="Failed to update item, name is missing.",
                status_code=400)

        args = ItemResource.parser.parse_args()

        if item := ItemModel.find_by_name(name):
            try:
                item.update(args["price"])

                return ItemResource.response(
                    message="Item updated.",
                    status_code=200,
                    name=item.name)
            except:
                return ItemResource.response(
                    message="An error occured updating the item.",
                    status_code=500)

        try:
            item = ItemModel(name, **args)
            item.save_to_db()

            return ItemResource.response(
                message="Item created.",
                status_code=201,
                name=item.name)
        except:
            return ItemResource.response(
                message="An error occured creating the item.",
                status_code=500)

    @jwt_required()
    def delete(self, name: str) -> tuple[dict, int]:
        if not name:
            return ItemResource.response(
                message="Failed to delete item, name is missing.",
                status_code=400)

        if item := ItemModel.find_by_name(name):
            try:
                item.delete_from_db()

                return ItemResource.response(
                    message="Item deleted.",
                    status_code=200,
                    name=item.name)
            except:
                return ItemResource.response(
                    message="An error occurred deleting the item.",
                    status_code=500)
        return ItemResource.response(
            message=f"There is no item by the name '{name}'.",
            status_code=404)

    @staticmethod
    def response(message: str,
                 status_code: int,
                 name: str = None) -> tuple[dict, int]:
        if name is None:
            return {"message": message}, status_code
        return {"name": name, "message": message}, status_code
