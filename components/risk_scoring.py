"""
Risk scoring engine for network connections
"""

import statistics
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Any, Deque

from settings import RISK_WEIGHTS, COUNTRY_RISKS, SUSPICIOUS_PORTS

class RiskScoringEngine:
    def __init__(self, blocking_manager):
        self.blocking_manager = blocking_manager
        self.ip_scores: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'score': 0, 
            'history': deque(maxlen=50)
        })
        self.process_scores: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            'score': 0, 
            'history': deque(maxlen=50)
        })
        
    def calculate_ip_risk(self, ip: str, data: Dict[str, Any]) -> float:
        """Calculate risk score for an IP address"""
        score = 0.0
        
        # Check if already blocked
        if self.blocking_manager.is_ip_blocked(ip):
            score += 5.0
        
        # VirusTotal reputation
        vt_malicious = data.get('vt_malicious', 0)
        vt_suspicious = data.get('vt_suspicious', 0)
        score += (vt_malicious * 5 + vt_suspicious * 2) * RISK_WEIGHTS['vt_malicious']
        
        # Port risk
        if data.get('port') in SUSPICIOUS_PORTS:
            score += RISK_WEIGHTS['suspicious_port']
        
        # Geographic risk
        country = data.get('country', 'Unknown')
        geo_score = COUNTRY_RISKS.get(country, 0.3)
        score += geo_score * RISK_WEIGHTS['geo_risk']
        
        # Normalize to 0-10 scale
        score = min(score * 3, 10)
        
        # Update cache with history
        self.ip_scores[ip]['history'].append(score)
        self.ip_scores[ip]['score'] = statistics.mean(self.ip_scores[ip]['history']) if self.ip_scores[ip]['history'] else score
        
        return self.ip_scores[ip]['score']
    
    def calculate_process_risk(self, process_name: str, connections: List[Dict[str, Any]]) -> float:
        """Calculate risk score for a process"""
        score = 0.0
        
        # Check if already blocked
        if self.blocking_manager.is_process_blocked(process_name):
            score += 5.0
        
        # Connection patterns
        if connections:
            suspicious_ports = sum(1 for conn in connections if conn.get('port') in SUSPICIOUS_PORTS)
            if suspicious_ports > 0:
                score += min(suspicious_ports * 0.3, 2.0)
            
            # High number of connections
            if len(connections) > 20:
                score += min((len(connections) - 20) * 0.05, 1.0)
        
        # Normalize to 0-10 scale
        score = min(score, 10)
        
        # Update cache with history
        self.process_scores[process_name]['history'].append(score)
        self.process_scores[process_name]['score'] = (
            statistics.mean(self.process_scores[process_name]['history']) 
            if self.process_scores[process_name]['history'] else score
        )
        
        return self.process_scores[process_name]['score']
    
    def get_risk_level(self, score: float) -> Tuple[str, str]:
        """Convert numeric score to risk level and color"""
        if score < 3:
            return "LOW", "#00ff00"
        elif score < 6:
            return "MEDIUM", "#ffff00"
        elif score < 8:
            return "HIGH", "#ff6600"
        else:
            return "CRITICAL", "#ff0000"