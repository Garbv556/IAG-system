import time
import math
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class PerformanceSnapshot:
    cycle: int
    avg_mastery: float
    std_dev: float
    system_efficiency: float

class RefinementEngine:
    def __init__(self, system_name: str):
        self.system_name = system_name
        self.cycle = 0
        self.generation = 1
        
        self.global_params = {
            "solo_speed_multiplier": 1.0,
            "group_boost_multiplier": 1.0,
            "peer_teach_rate": 0.35, # probability of explicit teaching vs self learning
            "convergence_bonus": 0.1,
        }
        
        self.efficiency_history: List[float] = []
        self.snapshots: List[PerformanceSnapshot] = []
        self.events: List[Dict[str, Any]] = []
        
    def _std_dev(self, values: List[float]) -> float:
        if not values: return 0.0
        mean = sum(values) / len(values)
        return math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))
        
    def run_cycle(self, masteries: Dict[str, float]) -> List[Dict[str, Any]]:
        self.cycle += 1
        new_events = []
        
        vals = list(masteries.values())
        avg = sum(vals) / len(vals) if vals else 0.0
        std_dev = self._std_dev(vals)
        
        # 1. Stagnation Detection
        if len(self.efficiency_history) >= 3:
            recent = self.efficiency_history[-3:]
            if max(recent) - min(recent) < 0.01: 
                old = self.global_params["peer_teach_rate"]
                self.global_params["peer_teach_rate"] = min(0.9, old + 0.15)
                new_events.append({
                    "reason": "Estagnação",
                    "log": "Matriz detectou estagnação térmica. Forçando ensino cruzado (Peer-Teaching).",
                    "param": "peer_teach_rate", "new_val": self.global_params["peer_teach_rate"]
                })
                
        # 2. Slow Progress Check -> Boost Solo (Ignora ciclo 1 para evitar spam inicial)
        if self.cycle > 1 and avg < 0.35 and self.global_params["solo_speed_multiplier"] < 2.0:
            self.global_params["solo_speed_multiplier"] = min(2.0, self.global_params["solo_speed_multiplier"] * 1.15)
            new_events.append({
                "reason": "Progresso Lento",
                "log": f"Média baixa ({avg:.0%}). Acelerando overclock individual dos nós.",
                "param": "solo_speed_multiplier", "new_val": self.global_params["solo_speed_multiplier"]
            })
            
        # 3. High Gap / Standard Deviation -> Boost Group Dynamics
        if std_dev > 0.20 and self.global_params["group_boost_multiplier"] < 2.5:
            self.global_params["group_boost_multiplier"] = min(2.5, self.global_params["group_boost_multiplier"] * 1.2)
            new_events.append({
                "reason": "Alta Dispersão",
                "log": f"Dissonância na rede (Gap alto: {std_dev:.2f}). Amplificando bônus de campo coletivo.",
                "param": "group_boost_multiplier", "new_val": self.global_params["group_boost_multiplier"]
            })
            
        # 4. Convergence Bonus
        if avg > 0.6 and std_dev < 0.1:
            self.global_params["convergence_bonus"] = min(0.3, self.global_params["convergence_bonus"] + 0.05)
            new_events.append({
                "reason": "Convergência",
                "log": f"Sincronismo detectado! Nós entrando em ressonância (Bônus ativo).",
                "param": "convergence_bonus", "new_val": self.global_params["convergence_bonus"]
            })
            
        # 5. Generation Evolution
        if avg > 0.90 and self.generation < 10:
            self.generation += 1
            self.global_params["solo_speed_multiplier"] = max(0.8, self.global_params["solo_speed_multiplier"] * 0.7)
            self.global_params["group_boost_multiplier"] = max(0.8, self.global_params["group_boost_multiplier"] * 0.7)
            new_events.append({
                "reason": "Evolução",
                "log": f"⚡ SALTO DIMENSIONAL: GERAÇÃO {self.generation}. Limite de complexidade elevado.",
                "param": "generation", "new_val": self.generation
            })
        
        eff = max(0, avg - std_dev * 0.5)
        self.efficiency_history.append(eff)
        if len(self.efficiency_history) > 10:
            self.efficiency_history.pop(0)

        self.snapshots.append(PerformanceSnapshot(self.cycle, avg, std_dev, eff))
        self.events.extend(new_events)
        return new_events
