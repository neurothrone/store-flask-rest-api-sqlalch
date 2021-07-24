from flask_jwt_extended import jwt_required

from src.models.store import StoreModel
from src.resources.base import BaseResource


class StoreListResource(BaseResource):
    @jwt_required()
    def get(self) -> tuple[dict, int]:
        if stores := StoreModel.all_to_json():
            return {"stores": stores}, 200
        return self.response(
            message="There are no stores.",
            status_code=404)


class StoreResource(BaseResource):
    @jwt_required()
    def get(self, name: str) -> tuple[dict, int]:
        if not name:
            return self.response(
                message="Failed to create store, name is missing.",
                status_code=400)

        try:
            if store := StoreModel.find_by_name(name):
                return store.to_json(), 200
        except:
            return self.response(
                message="An error occured requesting the store.",
                status_code=500)
        return self.response(
            message=f"There is no store by the name '{name}'.",
            status_code=404)

    @jwt_required()
    def post(self, name: str) -> tuple[dict, int]:
        if not name:
            return self.response(
                message="Failed to create store, name is missing.",
                status_code=400)

        if StoreModel.find_by_name(name):
            return self.response(
                message=f"A store with the name '{name}' already exists.",
                status_code=400)

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return self.response(
                message="An error occured creating the store.",
                status_code=500)
        return self.response(
            message="Store created.",
            status_code=201,
            name=store.name)

    @jwt_required()
    def delete(self, name) -> tuple[dict, int]:
        if not name:
            return self.response(
                message="Failed to delete store, name is missing.",
                status_code=400)

        if store := StoreModel.find_by_name(name):
            try:
                store.delete_from_db()

                return self.response(
                    message="Item deleted.",
                    status_code=200,
                    name=store.name)
            except:
                return self.response(
                    message="An error occurred deleting the store.",
                    status_code=500)
        return self.response(
            message=f"There is no store by the name '{name}'.",
            status_code=404)
