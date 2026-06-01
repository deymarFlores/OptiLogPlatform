from src.core.database import db
from src.modules.orders.schemas.OrderSchema import OrderSchema
from fastapi import HTTPException
from bson.objectid import ObjectId
from datetime import datetime


class OrderService:
    def __init__(self):
        self.collection = db["orders"]
        self._create_indexes()

    def _create_indexes(self):
        try:
            self.collection.create_index([("user_id", 1)])
            self.collection.create_index([("company_id", 1)])
            self.collection.create_index([("created_at", -1)])
        except Exception:
            pass

    def create(self, data: OrderSchema):
        try:
            order = {
                "user_id": ObjectId(data.user_id),
                "company_id": ObjectId(data.company_id),
                "product_id": ObjectId(data.product_id),
                "product_name": data.product_name,
                "quantity": data.quantity,
                "price": data.price,
                "total_amount": data.price * data.quantity,
                "delivery_lat": data.delivery_lat,
                "delivery_lng": data.delivery_lng,
                "company_name": data.company_name or "",
                "created_at": datetime.utcnow().isoformat(),
                "status": "pending"  # pending, confirmed, delivered, cancelled
            }
            result = self.collection.insert_one(order)
            return {
                "success": True,
                "data": {
                    "id": str(result.inserted_id),
                    "user_id": data.user_id,
                    "company_id": data.company_id,
                    "product_id": data.product_id,
                    "product_name": data.product_name,
                    "quantity": data.quantity,
                    "price": data.price,
                    "total_amount": data.price * data.quantity,
                    "delivery_lat": data.delivery_lat,
                    "delivery_lng": data.delivery_lng,
                    "company_name": data.company_name or "",
                    "created_at": order["created_at"]
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear orden: {str(e)}")

    def get_by_user(self, user_id: str):
        try:
            orders = self.collection.find(
                {"user_id": ObjectId(user_id)},
                sort=[("created_at", -1)]
            ).to_list(None)
            
            return {
                "success": True,
                "data": [
                    {
                        "id": str(order["_id"]),
                        "user_id": str(order["user_id"]),
                        "company_id": str(order["company_id"]),
                        "product_id": str(order["product_id"]),
                        "product_name": order.get("product_name", ""),
                        "quantity": order.get("quantity", 0),
                        "price": order.get("price", 0),
                        "total_amount": order.get("total_amount", 0),
                        "delivery_lat": order.get("delivery_lat", 0),
                        "delivery_lng": order.get("delivery_lng", 0),
                        "company_name": order.get("company_name", ""),
                        "created_at": order.get("created_at", ""),
                        "status": order.get("status", "pending")
                    }
                    for order in orders
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener órdenes: {str(e)}")

    def get_by_company(self, company_id: str):
        try:
            orders = self.collection.find(
                {"company_id": ObjectId(company_id)},
                sort=[("created_at", -1)]
            ).to_list(None)
            
            return {
                "success": True,
                "data": [
                    {
                        "id": str(order["_id"]),
                        "user_id": str(order["user_id"]),
                        "company_id": str(order["company_id"]),
                        "product_id": str(order["product_id"]),
                        "product_name": order.get("product_name", ""),
                        "quantity": order.get("quantity", 0),
                        "price": order.get("price", 0),
                        "total_amount": order.get("total_amount", 0),
                        "delivery_lat": order.get("delivery_lat", 0),
                        "delivery_lng": order.get("delivery_lng", 0),
                        "company_name": order.get("company_name", ""),
                        "created_at": order.get("created_at", ""),
                        "status": order.get("status", "pending")
                    }
                    for order in orders
                ]
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener órdenes: {str(e)}")

    def get_by_id(self, order_id: str):
        try:
            order = self.collection.find_one({"_id": ObjectId(order_id)})
            
            if not order:
                raise HTTPException(status_code=404, detail="Orden no encontrada")
            
            return {
                "success": True,
                "data": {
                    "id": str(order["_id"]),
                    "user_id": str(order["user_id"]),
                    "company_id": str(order["company_id"]),
                    "product_id": str(order["product_id"]),
                    "product_name": order.get("product_name", ""),
                    "quantity": order.get("quantity", 0),
                    "price": order.get("price", 0),
                    "total_amount": order.get("total_amount", 0),
                    "delivery_lat": order.get("delivery_lat", 0),
                    "delivery_lng": order.get("delivery_lng", 0),
                    "company_name": order.get("company_name", ""),
                    "created_at": order.get("created_at", ""),
                    "status": order.get("status", "pending")
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener orden: {str(e)}")
