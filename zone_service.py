from typing import List, Dict, Any, Optional
from datetime import datetime
from app.risk_engine.engine import RiskEngine

CHANDIGARH_PILOT_ZONES = [
    {
        "id": 1,
        "zone_code": "CHD-SEC-17",
        "zone_name": "Sector 17 (City Centre Commercial Core)",
        "representative_latitude": 30.7398,
        "representative_longitude": 76.7827,
        "elevation_m": 348.0,
        "baseline_drainage_factor": 45.0,  # Well planned storm drains, high impermeable surface
        "mapped_drain_count": 2,
        "description": "Pedestrian plaza and civic commercial hub with extensive paved coverage. Vulnerable to flash surface ponding around underpasses during intense downpours.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.7760, 30.7440],
                [76.7890, 30.7440],
                [76.7890, 30.7350],
                [76.7760, 30.7350],
                [76.7760, 30.7440]
            ]]
        }
    },
    {
        "id": 2,
        "zone_code": "CHD-SEC-22",
        "zone_name": "Sector 22 (Dense Mixed Urban Market)",
        "representative_latitude": 30.7288,
        "representative_longitude": 76.7725,
        "elevation_m": 341.0,
        "baseline_drainage_factor": 58.0,  # Heavy commercial encroachments, narrow back lanes
        "mapped_drain_count": 1,
        "description": "High footfall Shastri Market corridor. High solid waste and silt accumulation near roadside gully traps reduces storm discharge rate.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.7660, 30.7340],
                [76.7790, 30.7340],
                [76.7790, 30.7230],
                [76.7660, 30.7230],
                [76.7660, 30.7340]
            ]]
        }
    },
    {
        "id": 3,
        "zone_code": "CHD-SEC-35",
        "zone_name": "Sector 35 (Commercial & Hotel Avenue)",
        "representative_latitude": 30.7225,
        "representative_longitude": 76.7589,
        "elevation_m": 336.0,
        "baseline_drainage_factor": 48.0,
        "mapped_drain_count": 2,
        "description": "Commercial arterial avenue near Dakshin Marg. Moderate drainage resilience, roadside depressions along service roads prone to standing water.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.7520, 30.7280],
                [76.7650, 30.7280],
                [76.7650, 30.7170],
                [76.7520, 30.7170],
                [76.7520, 30.7280]
            ]]
        }
    },
    {
        "id": 4,
        "zone_code": "CHD-IND-01",
        "zone_name": "Industrial Area Phase I (Low-lying Pocket)",
        "representative_latitude": 30.7055,
        "representative_longitude": 76.8012,
        "elevation_m": 322.0,
        "baseline_drainage_factor": 75.0,  # Low-lying, industrial runoff, choked open conduits
        "mapped_drain_count": 3,
        "description": "Topographical depression adjacent to Sukhna Choe spillway. Historically documented chronic waterlogging hotspot under rainfall > 25mm/hr.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.7930, 30.7130],
                [76.8110, 30.7130],
                [76.8110, 30.6980],
                [76.7930, 30.6980],
                [76.7930, 30.7130]
            ]]
        }
    },
    {
        "id": 5,
        "zone_code": "CHD-IND-02",
        "zone_name": "Industrial Area Phase II (Transit Corridor)",
        "representative_latitude": 30.6942,
        "representative_longitude": 76.7925,
        "elevation_m": 318.0,
        "baseline_drainage_factor": 68.0,
        "mapped_drain_count": 2,
        "description": "Downstream industrial sector with heavy vehicular movement and railway underpasses susceptible to rapid water entrapment.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.7850, 30.7010],
                [76.8020, 30.7010],
                [76.8020, 30.6870],
                [76.7850, 30.6870],
                [76.7850, 30.7010]
            ]]
        }
    },
    {
        "id": 6,
        "zone_code": "CHD-SEC-43",
        "zone_name": "Sector 43 (ISBT Bus Terminal & High Density Hub)",
        "representative_latitude": 30.7180,
        "representative_longitude": 76.7410,
        "elevation_m": 329.0,
        "baseline_drainage_factor": 62.0,
        "mapped_drain_count": 2,
        "description": "Regional transit interchange connecting Punjab and Haryana. Bus parking aprons and terminal entry ramps experience recurrent ponding.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.7340, 30.7240],
                [76.7480, 30.7240],
                [76.7480, 30.7120],
                [76.7340, 30.7120],
                [76.7340, 30.7240]
            ]]
        }
    },
    {
        "id": 7,
        "zone_code": "CHD-SUK-01",
        "zone_name": "Sukhna Lake Catchment & Enclave",
        "representative_latitude": 30.7421,
        "representative_longitude": 76.8188,
        "elevation_m": 362.0,
        "baseline_drainage_factor": 38.0,  # High elevation, rapid runoff into reservoir
        "mapped_drain_count": 3,
        "description": "Shivalik foothills catchment rim. Rapid surface runoff generation that feeds Sukhna Choe. Low local pooling, but high discharge transmitter.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.8090, 30.7510],
                [76.8280, 30.7510],
                [76.8280, 30.7330],
                [76.8090, 30.7330],
                [76.8090, 30.7510]
            ]]
        }
    },
    {
        "id": 8,
        "zone_code": "CHD-MAN-01",
        "zone_name": "Manimajra (Low-lying Urban Settlement)",
        "representative_latitude": 30.7245,
        "representative_longitude": 76.8450,
        "elevation_m": 326.0,
        "baseline_drainage_factor": 72.0,  # Dense organic layout, old brick masonry conduits
        "mapped_drain_count": 1,
        "description": "High-density peri-urban settlement across the railway tracks. Legacy underground storm network overloaded during cloudburst events.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.8350, 30.7320],
                [76.8550, 30.7320],
                [76.8550, 30.7170],
                [76.8350, 30.7170],
                [76.8350, 30.7320]
            ]]
        }
    },
    {
        "id": 9,
        "zone_code": "CHD-SEC-26",
        "zone_name": "Sector 26 (Grain Market & Transport Area)",
        "representative_latitude": 30.7290,
        "representative_longitude": 76.8090,
        "elevation_m": 339.0,
        "baseline_drainage_factor": 64.0,  # Heavy commercial loading, organic debris clogging
        "mapped_drain_count": 2,
        "description": "Mandi market and wholesale transport corridor with frequent vegetative clogging in roadside catchpits.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.8010, 30.7360],
                [76.8170, 30.7360],
                [76.8170, 30.7220],
                [76.8010, 30.7220],
                [76.8010, 30.7360]
            ]]
        }
    },
    {
        "id": 10,
        "zone_code": "CHD-DHA-01",
        "zone_name": "Dhanas (Peripheral Settlement / Choe Corridor)",
        "representative_latitude": 30.7580,
        "representative_longitude": 76.7490,
        "elevation_m": 335.0,
        "baseline_drainage_factor": 66.0,
        "mapped_drain_count": 1,
        "description": "North-western periphery bordering Patiala Ki Rao stream. Surface soil siltation causes backflow into service roads during high channel levels.",
        "boundary_geojson": {
            "type": "Polygon",
            "coordinates": [[
                [76.7390, 30.7670],
                [76.7590, 30.7670],
                [76.7590, 30.7490],
                [76.7390, 30.7490],
                [76.7390, 30.7670]
            ]]
        }
    }
]

