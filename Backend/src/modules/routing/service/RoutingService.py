import logging
import math
from typing import List, Dict, Any, Optional, Tuple
from src.modules.routing.service.OSRMService import OSRMService
from src.modules.routing.service.VogelOptimizer import VogelOptimizer
from src.modules.routing.service.ModiOptimizer import ModiOptimizer
from src.modules.routing.schemas.RoutingSchema import (
    RoutingOptimizationRequestSchema,
    RoutingOptimizationResponseSchema,
    RouteDetailSchema,
    AllocationSchema
)

logger = logging.getLogger(__name__)


class RoutingService:
    @staticmethod
    async def optimize_routes(
        request: RoutingOptimizationRequestSchema
    ) -> RoutingOptimizationResponseSchema:
        try:
            logger.info(f"Iniciando optimizacion para empresa {request.company_id}")
            
            suppliers = request.suppliers
            customers = request.customers
            cost_per_km = request.cost_per_km
            product_id = request.product_id
            
            logger.info(f"{len(suppliers)} sucursales, {len(customers)} clientes")
            logger.info(f"Costo por km: {cost_per_km} Bs")
            
            if not suppliers:
                error_msg = "No hay sucursales registradas"
                logger.error(error_msg)
                return RoutingOptimizationResponseSchema(
                    success=False,
                    company_id=request.company_id,
                    cost_matrix=[],
                    suppliers_data=[],
                    customers_data=[],
                    vogel_solution={},
                    modi_solution={},
                    total_cost=0,
                    total_distance_km=0,
                    total_allocations=0,
                    error=error_msg
                )
            
            if not customers:
                error_msg = "No hay pedidos registrados"
                logger.error(error_msg)
                return RoutingOptimizationResponseSchema(
                    success=False,
                    company_id=request.company_id,
                    cost_matrix=[],
                    suppliers_data=[],
                    customers_data=[],
                    vogel_solution={},
                    modi_solution={},
                    total_cost=0,
                    total_distance_km=0,
                    total_allocations=0,
                    error=error_msg
                )
            
            supply = []
            supply_details = []
            
            for supplier in suppliers:
                if product_id:
                    qty = supplier.stock.get(product_id, 0)
                else:
                    qty = sum(supplier.stock.values())
                
                supply.append(qty)
                supply_details.append({
                    "id": supplier.id,
                    "name": supplier.name,
                    "quantity": qty,
                    "stock": supplier.stock
                })
            
            demand = []
            demand_details = []
            
            for customer in customers:
                if product_id:
                    qty = customer.demand.get(product_id, 0)
                else:
                    qty = sum(customer.demand.values())
                
                demand.append(qty)
                demand_details.append({
                    "id": customer.id,
                    "name": customer.name,
                    "quantity": qty,
                    "demand": customer.demand
                })
            
            total_supply = sum(supply)
            total_demand = sum(demand)
            
            logger.info("SUPPLY (stock disponible):")
            for s in supply_details:
                logger.info(f"   - {s['name']}: {s['quantity']} unidades")
            
            logger.info("DEMAND (pedidos):")
            for d in demand_details:
                logger.info(f"   - {d['name']}: {d['quantity']} unidades")
            
            logger.info(f"TOTAL: Supply={total_supply}, Demand={total_demand}")
            
            if total_supply == 0:
                error_msg = "No hay stock disponible en las sucursales"
                logger.error(error_msg)
                return RoutingOptimizationResponseSchema(
                    success=False,
                    company_id=request.company_id,
                    cost_matrix=[],
                    suppliers_data=[],
                    customers_data=[],
                    vogel_solution={},
                    modi_solution={},
                    total_cost=0,
                    total_distance_km=0,
                    total_allocations=0,
                    error=error_msg
                )
            
            if total_demand == 0:
                error_msg = "No hay demanda registrada en los pedidos"
                logger.error(error_msg)
                return RoutingOptimizationResponseSchema(
                    success=False,
                    company_id=request.company_id,
                    cost_matrix=[],
                    suppliers_data=[],
                    customers_data=[],
                    vogel_solution={},
                    modi_solution={},
                    total_cost=0,
                    total_distance_km=0,
                    total_allocations=0,
                    error=error_msg
                )
            
            valid_supplier_indices = [i for i, s in enumerate(supply) if s > 0]
            valid_customer_indices = [j for j, d in enumerate(demand) if d > 0]
            
            original_supplier_count = len(suppliers)
            original_customer_count = len(customers)
            
            if len(valid_supplier_indices) != original_supplier_count or len(valid_customer_indices) != original_customer_count:
                logger.info("Filtrando elementos sin stock/demanda:")
                logger.info(f"   Proveedores: {len(valid_supplier_indices)}/{original_supplier_count}")
                logger.info(f"   Clientes: {len(valid_customer_indices)}/{original_customer_count}")
                
                supply = [supply[i] for i in valid_supplier_indices]
                demand = [demand[j] for j in valid_customer_indices]
                suppliers_filtered = [suppliers[i] for i in valid_supplier_indices]
                customers_filtered = [customers[j] for j in valid_customer_indices]
            else:
                suppliers_filtered = suppliers
                customers_filtered = customers
            
            if not suppliers_filtered:
                error_msg = "No hay proveedores con stock disponible despues del filtrado"
                logger.error(error_msg)
                return RoutingOptimizationResponseSchema(
                    success=False,
                    company_id=request.company_id,
                    cost_matrix=[],
                    suppliers_data=[],
                    customers_data=[],
                    vogel_solution={},
                    modi_solution={},
                    total_cost=0,
                    total_distance_km=0,
                    total_allocations=0,
                    error=error_msg
                )
            
            if not customers_filtered:
                error_msg = "No hay clientes con demanda despues del filtrado"
                logger.error(error_msg)
                return RoutingOptimizationResponseSchema(
                    success=False,
                    company_id=request.company_id,
                    cost_matrix=[],
                    suppliers_data=[],
                    customers_data=[],
                    vogel_solution={},
                    modi_solution={},
                    total_cost=0,
                    total_distance_km=0,
                    total_allocations=0,
                    error=error_msg
                )
            
            logger.info("Consultando OSRM para distancias reales...")
            
            all_points = []
            supplier_indices = []
            customer_indices = []
            
            for i, supplier in enumerate(suppliers_filtered):
                all_points.append((supplier.lat, supplier.lng))
                supplier_indices.append(i)
            
            for i, customer in enumerate(customers_filtered):
                all_points.append((customer.lat, customer.lng))
                customer_indices.append(len(suppliers_filtered) + i)
            
            logger.info(f"Puntos a consultar: {len(all_points)} (proveedores: {len(suppliers_filtered)}, clientes: {len(customers_filtered)})")
            
            try:
                distance_data = await OSRMService.get_distance_matrix(
                    all_points,
                    sources=supplier_indices,
                    destinations=customer_indices
                )
                
                distances_matrix = distance_data["distances"]
                logger.info(f"Matriz de distancias obtenida: {len(distances_matrix)}x{len(distances_matrix[0]) if distances_matrix else 0}")
                
                if len(distances_matrix) != len(suppliers_filtered) or (len(distances_matrix) > 0 and len(distances_matrix[0]) != len(customers_filtered)):
                    logger.error(f"Matriz de distancias tiene tamano incorrecto: {len(distances_matrix)}x{len(distances_matrix[0]) if distances_matrix else 0}")
                    raise ValueError("La matriz de distancias no tiene el tamano esperado")
                
            except Exception as e:
                logger.error(f"Error obteniendo matriz de distancias: {str(e)}")
                logger.warning("Usando distancias euclidianas como fallback")
                distances_matrix = RoutingService._calculate_euclidean_distances(
                    suppliers_filtered, customers_filtered
                )
            
            cost_matrix = RoutingService._convert_distances_to_costs(
                distances_matrix,
                cost_per_km
            )
            
            logger.info("Matriz de costos calculada")
            
            total_supply_filtered = sum(supply)
            total_demand_filtered = sum(demand)
            
            logger.info(f"Despues de filtrado - Supply: {total_supply_filtered}, Demand: {total_demand_filtered}")
            
            original_supply = supply.copy()
            original_demand = demand.copy()
            original_cost_matrix = [row[:] for row in cost_matrix]
            
            if abs(total_supply_filtered - total_demand_filtered) > 0.01:
                logger.warning(f"Problema desbalanceado: supply={total_supply_filtered}, demand={total_demand_filtered}")
                
                if total_supply_filtered > total_demand_filtered:
                    demand.append(total_supply_filtered - total_demand_filtered)
                    for i in range(len(supply)):
                        cost_matrix[i].append(0)
                    logger.info(f"Cliente ficticio agregado con demanda {total_supply_filtered - total_demand_filtered}")
                else:
                    supply.append(total_demand_filtered - total_supply_filtered)
                    cost_matrix.append([0] * len(demand))
                    logger.info(f"Proveedor ficticio agregado con stock {total_demand_filtered - total_supply_filtered}")
            
            logger.info("Aplicando algoritmo Vogel...")
            try:
                vogel = VogelOptimizer(cost_matrix, supply, demand)
                vogel_result = vogel.solve()
                logger.info(f"Vogel completado: {len(vogel_result['allocations'])} asignaciones, costo: {vogel_result['total_cost']:.2f}")
            except Exception as e:
                logger.error(f"Error en Vogel: {str(e)}")
                vogel_result = {
                    "allocations": [],
                    "total_cost": 0,
                    "is_optimal": False,
                    "iterations": 0,
                    "method": "Vogel (VAM)",
                    "error": str(e)
                }
            
            logger.info("Aplicando metodo MODI...")
            try:
                if vogel_result["allocations"]:
                    modi = ModiOptimizer(cost_matrix, vogel_result["allocations"], supply, demand)
                    modi_result = modi.optimize()
                    logger.info(f"MODI completado: {len(modi_result['allocations'])} asignaciones, costo: {modi_result['total_cost']:.2f}")
                else:
                    modi_result = {
                        "allocations": [],
                        "total_cost": 0,
                        "is_optimal": False,
                        "iterations": 0,
                        "improvements": 0,
                        "method": "MODI",
                        "error": "No hay asignaciones para optimizar"
                    }
            except Exception as e:
                logger.error(f"Error en MODI: {str(e)}")
                modi_result = {
                    "allocations": vogel_result["allocations"],
                    "total_cost": vogel_result["total_cost"],
                    "is_optimal": False,
                    "iterations": 0,
                    "improvements": 0,
                    "method": "MODI",
                    "error": str(e)
                }
            
            if modi_result["total_cost"] < vogel_result["total_cost"] and modi_result["allocations"]:
                final_allocations = modi_result["allocations"]
                final_cost = modi_result["total_cost"]
                logger.info(f"MODI mejoro la solucion: {vogel_result['total_cost']:.2f} -> {final_cost:.2f} Bs")
            else:
                final_allocations = vogel_result["allocations"]
                final_cost = vogel_result["total_cost"]
                logger.info(f"Usando solucion Vogel: {final_cost:.2f} Bs")
            
            logger.info("Generando detalles de rutas...")
            routes = []
            
            for alloc in final_allocations:
                supplier_idx = alloc["supplier"]
                customer_idx = alloc["customer"]
                quantity = alloc["quantity"]
                
                if supplier_idx >= len(suppliers_filtered) or customer_idx >= len(customers_filtered):
                    logger.warning(f"Indices fuera de rango: supplier={supplier_idx}, customer={customer_idx}")
                    continue
                
                supplier = suppliers_filtered[supplier_idx]
                customer = customers_filtered[customer_idx]
                
                if supplier_idx < len(distances_matrix) and customer_idx < len(distances_matrix[0]):
                    distance_m = distances_matrix[supplier_idx][customer_idx]
                else:
                    distance_m = 0
                
                distance_km = distance_m / 1000
                unit_cost = cost_per_km * distance_km if distance_km > 0 else 0
                total_cost = quantity * unit_cost
                
                geometry = ""
                
                try:
                    route_data = await OSRMService.get_route(
                        (supplier.lat, supplier.lng),
                        (customer.lat, customer.lng)
                    )
                    
                    if route_data and route_data.get("routes"):
                        route = route_data["routes"][0]
                        geometry = route.get("geometry", "")
                        
                except Exception as e:
                    logger.warning(f"Error obteniendo ruta entre {supplier.name} y {customer.name}: {e}")
                
                route_detail = RouteDetailSchema(
                    supplier_id=supplier.id,
                    supplier_name=supplier.name,
                    customer_id=customer.id,
                    customer_name=customer.name,
                    quantity=quantity,
                    distance_m=distance_m,
                    distance_km=distance_km,
                    unit_cost=unit_cost,
                    cost=total_cost,
                    geometry=geometry,
                    coordinates=[]
                )
                
                routes.append(route_detail)
            
            suppliers_data = []
            for i, s in enumerate(suppliers_filtered):
                suppliers_data.append({
                    "id": s.id,
                    "name": s.name,
                    "lat": s.lat,
                    "lng": s.lng,
                    "stock": s.stock,
                    "total_stock": supply[i] if i < len(supply) else 0,
                    "original_index": i
                })
            
            customers_data = []
            for i, c in enumerate(customers_filtered):
                customers_data.append({
                    "id": c.id,
                    "name": c.name,
                    "user_name": getattr(c, 'user_name', None),
                    "product_name": getattr(c, 'product_name', None),
                    "lat": c.lat,
                    "lng": c.lng,
                    "demand": c.demand,
                    "total_demand": demand[i] if i < len(demand) else 0,
                    "original_index": i
                })
            
            total_distance_km = sum(r.distance_km for r in routes)
            
            response = RoutingOptimizationResponseSchema(
                success=True,
                company_id=request.company_id,
                cost_matrix=cost_matrix,
                suppliers_data=suppliers_data,
                customers_data=customers_data,
                vogel_solution=vogel_result,
                modi_solution=modi_result,
                routes=routes,
                total_cost=final_cost,
                total_distance_km=total_distance_km,
                total_allocations=len(final_allocations)
            )
            
            logger.info(f"Optimizacion completada exitosamente")
            logger.info(f"Costo total: {final_cost:.2f} Bs")
            logger.info(f"Distancia total: {total_distance_km:.2f} km")
            logger.info(f"Asignaciones: {len(final_allocations)}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error en optimizacion: {str(e)}", exc_info=True)
            return RoutingOptimizationResponseSchema(
                success=False,
                company_id=request.company_id,
                cost_matrix=[],
                suppliers_data=[],
                customers_data=[],
                vogel_solution={},
                modi_solution={},
                total_cost=0,
                total_distance_km=0,
                total_allocations=0,
                error=str(e)
            )
    
    @staticmethod
    def _calculate_euclidean_distances(suppliers, customers):
        distances = []
        for supplier in suppliers:
            row = []
            for customer in customers:
                lat1, lon1 = math.radians(supplier.lat), math.radians(supplier.lng)
                lat2, lon2 = math.radians(customer.lat), math.radians(customer.lng)
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                
                a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                c = 2 * math.asin(math.sqrt(a))
                
                r = 6371
                distance_km = r * c
                
                row.append(distance_km * 1000)
            distances.append(row)
        
        logger.info(f"Distancias euclidianas calculadas: {len(distances)}x{len(distances[0]) if distances else 0}")
        return distances
    
    @staticmethod
    def _convert_distances_to_costs(
        distances_matrix: List[List[float]],
        cost_per_km: float
    ) -> List[List[float]]:
        cost_matrix = []
        for row in distances_matrix:
            cost_row = [
                (distance / 1000) * cost_per_km
                for distance in row
            ]
            cost_matrix.append(cost_row)
        
        logger.info(f"Matriz de costos generada: {len(cost_matrix)}x{len(cost_matrix[0]) if cost_matrix else 0}")
        return cost_matrix