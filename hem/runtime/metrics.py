from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MetricsAPI:
    build_time_ms: float = 0.0
    assets_count: int = 0
    providers_count: int = 0
    entities_count: int = 0
    health_score: int = 100
    health_status: str = "HEALTHY"


class MetricsCollector:

    @staticmethod
    def collect(context) -> MetricsAPI:
        from hem.doctor.doctor_manager import DoctorManager
        doc_mgr = DoctorManager()

        # Perform a silent diagnosis run
        old_console_print = doc_mgr.diagnose
        health = old_console_print(context)

        return MetricsAPI(
            build_time_ms=context.statistics.build_time_ms,
            assets_count=context.statistics.assets_loaded,
            providers_count=len(context.statistics.providers_used),
            entities_count=context.statistics.entities_generated,
            health_score=health.score,
            health_status=health.status,
        )
