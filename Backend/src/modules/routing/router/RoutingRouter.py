from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from src.modules.routing.service.RoutingService import RoutingService
from src.modules.routing.schemas import (
    RoutingOptimizationRequestSchema,
    RoutingOptimizationResponseSchema,
    SupplierPointSchema,
    CustomerPointSchema
)
from src.core.database import db
from bson import ObjectId

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/routing", tags=["Routing & Optimization"])


@router.post("/optimize/from-company")
async def optimize_from_company(
    company_id: str,
    cost_per_km: float = Query(5.5, description="Costo por km en Bs"),
    product_id: Optional[str] = Query(None, description="Filtrar por producto especifico")
):
    try:
        logger.info(f"Optimizacion desde BD para empresa {company_id}")
        
        company = db["companies"].find_one({"_id": ObjectId(company_id)})
        if not company:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        
        locations = list(db["location_companies"].find({"company_id": ObjectId(company_id)}))
        logger.info(f"Sucursales encontradas: {len(locations)}")
        
        if not locations:
            raise HTTPException(status_code=400, detail="No hay sucursales registradas")
        
        suppliers = []
        suppliers_data_for_log = []
        
        for loc in locations:
            stocks = list(db["location_stocks"].find({"location_id": loc["_id"]}))
            
            stock_dict = {}
            for stock in stocks:
                material_id = str(stock["type_material_id"])
                quantity = float(stock.get("stock", 0))
                if quantity > 0:
                    stock_dict[material_id] = quantity
            
            if product_id and product_id not in stock_dict:
                continue
            
            if product_id:
                total_stock = stock_dict.get(product_id, 0)
            else:
                total_stock = sum(stock_dict.values())
            
            if total_stock > 0:
                suppliers.append(SupplierPointSchema(
                    id=str(loc["_id"]),
                    lat=float(loc.get("lat", -16.5)),
                    lng=float(loc.get("lng", -68.15)),
                    name=loc.get("name", "Sucursal"),
                    stock=stock_dict
                ))
                suppliers_data_for_log.append({
                    "name": loc.get("name"),
                    "total_stock": total_stock,
                    "products": list(stock_dict.keys())
                })
        
        if not suppliers:
            raise HTTPException(status_code=400, detail="No hay sucursales con stock disponible")
        
        logger.info(f"Proveedores con stock: {len(suppliers)}")
        for s in suppliers_data_for_log:
            logger.info(f"   - {s['name']}: stock={s['total_stock']}, productos={s['products']}")
        
        query = {"company_id": ObjectId(company_id)}
        if product_id:
            query["product_id"] = ObjectId(product_id)
        
        orders = list(db["orders"].find(query))
        logger.info(f"Pedidos encontrados: {len(orders)}")
        
        if not orders:
            raise HTTPException(status_code=400, detail="No hay pedidos para optimizar")
        
        demand_by_location = {}
        
        for order in orders:
            lat = order.get("delivery_lat")
            lng = order.get("delivery_lng")
            
            if not lat or not lng:
                logger.warning(f"Pedido {order['_id']} sin coordenadas, omitiendo")
                continue
            
            user_id = order.get("user_id")
            user_name = "Cliente"
            if user_id:
                try:
                    user = db["users"].find_one({"_id": ObjectId(user_id)})
                    if user:
                        user_name = user.get("name", "Cliente")
                except Exception as e:
                    logger.warning(f"Error obteniendo usuario {user_id}: {e}")
            
            location_key = f"{lat},{lng}"
            product_id_str = str(order["product_id"])
            quantity = float(order.get("quantity", 0))
            product_name = order.get("product_name", "Producto")
            
            if location_key not in demand_by_location:
                demand_by_location[location_key] = {
                    "id": str(order["_id"]),
                    "lat": lat,
                    "lng": lng,
                    "name": f"{user_name} - {product_name}",
                    "user_name": user_name,
                    "product_name": product_name,
                    "demand": {}
                }
            
            if product_id_str in demand_by_location[location_key]["demand"]:
                demand_by_location[location_key]["demand"][product_id_str] += quantity
            else:
                demand_by_location[location_key]["demand"][product_id_str] = quantity
        
        customers = []
        for location_data in demand_by_location.values():
            customers.append(CustomerPointSchema(
                id=location_data["id"],
                lat=float(location_data["lat"]),
                lng=float(location_data["lng"]),
                name=location_data["name"],
                demand=location_data["demand"],
                user_name=location_data.get("user_name"),
                product_name=location_data.get("product_name")
            ))
        
        if not customers:
            raise HTTPException(status_code=400, detail="No hay pedidos con coordenadas validas")
        
        logger.info(f"Clientes (puntos de entrega unicos): {len(customers)}")
        
        total_supply = 0
        for s in suppliers:
            if product_id:
                supply_qty = s.stock.get(product_id, 0)
            else:
                supply_qty = sum(s.stock.values())
            total_supply += supply_qty
            logger.info(f"   Proveedor {s.name}: {supply_qty} unidades")
        
        total_demand = 0
        for c in customers:
            if product_id:
                demand_qty = c.demand.get(product_id, 0)
            else:
                demand_qty = sum(c.demand.values())
            total_demand += demand_qty
            logger.info(f"   Cliente {c.name}: {demand_qty} unidades")
        
        logger.info(f"TOTAL: Supply={total_supply}, Demand={total_demand}")
        
        if total_supply == 0:
            raise HTTPException(status_code=400, detail="No hay stock disponible")
        
        if total_demand == 0:
            raise HTTPException(status_code=400, detail="No hay demanda registrada")
        
        request = RoutingOptimizationRequestSchema(
            company_id=company_id,
            suppliers=suppliers,
            customers=customers,
            cost_per_km=cost_per_km,
            product_id=product_id
        )
        
        result = await RoutingService.optimize_routes(request)
        
        if result.success:
            logger.info("Optimizacion desde BD exitosa")
            return {
                "success": True,
                "data": result.dict()
            }
        else:
            raise HTTPException(status_code=400, detail=result.error)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matrix-analysis/{company_id}")
