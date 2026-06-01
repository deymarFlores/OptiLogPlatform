import requests
import asyncio
from typing import List, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)

class OSRMService:
    
    # API pública de OSRM
    OSRM_BASE_URL = "https://router.project-osrm.org"
    
    @staticmethod
    async def get_distance_matrix(
        coordinates: List[Tuple[float, float]],
        sources: List[int] = None,
        destinations: List[int] = None
    ) -> Dict[str, Any]:
        try:
            # Validar coordenadas
            if not coordinates or len(coordinates) < 2:
                raise ValueError("Se requieren al menos 2 coordenadas")
            
            coords_str = ";".join([f"{lng},{lat}" for lat, lng in coordinates])
            url = f"{OSRMService.OSRM_BASE_URL}/table/v1/driving/{coords_str}"
            params = {
                "annotations": "distance,duration"  # Obtener distancias y tiempos
            }
            
            if sources:
                params["sources"] = ";".join(map(str, sources))
            if destinations:
                params["destinations"] = ";".join(map(str, destinations))
            
            logger.info(f" Consultando OSRM: {url}")
            
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("code") != "Ok":
                error_msg = f"OSRM error: {data.get('message', 'Unknown error')}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            result = {
                "distances": data.get("distances", []),
                "durations": data.get("durations", []),
                "sources": data.get("sources", list(range(len(coordinates)))),
                "destinations": data.get("destinations", list(range(len(coordinates))))
            }
            
            logger.info(f" Matriz de distancias obtenida: {len(result['distances'])}x{len(result['distances'][0]) if result['distances'] else 0}")
            return result
            
        except requests.exceptions.Timeout:
            logger.error(" Timeout al consultar OSRM (>30s)")
            raise Exception("OSRM request timeout")
        except requests.exceptions.RequestException as e:
            logger.error(f" Error en solicitud OSRM: {str(e)}")
            raise Exception(f"OSRM request failed: {str(e)}")
        except Exception as e:
            logger.error(f" Error inesperado en OSRM: {str(e)}")
            raise
    
    @staticmethod
    async def get_route(
        start: Tuple[float, float],
        end: Tuple[float, float],
        alternatives: bool = False
    ) -> Dict[str, Any]:
        try:
            start_lng, start_lat = start[1], start[0]
            end_lng, end_lat = end[1], end[0]
            
            coords_str = f"{start_lng},{start_lat};{end_lng},{end_lat}"
            url = f"{OSRMService.OSRM_BASE_URL}/route/v1/driving/{coords_str}"
            
            params = {
                "alternatives": "true" if alternatives else "false",
                "steps": "true",
                "annotations": "distance,duration,nodes"
            }
            
            logger.info(f" Consultando ruta OSRM: {start} → {end}")
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("code") != "Ok":
                error_msg = f"OSRM error: {data.get('message', 'Unknown error')}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            routes = data.get("routes", [])
            if not routes:
                raise ValueError("No routes found")
            
            logger.info(f"✅ Ruta obtenida: {routes[0]['distance']}m, {routes[0]['duration']}s")
            
            return {
                "routes": routes,
                "code": data.get("code")
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo ruta: {str(e)}")
            raise
    
    @staticmethod
    def convert_distances_to_costs(
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
        
        logger.info(f" Matriz de costos generada: {len(cost_matrix)}x{len(cost_matrix[0]) if cost_matrix else 0}")
        return cost_matrix
