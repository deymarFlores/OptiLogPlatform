from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Tuple


class SupplierPointSchema(BaseModel):
    id: str
    lat: float = Field(..., description="Latitud")
    lng: float = Field(..., description="Longitud")
    name: str = Field(..., description="Nombre de la sucursal")
    stock: Dict[str, float] = Field(default_factory=dict, description="Stock por producto")


class CustomerPointSchema(BaseModel):
    id: str
    lat: float
    lng: float
    name: str = Field(..., description="Nombre del cliente/orden")
    demand: Dict[str, float] = Field(default_factory=dict, description="Demanda por producto")
    user_name: Optional[str] = Field(default=None, description="Nombre del cliente/usuario")
    product_name: Optional[str] = Field(default=None, description="Nombre del producto solicitado")


class RoutingOptimizationRequestSchema(BaseModel):
    company_id: str
    suppliers: List[SupplierPointSchema] = Field(..., description="Sucursales/almacenes")
    customers: List[CustomerPointSchema] = Field(..., description="Clientes/destinos")
    cost_per_km: float = Field(default=5.5, description="Costo de gasolina por km en Bs")
    product_id: Optional[str] = Field(default=None, description="Filtrar por producto especifico")


class AllocationSchema(BaseModel):
    supplier_id: str
    supplier_name: str
    customer_id: str
    customer_name: str
    quantity: float
    unit_cost: float = Field(..., description="Costo por unidad")
    total_cost: float = Field(..., description="Costo total")


class RouteDetailSchema(BaseModel):
    supplier_id: str
    supplier_name: str
    customer_id: str
    customer_name: str
    quantity: float = Field(..., description="Cantidad asignada")
    distance_m: float = Field(..., description="Distancia en metros")
    distance_km: float = Field(..., description="Distancia en km")
    unit_cost: float = Field(..., description="Costo por unidad")
    cost: float = Field(..., description="Costo total de transporte")
    geometry: Optional[str] = Field(default=None, description="Polyline codificado")
    coordinates: List[Tuple[float, float]] = Field(default_factory=list, description="Coordenadas de la ruta")


class RoutingOptimizationResponseSchema(BaseModel):
    success: bool
    company_id: str
    cost_matrix: List[List[float]] = Field(..., description="Matriz de costos")
    suppliers_data: List[Dict[str, Any]]
    customers_data: List[Dict[str, Any]]
    vogel_solution: Dict[str, Any] = Field(..., description="Solucion inicial Vogel/VAM")
    modi_solution: Dict[str, Any] = Field(..., description="Solucion optimizada MODI")
    routes: List[RouteDetailSchema] = Field(default_factory=list)
    total_cost: float
    total_distance_km: float
    total_allocations: int
    error: Optional[str] = None


class RoutingAnalysisSchema(BaseModel):
    success: bool
    company_id: str
    cost_matrix: List[List[float]]
    allocations: List[AllocationSchema]
    total_cost: float
    is_optimal: bool
    analysis_method: str = Field(default="Vogel+MODI")
    error: Optional[str] = None