async def get_matrix_analysis(
    company_id: str,
    cost_per_km: float = Query(5.5, description="Costo por km")
):
    try:
        logger.info(f"Analisis de matriz para empresa {company_id}")
        
        company = db["companies"].find_one({"_id": ObjectId(company_id)})
        if not company:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")
        
        locations = list(db["location_companies"].find({"company_id": ObjectId(company_id)}))
        orders = list(db["orders"].find({"company_id": ObjectId(company_id)}))
        
        if not locations or not orders:
            raise HTTPException(status_code=400, detail="Datos insuficientes")
        
        suppliers = []
        for loc in locations:
            stocks = list(db["location_stocks"].find({"location_id": loc["_id"]}))
            stock_dict = {}
            for stock in stocks:
                material_id = str(stock["type_material_id"])
                quantity = float(stock.get("stock", 0))
                if quantity > 0:
                    stock_dict[material_id] = quantity
            
            suppliers.append(SupplierPointSchema(
                id=str(loc["_id"]),
                lat=float(loc.get("lat", -16.5)),
                lng=float(loc.get("lng", -68.15)),
                name=loc.get("name", "Sucursal"),
                stock=stock_dict
            ))
        
        demand_by_location = {}
        for order in orders:
            lat = order.get("delivery_lat")
            lng = order.get("delivery_lng")
            
            if not lat or not lng:
                continue
            
            user_id = order.get("user_id")
            user_name = "Cliente"
            if user_id:
                try:
                    user = db["users"].find_one({"_id": ObjectId(user_id)})
                    if user:
                        user_name = user.get("name", "Cliente")
                except Exception:
                    pass
            
            location_key = f"{lat},{lng}"
            product_id_str = str(order["product_id"])
            quantity = float(order.get("quantity", 0))
            product_name = order.get("product_name", "Producto")
            
            if location_key not in demand_by_location:
                demand_by_location[location_key] = {
                    "id": str(order["_id"]),
                    "lat": lat,
                    "lng": lng,
                    "name": f"{user_name} - {product_name}",
                    "demand": {}
                }
            
            if product_id_str in demand_by_location[location_key]["demand"]:
                demand_by_location[location_key]["demand"][product_id_str] += quantity
            else:
                demand_by_location[location_key]["demand"][product_id_str] = quantity
        
        customers = []
        for location_data in demand_by_location.values():
            customers.append(CustomerPointSchema(
                id=location_data["id"],
                lat=float(location_data["lat"]),
                lng=float(location_data["lng"]),
                name=location_data["name"],
                demand=location_data["demand"]
            ))
        
        if not suppliers or not customers:
            raise HTTPException(status_code=400, detail="Datos insuficientes")
        
        request = RoutingOptimizationRequestSchema(
            company_id=company_id,
            suppliers=suppliers,
            customers=customers,
            cost_per_km=cost_per_km
        )
        
        result = await RoutingService.optimize_routes(request)
        
        return {
            "success": result.success,
            "cost_matrix": result.cost_matrix,
            "suppliers": [{"name": s.name, "stock": s.stock} for s in suppliers],
            "customers": [{"name": c.name, "demand": c.demand} for c in customers],
            "allocations": [a.dict() for a in result.routes] if result.routes else [],
            "total_cost": result.total_cost,
            "total_distance_km": result.total_distance_km,
            "total_allocations": result.total_allocations,
            "is_optimal": result.modi_solution.get("is_optimal", False),
            "vogel_allocations": len(result.vogel_solution.get("allocations", [])),
            "modi_allocations": len(result.modi_solution.get("allocations", [])),
            "error": result.error
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))