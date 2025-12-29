"""
VirusTotal API integration
"""

import time
from typing import Dict, Any, List
import requests

class VirusTotalAnalyzer:
    def __init__(self, api_keys: List[str]):
        self.api_keys = api_keys
        self.current_key_index = 0
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.request_count = 0
        
    def get_next_key(self) -> str:
        """Rotate through API keys"""
        key = self.api_keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return key
    
    def check_ip(self, ip: str) -> Dict[str, Any]:
        """Check IP reputation"""
        cache_key = f"ip_{ip}"
        if cache_key in self.cache:
            if time.time() - self.cache[cache_key]['timestamp'] < 3600:
                return self.cache[cache_key]['data']
        
        try:
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
            headers = {"x-apikey": self.get_next_key()}
            
            response = requests.get(url, headers=headers, timeout=5)
            self.request_count += 1
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                
                result = {
                    'malicious': stats.get('malicious', 0),
                    'suspicious': stats.get('suspicious', 0),
                    'harmless': stats.get('harmless', 0),
                    'undetected': stats.get('undetected', 0),
                    'as_owner': data.get("data", {}).get("attributes", {}).get("as_owner", "Unknown"),
                    'timestamp': time.time()
                }
                
                self.cache[cache_key] = {
                    'data': result,
                    'timestamp': time.time()
                }
                
                return result
            elif response.status_code == 429:
                time.sleep(1)
                return self.check_ip(ip)
                
        except Exception as e:
            print(f"VT error for {ip}: {e}")
        
        return {
            'malicious': 0, 
            'suspicious': 0, 
            'harmless': 0, 
            'undetected': 0, 
            'as_owner': 'Unknown', 
            'timestamp': time.time()
        }
    
    def check_domain(self, domain: str) -> Dict[str, Any]:
        """Check domain reputation"""
        cache_key = f"domain_{domain}"
        if cache_key in self.cache:
            if time.time() - self.cache[cache_key]['timestamp'] < 3600:
                return self.cache[cache_key]['data']
        
        try:
            url = f"https://www.virustotal.com/api/v3/domains/{domain}"
            headers = {"x-apikey": self.get_next_key()}
            
            response = requests.get(url, headers=headers, timeout=5)
            self.request_count += 1
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                
                result = {
                    'malicious': stats.get('malicious', 0),
                    'suspicious': stats.get('suspicious', 0),
                    'harmless': stats.get('harmless', 0),
                    'undetected': stats.get('undetected', 0),
                    'timestamp': time.time()
                }
                
                self.cache[cache_key] = {
                    'data': result,
                    'timestamp': time.time()
                }
                
                return result
                
        except Exception as e:
            print(f"VT domain error for {domain}: {e}")
        
        return {
            'malicious': 0, 
            'suspicious': 0, 
            'harmless': 0, 
            'undetected': 0, 
            'timestamp': time.time()
        }