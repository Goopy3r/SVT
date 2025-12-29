"""
Geolocation service for IP addresses
"""

import time
import requests
from typing import Dict, Any

class GeoLocator:
    def __init__(self):
        self.cache = {}
        
    def get_location(self, ip: str) -> Dict[str, Any]:
        """Get geolocation for IP address"""
        if ip in self.cache:
            if time.time() - self.cache[ip]['timestamp'] < 86400:
                return self.cache[ip]['data']
        
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    result = {
                        'country': data.get('countryCode', 'Unknown'),
                        'country_name': data.get('country', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'lat': data.get('lat', 0),
                        'lon': data.get('lon', 0),
                        'isp': data.get('isp', 'Unknown'),
                        'timestamp': time.time()
                    }
                    
                    self.cache[ip] = {'data': result, 'timestamp': time.time()}
                    return result
                    
        except Exception as e:
            print(f"Geo error for {ip}: {e}")
        
        # Fallback result
        result = {
            'country': 'Unknown',
            'country_name': 'Unknown',
            'region': 'Unknown',
            'city': 'Unknown',
            'lat': 0,
            'lon': 0,
            'isp': 'Unknown',
            'timestamp': time.time()
        }
        
        self.cache[ip] = {'data': result, 'timestamp': time.time()}
        return result