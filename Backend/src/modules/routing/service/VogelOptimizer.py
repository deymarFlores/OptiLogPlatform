import logging
from typing import List, Dict, Tuple, Any
from copy import deepcopy

logger = logging.getLogger(__name__)


class VogelOptimizer:
    def __init__(
        self, cost_matrix: List[List[float]], supply: List[float], demand: List[float]
    ):
        self.cost_matrix = deepcopy(cost_matrix)
        self.supply = deepcopy(supply)
        self.demand = deepcopy(demand)
        self.allocations = []
        self.total_cost = 0

        if abs(sum(supply) - sum(demand)) > 0.01:
            logger.warning(
                f" Problema no balanceado: Supply={sum(supply)}, Demand={sum(demand)}"
            )

        self.num_suppliers = len(supply)
        self.num_customers = len(demand)

    def solve(self) -> Dict[str, Any]:
        logger.info(" Iniciando algoritmo Vogel...")

        supply = deepcopy(self.supply)
        demand = deepcopy(self.demand)
        cost_matrix = deepcopy(self.cost_matrix)
        allocations = []
        iteration = 0

        active_suppliers = set(range(self.num_suppliers))
        active_customers = set(range(self.num_customers))

        while active_suppliers and active_customers:
            iteration += 1
            logger.debug(
                f"  Iteración {iteration}: {len(active_suppliers)} suppliers, {len(active_customers)} customers"
            )

            row_penalties = {}
            for i in active_suppliers:
                valid_costs = [cost_matrix[i][j] for j in active_customers]
                if len(valid_costs) >= 2:
                    valid_costs.sort()
                    row_penalties[i] = valid_costs[1] - valid_costs[0]
                elif len(valid_costs) == 1:
                    row_penalties[i] = 0
                else:
                    row_penalties[i] = float("inf")

            col_penalties = {}
            for j in active_customers:
                valid_costs = [cost_matrix[i][j] for i in active_suppliers]
                if len(valid_costs) >= 2:
                    valid_costs.sort()
                    col_penalties[j] = valid_costs[1] - valid_costs[0]
                elif len(valid_costs) == 1:
                    col_penalties[j] = 0
                else:
                    col_penalties[j] = float("inf")

            max_row_penalty = max(row_penalties.values()) if row_penalties else 0
            max_col_penalty = max(col_penalties.values()) if col_penalties else 0

            if max_row_penalty >= max_col_penalty:

                supplier_idx = max(row_penalties, key=row_penalties.get)

                best_customer = min(
                    active_customers, key=lambda j: cost_matrix[supplier_idx][j]
                )
            else:

                customer_idx = max(col_penalties, key=col_penalties.get)

                supplier_idx = min(
                    active_suppliers, key=lambda i: cost_matrix[i][customer_idx]
                )
                best_customer = customer_idx

            quantity = min(supply[supplier_idx], demand[best_customer])

            if quantity > 0.01:
                cost = quantity * cost_matrix[supplier_idx][best_customer]
                allocations.append(
                    {
                        "supplier": supplier_idx,
                        "customer": best_customer,
                        "quantity": quantity,
                        "unit_cost": cost_matrix[supplier_idx][best_customer],
                        "total_cost": cost,
                    }
                )
                logger.debug(
                    f"  Asignación: S{supplier_idx} → C{best_customer}: {quantity} @ {cost_matrix[supplier_idx][best_customer]} = {cost}"
                )

            supply[supplier_idx] -= quantity
            demand[best_customer] -= quantity

            if supply[supplier_idx] < 0.01:
                active_suppliers.discard(supplier_idx)
            if demand[best_customer] < 0.01:
                active_customers.discard(best_customer)

        total_cost = sum(alloc["total_cost"] for alloc in allocations)

        logger.info(f" Solución Vogel encontrada en {iteration} iteraciones")
        logger.info(f" Total de asignaciones: {len(allocations)}")
        logger.info(f" Costo total: {total_cost:.2f} Bs")

        return {
            "allocations": allocations,
            "total_cost": total_cost,
            "is_optimal": False,
            "iterations": iteration,
            "method": "Vogel (VAM)",
        }

    def calculate_penalties(self) -> Tuple[Dict, Dict]:
        row_penalties = {}
        for i in range(self.num_suppliers):
            valid_costs = sorted(self.cost_matrix[i])
            if len(valid_costs) >= 2:
                row_penalties[i] = valid_costs[1] - valid_costs[0]

        col_penalties = {}
        for j in range(self.num_customers):
            column = [self.cost_matrix[i][j] for i in range(self.num_suppliers)]
            valid_costs = sorted(column)
            if len(valid_costs) >= 2:
                col_penalties[j] = valid_costs[1] - valid_costs[0]

        return row_penalties, col_penalties
