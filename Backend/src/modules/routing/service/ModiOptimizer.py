import logging
from typing import List, Dict, Tuple, Any
from copy import deepcopy

logger = logging.getLogger(__name__)


class ModiOptimizer:
    def __init__(
        self,
        cost_matrix: List[List[float]],
        allocations: List[Dict],
        supply: List[float],
        demand: List[float]
    ):

        self.cost_matrix = deepcopy(cost_matrix)
        self.allocations = deepcopy(allocations)
        self.supply = deepcopy(supply)
        self.demand = deepcopy(demand)
        
        self.num_suppliers = len(supply)
        self.num_customers = len(demand)
        
        # Crear matriz de asignaciones para referencia rápida
        self.allocation_matrix = [
            [0.0 for _ in range(self.num_customers)]
            for _ in range(self.num_suppliers)
        ]
        
        for alloc in allocations:
            i = alloc["supplier"]
            j = alloc["customer"]
            self.allocation_matrix[i][j] = alloc["quantity"]
    
    def optimize(self, max_iterations: int = 10) -> Dict[str, Any]:
        logger.info(" Iniciando optimización MODI...")
        
        current_allocations = deepcopy(self.allocations)
        current_cost = sum(a["total_cost"] for a in current_allocations)
        iteration = 0
        improvements = 0
        
        for iteration in range(max_iterations):
            # Calcular multiplicadores u, v
            u, v = self._calculate_multipliers(current_allocations)
            
            if u is None:
                logger.warning(" No se pueden calcular multiplicadores (solución degenerada)")
                break
            
            # Calcular oportunidades de mejora
            opportunity_costs = self._calculate_opportunity_costs(u, v, current_allocations)
            
            # Encontrar celda con mayor potencial de mejora
            best_cell = None
            best_saving = 0
            
            for i in range(self.num_suppliers):
                for j in range(self.num_customers):
                    if (i, j) not in [(a["supplier"], a["customer"]) for a in current_allocations]:
                        opp_cost = opportunity_costs.get((i, j), 0)
                        if opp_cost < best_saving:  # Negativo = ahorro
                            best_saving = opp_cost
                            best_cell = (i, j)
            
            if best_cell is None or best_saving >= 0:
                logger.info(f" Solución óptima alcanzada en iteración {iteration + 1}")
                return {
                    "allocations": current_allocations,
                    "total_cost": current_cost,
                    "is_optimal": True,
                    "iterations": iteration + 1,
                    "improvements": improvements,
                    "method": "MODI"
                }
            
            # Mejorar usando ciclo MODI
            logger.debug(f"  Iteración {iteration + 1}: Encontrado ciclo de mejora en {best_cell}")
            current_allocations, new_cost = self._execute_cycle(best_cell, current_allocations)
            
            saving = current_cost - new_cost
            if saving > 0.01:
                logger.info(f" Mejora: {saving:.2f} Bs (total: {new_cost:.2f} Bs)")
                improvements += 1
                current_cost = new_cost
            else:
                break
        
        return {
            "allocations": current_allocations,
            "total_cost": current_cost,
            "is_optimal": False,
            "iterations": iteration + 1,
            "improvements": improvements,
            "method": "MODI"
        }
    
    def _calculate_multipliers(self, allocations: List[Dict]) -> Tuple[Dict, Dict]:
        u = {}
        v = {}
        
        # Inicializar con None
        for i in range(self.num_suppliers):
            u[i] = None
        for j in range(self.num_customers):
            v[j] = None
        
        # Asignar u[0] = 0 como punto de partida
        u[0] = 0
        
        # Propagar valores usando asignaciones
        changed = True
        iterations = 0
        max_iter = 100
        
        while changed and iterations < max_iter:
            changed = False
            iterations += 1
            
            for alloc in allocations:
                i = alloc["supplier"]
                j = alloc["customer"]
                cost = alloc["unit_cost"]
                
                # u[i] + v[j] = cost
                if u[i] is not None and v[j] is None:
                    v[j] = cost - u[i]
                    changed = True
                elif v[j] is not None and u[i] is None:
                    u[i] = cost - v[j]
                    changed = True
        
        # Validar que se calcularon todos los multiplicadores
        if None in u.values() or None in v.values():
            logger.warning(" No se pudieron calcular todos los multiplicadores (problema degenerado)")
            return None, None
        
        return u, v
    
    def _calculate_opportunity_costs(
        self,
        u: Dict,
        v: Dict,
        allocations: List[Dict]
    ) -> Dict[Tuple, float]:
        assigned_cells = {(a["supplier"], a["customer"]) for a in allocations}
        opportunity_costs = {}
        
        for i in range(self.num_suppliers):
            for j in range(self.num_customers):
                if (i, j) not in assigned_cells:
                    # Costo de oportunidad = costo real - (u[i] + v[j])
                    opp_cost = self.cost_matrix[i][j] - (u[i] + v[j])
                    opportunity_costs[(i, j)] = opp_cost
        
        return opportunity_costs
    
    def _execute_cycle(
        self,
        entering_cell: Tuple[int, int],
        allocations: List[Dict]
    ) -> Tuple[List[Dict], float]:
        i, j = entering_cell
        current_allocations = deepcopy(allocations)

        new_cost = sum(a["total_cost"] for a in current_allocations)
        
        return current_allocations, new_cost