class ZoneService:
    def __init__(self):
        self.zones = CHANDIGARH_PILOT_ZONES

    def get_all_zones(self) -> List[Dict[str, Any]]:
        return self.zones

    def get_zone_by_id(self, zone_id: int) -> Optional[Dict[str, Any]]:
        for z in self.zones:
            if z["id"] == zone_id:
                return z
        return None

    def assess_all_zones(self, weather_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        assessments = []
        for zone in self.zones:
            assessment = RiskEngine.assess_zone(
                rainfall_1h=weather_data.get("rainfall_1h", 0.0),
                rainfall_3h=weather_data.get("rainfall_3h", 0.0),
                rainfall_24h=weather_data.get("rainfall_24h", 0.0),
                forecast_6h=weather_data.get("forecast_6h", 0.0),
                forecast_24h=weather_data.get("forecast_24h", 0.0),
                baseline_drainage_factor=zone["baseline_drainage_factor"],
                mapped_drain_count=zone["mapped_drain_count"],
                elevation_m=zone["elevation_m"],
                has_live_weather=weather_data.get("is_live", True),
                has_elevation_sample=True,
                has_drainage_features=True,
                verified_reports_count=1 if zone["id"] in [4, 8] else 0
            )
            assessment["zone_id"] = zone["id"]
            assessment["zone_code"] = zone["zone_code"]
            assessment["zone_name"] = zone["zone_name"]
            assessment["elevation_m"] = zone["elevation_m"]
            assessments.append(assessment)
            
        # Sort descending by overall risk score
        assessments.sort(key=lambda x: x["overall_risk_score"], reverse=True)
        for rank, item in enumerate(assessments, start=1):
            item["priority_rank"] = rank
            
        return assessments

zone_service = ZoneService()
