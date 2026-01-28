"""
Cliente para interactuar con la API de NiceHash
Implementa autenticación HMAC-SHA256 y métodos para obtener estadísticas de minería
"""
import time
import uuid
import hmac
import hashlib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import config


class NiceHashClient:
    def __init__(self):
        """Inicializa el cliente de NiceHash con las credenciales configuradas"""
        config.validate_config()
        self.api_key = config.API_KEY
        self.api_secret = config.API_SECRET
        self.org_id = config.ORG_ID
        self.base_url = config.API_URL
        
    def _generate_signature(self, method: str, path: str, query: str = "", body: str = "") -> tuple:
        """
        Genera la firma HMAC-SHA256 requerida para autenticar requests
        
        Args:
            method: Método HTTP (GET, POST, etc.)
            path: Ruta del endpoint
            query: Query string (sin el ?)
            body: Cuerpo de la petición (si aplica)
            
        Returns:
            Tupla con (timestamp, nonce, signature)
        """
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4())
        
        # Construir el input para la firma según la documentación de NiceHash
        # Formato: API_KEY\x00timestamp\x00nonce\x00\x00org_id\x00\x00method\x00path\x00query\x00body
        message = self.api_key.encode('latin-1')
        message += b'\x00' + timestamp.encode('latin-1')
        message += b'\x00' + nonce.encode('latin-1')
        message += b'\x00'  # Empty field
        message += b'\x00' + self.org_id.encode('latin-1')
        message += b'\x00'  # Empty field
        message += b'\x00' + method.encode('latin-1')
        message += b'\x00' + path.encode('latin-1')
        message += b'\x00' + query.encode('latin-1')
        
        if body:
            message += b'\x00' + body.encode('utf-8')
        
        # Generar firma HMAC-SHA256
        signature = hmac.new(
            self.api_secret.encode('latin-1'),
            message,
            hashlib.sha256
        ).hexdigest()
        
        return timestamp, nonce, signature
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Realiza una petición autenticada a la API de NiceHash
        
        Args:
            method: Método HTTP
            endpoint: Endpoint de la API
            params: Parámetros de la petición
            
        Returns:
            Respuesta JSON de la API
        """
        url = f"{self.base_url}{endpoint}"
        
        # Construir query string si hay parámetros
        query_string = ""
        if params:
            query_parts = [f"{k}={v}" for k, v in sorted(params.items())]
            query_string = "&".join(query_parts)
        
        # Generar firma
        timestamp, nonce, signature = self._generate_signature(
            method, 
            endpoint, 
            query_string
        )
        
        # Preparar headers
        headers = {
            'X-Time': timestamp,
            'X-Nonce': nonce,
            'X-Organization-Id': self.org_id,
            'X-Request-Id': str(uuid.uuid4()),
            'X-Auth': f"{self.api_key}:{signature}",
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Realizar petición
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
            else:
                response = requests.request(method, url, headers=headers, params=params)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Respuesta del servidor: {e.response.text}")
            raise
    
    def get_rigs(self, get_all_pages: bool = True) -> Dict:
        """
        Obtiene información de todos los rigs (mineros)
        
        Args:
            get_all_pages: Si es True, obtiene todos los rigs de todas las páginas
        
        Returns:
            Diccionario con información de los rigs
        """
        # Obtener primera página
        result = self._make_request('GET', '/main/api/v2/mining/rigs')
        
        # Si no queremos todas las páginas o no hay paginación, retornar
        if not get_all_pages or 'pagination' not in result:
            return result
        
        # Obtener información de paginación
        pagination = result['pagination']
        total_pages = pagination.get('totalPageCount', 1)
        
        # Si solo hay una página, retornar
        if total_pages <= 1:
            return result
        
        # Obtener el resto de páginas
        all_rigs = result.get('miningRigs', [])
        
        for page in range(1, total_pages):
            params = {'page': page, 'size': 25}
            page_result = self._make_request('GET', '/main/api/v2/mining/rigs', params)
            all_rigs.extend(page_result.get('miningRigs', []))
        
        # Actualizar el resultado con todos los rigs
        result['miningRigs'] = all_rigs
        result['pagination']['page'] = 0
        result['pagination']['size'] = len(all_rigs)
        
        return result
    
    def get_active_workers(self) -> Dict:
        """
        Obtiene información de los workers activos
        
        Returns:
            Diccionario con información de workers activos
        """
        return self._make_request('GET', '/main/api/v2/mining/rigs/activeWorkers')
    
    def get_rig_stats_algo(self) -> Dict:
        """
        Obtiene estadísticas por algoritmo de los rigs
        
        Returns:
            Diccionario con estadísticas por algoritmo
        """
        return self._make_request('GET', '/main/api/v2/mining/rigs/stats/algo')
    
    def get_daily_earnings(self, from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict:
        """
        Obtiene ganancias diarias en un rango de fechas
        
        Args:
            from_date: Fecha inicial (formato: YYYY-MM-DD), por defecto hace 30 días
            to_date: Fecha final (formato: YYYY-MM-DD), por defecto hoy
            
        Returns:
            Diccionario con ganancias diarias
        """
        if not to_date:
            to_date = datetime.now().strftime('%Y-%m-%d')
        if not from_date:
            from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        params = {
            'fromDate': from_date,
            'toDate': to_date
        }
        return self._make_request('GET', '/main/api/v2/mining/rigs/stats/data', params)
    
    def get_algo_stats(self) -> Dict:
        """
        Obtiene estadísticas generales por algoritmo
        
        Returns:
            Diccionario con estadísticas de algoritmos
        """
        return self._make_request('GET', '/main/api/v2/mining/algo/stats')
    
    def get_payouts(self) -> Dict:
        """
        Obtiene información de pagos realizados
        
        Returns:
            Diccionario con información de payouts
        """
        return self._make_request('GET', '/main/api/v2/mining/rigs/payouts')
    
    def get_mining_address(self) -> Dict:
        """
        Obtiene la dirección de minería configurada
        
        Returns:
            Diccionario con la dirección de minería
        """
        return self._make_request('GET', '/main/api/v2/mining/miningAddress')
    
    def get_unpaid_stats(self) -> Dict:
        """
        Obtiene estadísticas de balance no pagado
        
        Returns:
            Diccionario con balance no pagado
        """
        return self._make_request('GET', '/main/api/v2/mining/rig/stats/unpaid')
    
    def get_account_info(self) -> Dict:
        """
        Obtiene información de la cuenta
        
        Returns:
            Diccionario con información de la cuenta (email, nombre, etc.)
        """
        return self._make_request('GET', '/main/api/v2/accounting/accounts2')
