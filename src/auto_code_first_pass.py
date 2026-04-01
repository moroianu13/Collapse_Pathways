from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

try:
    from .config import (
        COLLAPSE_DATASET_PATH,
        PROCESSED_DATA_DIR,
        REFERENCES_SOURCES_DIR,
        REPORTS_DIR,
    )
    from .dataset_utils import get_factor_columns, validate_factor_values
except ImportError:
    from config import COLLAPSE_DATASET_PATH, PROCESSED_DATA_DIR, REFERENCES_SOURCES_DIR, REPORTS_DIR
    from dataset_utils import get_factor_columns, validate_factor_values


FACTOR_COLUMNS = get_factor_columns()
PHASE_SOURCE_CAP = {
    "stable": 3,
    "stressed": 4,
    "decline": 5,
    "collapse": 6,
    "post-collapse": 4,
}
CONFIDENCE_ADJUSTMENT = {
    "low": -1,
    "medium": 0,
    "high": 1,
}


def unknown_scores() -> dict[str, int]:
    return {column: 9 for column in FACTOR_COLUMNS}


TEMPLATES: dict[str, dict[str, int]] = {
    "stable_empire": {
        "political_fragmentation": 0,
        "elite_conflict": 1,
        "succession_crisis": 1,
        "legitimacy_crisis": 0,
        "administrative_overload": 1,
        "social_unrest_rebellion": 0,
        "urban_decline": 0,
        "fiscal_crisis": 0,
        "taxation_extraction_pressure": 1,
        "trade_disruption": 0,
        "resource_dependency": 1,
        "food_insecurity": 0,
        "external_invasion_pressure": 1,
        "civil_war_internal_conflict": 0,
        "military_overstretch": 1,
        "territorial_loss": 0,
        "institutional_rigidity": 1,
        "adaptive_capacity": 3,
        "logistics_food_storage_resilience": 3,
        "alliance_network_strength": 2,
        "recovery_capacity": 3,
    },
    "stressed_empire": {
        "political_fragmentation": 1,
        "elite_conflict": 2,
        "succession_crisis": 1,
        "legitimacy_crisis": 1,
        "administrative_overload": 2,
        "social_unrest_rebellion": 1,
        "urban_decline": 1,
        "fiscal_crisis": 1,
        "taxation_extraction_pressure": 2,
        "trade_disruption": 1,
        "resource_dependency": 1,
        "agricultural_decline": 1,
        "food_insecurity": 1,
        "external_invasion_pressure": 2,
        "civil_war_internal_conflict": 1,
        "military_overstretch": 2,
        "territorial_loss": 1,
        "institutional_rigidity": 2,
        "adaptive_capacity": 2,
        "logistics_food_storage_resilience": 2,
        "alliance_network_strength": 2,
        "recovery_capacity": 2,
    },
    "decline_empire": {
        "political_fragmentation": 2,
        "elite_conflict": 2,
        "succession_crisis": 2,
        "legitimacy_crisis": 2,
        "administrative_overload": 2,
        "corruption_governance_failure": 2,
        "social_inequality": 2,
        "social_unrest_rebellion": 2,
        "migration_pressure": 1,
        "urban_decline": 2,
        "fiscal_crisis": 2,
        "taxation_extraction_pressure": 2,
        "trade_disruption": 2,
        "resource_dependency": 2,
        "agricultural_decline": 1,
        "food_insecurity": 2,
        "external_invasion_pressure": 2,
        "civil_war_internal_conflict": 2,
        "military_overstretch": 2,
        "territorial_loss": 2,
        "institutional_rigidity": 2,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "collapse_empire": {
        "political_fragmentation": 3,
        "elite_conflict": 3,
        "succession_crisis": 3,
        "legitimacy_crisis": 3,
        "administrative_overload": 3,
        "corruption_governance_failure": 2,
        "social_inequality": 2,
        "social_unrest_rebellion": 2,
        "migration_pressure": 2,
        "urban_decline": 3,
        "fiscal_crisis": 3,
        "taxation_extraction_pressure": 2,
        "trade_disruption": 2,
        "resource_dependency": 2,
        "agricultural_decline": 2,
        "food_insecurity": 2,
        "external_invasion_pressure": 3,
        "civil_war_internal_conflict": 2,
        "military_overstretch": 3,
        "territorial_loss": 3,
        "institutional_rigidity": 3,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "postcollapse_empire": {
        "political_fragmentation": 3,
        "elite_conflict": 2,
        "succession_crisis": 1,
        "legitimacy_crisis": 2,
        "administrative_overload": 2,
        "social_unrest_rebellion": 1,
        "migration_pressure": 2,
        "urban_decline": 2,
        "fiscal_crisis": 2,
        "trade_disruption": 2,
        "resource_dependency": 2,
        "food_insecurity": 1,
        "external_invasion_pressure": 2,
        "civil_war_internal_conflict": 1,
        "military_overstretch": 2,
        "territorial_loss": 3,
        "institutional_rigidity": 2,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "stable_regional": {
        "political_fragmentation": 0,
        "elite_conflict": 1,
        "legitimacy_crisis": 0,
        "administrative_overload": 1,
        "social_unrest_rebellion": 0,
        "urban_decline": 0,
        "fiscal_crisis": 0,
        "trade_disruption": 1,
        "resource_dependency": 2,
        "food_insecurity": 0,
        "external_invasion_pressure": 1,
        "civil_war_internal_conflict": 1,
        "military_overstretch": 1,
        "territorial_loss": 0,
        "institutional_rigidity": 1,
        "adaptive_capacity": 2,
        "logistics_food_storage_resilience": 2,
        "alliance_network_strength": 2,
        "recovery_capacity": 2,
    },
    "stressed_regional": {
        "political_fragmentation": 1,
        "elite_conflict": 2,
        "legitimacy_crisis": 1,
        "administrative_overload": 2,
        "social_unrest_rebellion": 1,
        "urban_decline": 1,
        "fiscal_crisis": 1,
        "trade_disruption": 2,
        "resource_dependency": 2,
        "agricultural_decline": 1,
        "food_insecurity": 1,
        "external_invasion_pressure": 2,
        "civil_war_internal_conflict": 1,
        "military_overstretch": 2,
        "territorial_loss": 1,
        "institutional_rigidity": 2,
        "adaptive_capacity": 2,
        "logistics_food_storage_resilience": 2,
        "alliance_network_strength": 1,
        "recovery_capacity": 2,
    },
    "decline_regional": {
        "political_fragmentation": 2,
        "elite_conflict": 2,
        "legitimacy_crisis": 2,
        "administrative_overload": 2,
        "social_unrest_rebellion": 1,
        "migration_pressure": 1,
        "urban_decline": 2,
        "fiscal_crisis": 1,
        "trade_disruption": 2,
        "resource_dependency": 2,
        "agricultural_decline": 2,
        "drought_climate_stress": 2,
        "food_insecurity": 2,
        "external_invasion_pressure": 2,
        "civil_war_internal_conflict": 1,
        "military_overstretch": 2,
        "territorial_loss": 2,
        "institutional_rigidity": 2,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "collapse_regional": {
        "political_fragmentation": 3,
        "elite_conflict": 2,
        "legitimacy_crisis": 2,
        "administrative_overload": 2,
        "social_unrest_rebellion": 1,
        "migration_pressure": 2,
        "urban_decline": 3,
        "trade_disruption": 3,
        "resource_dependency": 2,
        "agricultural_decline": 2,
        "drought_climate_stress": 2,
        "food_insecurity": 2,
        "external_invasion_pressure": 3,
        "military_overstretch": 3,
        "territorial_loss": 3,
        "institutional_rigidity": 3,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "postcollapse_regional": {
        "political_fragmentation": 3,
        "urban_decline": 2,
        "trade_disruption": 2,
        "resource_dependency": 1,
        "agricultural_decline": 1,
        "food_insecurity": 1,
        "territorial_loss": 2,
        "institutional_rigidity": 2,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "stable_modern": {
        "political_fragmentation": 0,
        "elite_conflict": 1,
        "succession_crisis": 0,
        "legitimacy_crisis": 0,
        "administrative_overload": 2,
        "corruption_governance_failure": 1,
        "social_inequality": 1,
        "social_unrest_rebellion": 0,
        "demographic_pressure": 0,
        "migration_pressure": 0,
        "ethnic_sectarian_fragmentation": 1,
        "urban_decline": 0,
        "fiscal_crisis": 0,
        "taxation_extraction_pressure": 0,
        "trade_disruption": 0,
        "inflation_currency_instability": 0,
        "resource_dependency": 1,
        "agricultural_decline": 0,
        "drought_climate_stress": 0,
        "flood_environmental_shock": 0,
        "temperature_anomaly": 0,
        "ecological_degradation": 0,
        "food_insecurity": 0,
        "external_invasion_pressure": 0,
        "civil_war_internal_conflict": 0,
        "military_overstretch": 1,
        "territorial_loss": 0,
        "institutional_rigidity": 1,
        "adaptive_capacity": 3,
        "logistics_food_storage_resilience": 3,
        "alliance_network_strength": 2,
        "recovery_capacity": 3,
    },
    "stressed_modern": {
        "political_fragmentation": 1,
        "elite_conflict": 2,
        "succession_crisis": 0,
        "legitimacy_crisis": 1,
        "administrative_overload": 2,
        "corruption_governance_failure": 2,
        "social_inequality": 2,
        "social_unrest_rebellion": 1,
        "demographic_pressure": 1,
        "migration_pressure": 1,
        "ethnic_sectarian_fragmentation": 2,
        "urban_decline": 0,
        "fiscal_crisis": 1,
        "taxation_extraction_pressure": 0,
        "trade_disruption": 1,
        "inflation_currency_instability": 1,
        "resource_dependency": 2,
        "agricultural_decline": 0,
        "drought_climate_stress": 0,
        "flood_environmental_shock": 0,
        "temperature_anomaly": 0,
        "ecological_degradation": 0,
        "food_insecurity": 0,
        "external_invasion_pressure": 0,
        "civil_war_internal_conflict": 0,
        "military_overstretch": 2,
        "territorial_loss": 0,
        "institutional_rigidity": 2,
        "adaptive_capacity": 2,
        "logistics_food_storage_resilience": 2,
        "alliance_network_strength": 2,
        "recovery_capacity": 2,
    },
    "decline_modern": {
        "political_fragmentation": 2,
        "elite_conflict": 2,
        "succession_crisis": 1,
        "legitimacy_crisis": 3,
        "administrative_overload": 3,
        "corruption_governance_failure": 2,
        "social_inequality": 2,
        "social_unrest_rebellion": 2,
        "demographic_pressure": 1,
        "migration_pressure": 1,
        "ethnic_sectarian_fragmentation": 2,
        "urban_decline": 1,
        "fiscal_crisis": 2,
        "taxation_extraction_pressure": 0,
        "trade_disruption": 2,
        "inflation_currency_instability": 2,
        "resource_dependency": 2,
        "agricultural_decline": 0,
        "drought_climate_stress": 0,
        "flood_environmental_shock": 0,
        "temperature_anomaly": 0,
        "ecological_degradation": 0,
        "food_insecurity": 1,
        "external_invasion_pressure": 0,
        "civil_war_internal_conflict": 1,
        "military_overstretch": 2,
        "territorial_loss": 1,
        "institutional_rigidity": 3,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "collapse_modern": {
        "political_fragmentation": 3,
        "elite_conflict": 3,
        "succession_crisis": 2,
        "legitimacy_crisis": 3,
        "administrative_overload": 3,
        "corruption_governance_failure": 2,
        "social_inequality": 2,
        "social_unrest_rebellion": 2,
        "demographic_pressure": 1,
        "migration_pressure": 2,
        "ethnic_sectarian_fragmentation": 3,
        "urban_decline": 1,
        "fiscal_crisis": 3,
        "taxation_extraction_pressure": 0,
        "trade_disruption": 3,
        "inflation_currency_instability": 2,
        "resource_dependency": 2,
        "agricultural_decline": 0,
        "drought_climate_stress": 0,
        "flood_environmental_shock": 0,
        "temperature_anomaly": 0,
        "ecological_degradation": 0,
        "food_insecurity": 1,
        "external_invasion_pressure": 0,
        "civil_war_internal_conflict": 3,
        "military_overstretch": 2,
        "territorial_loss": 3,
        "institutional_rigidity": 3,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "postcollapse_modern": {
        "political_fragmentation": 3,
        "elite_conflict": 2,
        "succession_crisis": 1,
        "legitimacy_crisis": 2,
        "administrative_overload": 2,
        "corruption_governance_failure": 2,
        "social_inequality": 2,
        "social_unrest_rebellion": 1,
        "migration_pressure": 2,
        "ethnic_sectarian_fragmentation": 2,
        "urban_decline": 1,
        "fiscal_crisis": 2,
        "trade_disruption": 2,
        "inflation_currency_instability": 2,
        "food_insecurity": 1,
        "civil_war_internal_conflict": 1,
        "territorial_loss": 3,
        "institutional_rigidity": 2,
        "adaptive_capacity": 1,
        "logistics_food_storage_resilience": 1,
        "alliance_network_strength": 1,
        "recovery_capacity": 1,
    },
    "transformation_island": {
        "political_fragmentation": 9,
        "elite_conflict": 9,
        "succession_crisis": 9,
        "legitimacy_crisis": 9,
        "administrative_overload": 9,
        "corruption_governance_failure": 9,
        "social_inequality": 1,
        "social_unrest_rebellion": 9,
        "demographic_pressure": 1,
        "migration_pressure": 0,
        "ethnic_sectarian_fragmentation": 0,
        "urban_decline": 0,
        "fiscal_crisis": 9,
        "taxation_extraction_pressure": 9,
        "trade_disruption": 0,
        "inflation_currency_instability": 9,
        "resource_dependency": 2,
        "agricultural_decline": 0,
        "drought_climate_stress": 9,
        "flood_environmental_shock": 9,
        "temperature_anomaly": 9,
        "ecological_degradation": 1,
        "food_insecurity": 0,
        "external_invasion_pressure": 0,
        "civil_war_internal_conflict": 9,
        "military_overstretch": 0,
        "territorial_loss": 0,
        "institutional_rigidity": 1,
        "adaptive_capacity": 3,
        "logistics_food_storage_resilience": 2,
        "alliance_network_strength": 9,
        "recovery_capacity": 3,
    },
}


def build_scores(*template_names: str, **overrides: int) -> dict[str, int]:
    values = unknown_scores()
    for template_name in template_names:
        values.update(TEMPLATES[template_name])
    values.update(overrides)
    return values


def segment(
    start: int,
    end: int,
    phase_label: str,
    collapse_outcome: int,
    data_confidence: str,
    note: str,
    *template_names: str,
    **overrides: int,
) -> dict[str, object]:
    return {
        "start": start,
        "end": end,
        "phase_label": phase_label,
        "collapse_outcome": collapse_outcome,
        "data_confidence": data_confidence,
        "note": note,
        "template_names": template_names,
        "overrides": overrides,
    }


CASE_SEGMENTS: dict[str, list[dict[str, object]]] = {}
CASE_SEGMENTS.update(
    {
        "Western Roman Empire": [
            segment(-100, 150, "stable", 0, "medium", "Imperial order is broadly stable, with low acute crisis indicators and strong resilience.", "stable_empire", social_inequality=2, resource_dependency=1),
            segment(150, 225, "stressed", 1, "medium", "Frontier strain and administrative-fiscal pressure rise, but the western imperial system remains intact.", "stressed_empire", social_inequality=2, resource_dependency=1, inflation_currency_instability=1, drought_climate_stress=1),
            segment(225, 250, "decline", 2, "medium", "The third-century crisis intensifies elite conflict, military strain, and fiscal instability before later recovery.", "decline_empire", elite_conflict=3, succession_crisis=3, legitimacy_crisis=2, administrative_overload=3, fiscal_crisis=2, inflation_currency_instability=3, external_invasion_pressure=3, civil_war_internal_conflict=3, military_overstretch=3, territorial_loss=2, recovery_capacity=3),
            segment(250, 275, "collapse", 3, "medium", "The third-century crisis reaches collapse-level fragmentation and conflict, though recovery capacity remains substantial.", "collapse_empire", legitimacy_crisis=2, social_unrest_rebellion=1, inflation_currency_instability=3, civil_war_internal_conflict=3, adaptive_capacity=2, logistics_food_storage_resilience=2, recovery_capacity=3),
            segment(275, 350, "post-collapse", 2, "medium", "Reform and reconsolidation restore order, but the imperial system remains heavily militarized and burdensome.", "postcollapse_empire", political_fragmentation=1, legitimacy_crisis=1, administrative_overload=2, taxation_extraction_pressure=2, trade_disruption=1, external_invasion_pressure=2, military_overstretch=2, territorial_loss=1, institutional_rigidity=2, adaptive_capacity=2, logistics_food_storage_resilience=2, alliance_network_strength=2, recovery_capacity=3),
            segment(350, 425, "decline", 2, "medium", "Late imperial cohesion weakens under migration pressure, military burden, and growing fiscal strain.", "decline_empire", social_inequality=2, migration_pressure=2, fiscal_crisis=2, taxation_extraction_pressure=2, external_invasion_pressure=2, military_overstretch=3, territorial_loss=1, institutional_rigidity=2, adaptive_capacity=2, logistics_food_storage_resilience=2, alliance_network_strength=1, recovery_capacity=2),
            segment(425, 450, "decline", 2, "medium", "The western empire survives but suffers deep territorial, fiscal, and alliance erosion.", "decline_empire", political_fragmentation=2, elite_conflict=2, urban_decline=2, fiscal_crisis=3, trade_disruption=2, resource_dependency=3, food_insecurity=2, external_invasion_pressure=3, military_overstretch=3, territorial_loss=2, institutional_rigidity=3, adaptive_capacity=1, logistics_food_storage_resilience=1, alliance_network_strength=1, recovery_capacity=1),
            segment(450, 475, "collapse", 3, "medium", "Terminal western collapse follows repeated elite conflict, territorial loss, invasion pressure, and fiscal breakdown.", "collapse_empire", administrative_overload=2, corruption_governance_failure=3, urban_decline=3, trade_disruption=3, resource_dependency=3, agricultural_decline=2, food_insecurity=2, civil_war_internal_conflict=2, institutional_rigidity=3),
            segment(475, 500, "post-collapse", 3, "medium", "Post-476 successor polities persist, but western Roman imperial capacity is gone.", "postcollapse_empire", urban_decline=3),
        ],
        "Bronze Age Collapse States": [
            segment(-1300, -1250, "stable", 0, "low", "A highly interconnected palace world persists, but its complexity already depends on vulnerable exchange and administrative systems.", "stable_regional", administrative_overload=2, trade_disruption=2, institutional_rigidity=2),
            segment(-1250, -1225, "stressed", 1, "low", "Trade fragility, pressure on palace systems, and early military stress become more visible across the region.", "stressed_regional", migration_pressure=1, drought_climate_stress=1),
            segment(-1225, -1200, "decline", 2, "low", "Interconnected palace states face escalating trade breakdown, invasion pressure, migration, and food stress.", "decline_regional", migration_pressure=2, trade_disruption=3, external_invasion_pressure=2, military_overstretch=3),
            segment(-1200, -1175, "collapse", 3, "low", "The regional crisis peaks as urban systems fail and multiple palace-centered states fragment or disappear.", "collapse_regional", migration_pressure=3, external_invasion_pressure=3, trade_disruption=3, urban_decline=3),
            segment(-1175, -1125, "post-collapse", 3, "low", "Post-collapse fragmentation remains severe even as some regions stabilize under new, smaller political formations.", "postcollapse_regional", political_fragmentation=3, urban_decline=2, trade_disruption=2, territorial_loss=2),
            segment(-1125, -1100, "post-collapse", 2, "low", "The collapse horizon has passed, but regional recovery remains uneven and the old palace order has not returned.", "postcollapse_regional", political_fragmentation=2, urban_decline=2, trade_disruption=1, territorial_loss=2, recovery_capacity=2),
        ],
        "Maya": [
            segment(600, 700, "stable", 0, "medium", "Classic Maya polities remain viable, though hierarchy and rivalry already create background fragility.", "stable_regional", social_inequality=2, demographic_pressure=1, military_overstretch=1, recovery_capacity=3),
            segment(700, 775, "stressed", 1, "medium", "Competition among city-states and rising population and drought sensitivity increase systemic stress.", "stressed_regional", social_inequality=2, demographic_pressure=2, military_overstretch=2, drought_climate_stress=1),
            segment(775, 850, "decline", 2, "medium", "Political fragmentation, warfare, urban weakening, and drought-related food stress intensify across many southern lowland polities.", "decline_regional", social_inequality=2, demographic_pressure=2, migration_pressure=1, external_invasion_pressure=9, civil_war_internal_conflict=2, military_overstretch=2),
            segment(850, 875, "decline", 2, "medium", "Many southern lowland centers enter acute decline, but the regional collapse is still uneven.", "decline_regional", political_fragmentation=2, legitimacy_crisis=2, migration_pressure=2, external_invasion_pressure=9, civil_war_internal_conflict=2, drought_climate_stress=2),
            segment(875, 900, "collapse", 3, "medium", "Terminal abandonment and fragmentation spread across core southern lowland centers as drought, warfare, and dynastic failure combine.", "collapse_regional", legitimacy_crisis=3, migration_pressure=2, external_invasion_pressure=9, civil_war_internal_conflict=2, drought_climate_stress=3),
            segment(900, 925, "post-collapse", 2, "medium", "The southern collapse persists, though Maya society continues in more regionally uneven and resilient forms elsewhere.", "postcollapse_regional", political_fragmentation=2, urban_decline=2, territorial_loss=1, recovery_capacity=2),
            segment(925, 950, "post-collapse", 1, "medium", "Post-collapse conditions remain visible in the southern lowlands, but the wider Maya world is not uniformly extinguished.", "postcollapse_regional", political_fragmentation=1, urban_decline=1, territorial_loss=1, recovery_capacity=2),
        ],
        "Akkadian Empire": [
            segment(-2350, -2300, "stable", 0, "low", "The empire is expanding and still resilient, though its reach already depends on military coercion and broad resource control.", "stable_empire", administrative_overload=1, resource_dependency=2, military_overstretch=2),
            segment(-2300, -2250, "stressed", 1, "low", "Imperial overextension, elite conflict, and dependence on northern zones and exchange networks create growing strain.", "stressed_empire", elite_conflict=2, civil_war_internal_conflict=2, military_overstretch=3, resource_dependency=3),
            segment(-2250, -2225, "decline", 2, "low", "Late-apogee strain raises conflict, overextension, and early agrarian-climate stress without full imperial breakdown yet.", "decline_empire", succession_crisis=1, resource_dependency=3, drought_climate_stress=1, external_invasion_pressure=1, civil_war_internal_conflict=2, military_overstretch=3, recovery_capacity=2),
            segment(-2225, -2200, "decline", 2, "low", "Northern contraction, agrarian stress, and exchange disruption deepen as the empire loses coherence.", "decline_empire", urban_decline=2, trade_disruption=2, resource_dependency=3, agricultural_decline=2, drought_climate_stress=2, ecological_degradation=1, food_insecurity=2, external_invasion_pressure=2, military_overstretch=3),
            segment(-2200, -2175, "collapse", 3, "low", "Political fragmentation, succession crisis, external pressure, and climate-linked agrarian stress combine in terminal imperial collapse.", "collapse_empire", elite_conflict=2, legitimacy_crisis=2, trade_disruption=2, drought_climate_stress=2, ecological_degradation=1, food_insecurity=2, external_invasion_pressure=3, civil_war_internal_conflict=2, institutional_rigidity=2),
            segment(-2175, -2150, "post-collapse", 3, "low", "The Akkadian imperial system is gone, though regional continuity persists beyond the empire itself.", "postcollapse_empire"),
        ],
        "Khmer Empire": [
            segment(1000, 1175, "stable", 0, "medium", "Angkor remains a powerful hydraulic empire with strong logistical and adaptive capacity.", "stable_empire", administrative_overload=1, resource_dependency=2, military_overstretch=1),
            segment(1175, 1250, "stressed", 1, "medium", "Peak complexity after Jayavarman VII increases administrative burden and long-term infrastructural vulnerability.", "stressed_empire", taxation_extraction_pressure=2, resource_dependency=2, military_overstretch=2),
            segment(1250, 1325, "decline", 2, "medium", "Institutional and urban weakening becomes more visible as central mobilization and hydraulic maintenance lose coherence.", "decline_empire", political_fragmentation=2, urban_decline=2, drought_climate_stress=1, external_invasion_pressure=1, territorial_loss=1),
            segment(1325, 1400, "decline", 2, "medium", "Late Angkor faces deeper water-management stress, climate volatility, and declining adaptive capacity.", "decline_empire", political_fragmentation=2, drought_climate_stress=2, flood_environmental_shock=2, ecological_degradation=1, external_invasion_pressure=2),
            segment(1400, 1425, "collapse", 3, "medium", "Severe drought-flood oscillation, hydraulic fragility, urban decline, and Ayutthayan pressure drive terminal Angkorian collapse.", "collapse_empire", elite_conflict=2, succession_crisis=2, flood_environmental_shock=3, ecological_degradation=2, external_invasion_pressure=3),
            segment(1425, 1450, "post-collapse", 2, "medium", "Political power shifts away from Angkor, leaving a transformed post-collapse landscape rather than instant civilizational disappearance.", "postcollapse_empire", urban_decline=2, territorial_loss=3, trade_disruption=1, recovery_capacity=2),
        ],
        "Han Dynasty Crisis": [
            segment(150, 170, "stressed", 1, "medium", "Late Han court factionalism, land concentration, and frontier burdens weaken but do not yet break the regime.", "stressed_empire", social_inequality=2, fiscal_crisis=2, taxation_extraction_pressure=2, external_invasion_pressure=2),
            segment(170, 180, "decline", 2, "medium", "Court fragility deepens as environmental stress and fiscal weakness accumulate before the terminal crisis.", "decline_empire", drought_climate_stress=1, flood_environmental_shock=1, agricultural_decline=1, food_insecurity=1, external_invasion_pressure=2),
            segment(180, 190, "decline", 2, "medium", "The Yellow Turban revolt and the 189 court crisis push the late Han into acute but not yet final breakdown.", "decline_empire", elite_conflict=3, succession_crisis=3, legitimacy_crisis=3, administrative_overload=3, corruption_governance_failure=3, social_unrest_rebellion=3, fiscal_crisis=3, military_overstretch=3, institutional_rigidity=3, adaptive_capacity=1, recovery_capacity=1),
            segment(190, 200, "collapse", 3, "medium", "Civil war, warlordism, and Luoyang's destruction mark the collapse of effective central Han authority.", "collapse_empire", migration_pressure=2, food_insecurity=2, civil_war_internal_conflict=3),
            segment(200, 210, "post-collapse", 3, "medium", "Central authority remains shattered as regional military regimes dominate the former empire.", "postcollapse_empire", political_fragmentation=3, territorial_loss=3, civil_war_internal_conflict=3),
            segment(210, 220, "post-collapse", 3, "medium", "The Han end state is one of durable fragmentation and low recovery capacity before formal dynastic termination.", "postcollapse_empire", political_fragmentation=3, territorial_loss=3, civil_war_internal_conflict=2),
        ],
    }
)
def get_segment(case_name: str, period_start: int, period_end: int) -> dict[str, object]:
    for case_segment in CASE_SEGMENTS[case_name]:
        if int(case_segment["start"]) <= period_start and period_end <= int(case_segment["end"]):
            return case_segment
    raise ValueError(f"No segment found for {case_name} {period_start}-{period_end}")


def load_case_source_totals() -> dict[str, int]:
    inventory_path = REFERENCES_SOURCES_DIR / "source_inventory.csv"
    if not inventory_path.exists():
        return {}

    inventory_df = pd.read_csv(inventory_path)
    if inventory_df.empty:
        return {}

    return inventory_df.groupby("case_name").size().to_dict()


def derive_source_count(case_name: str, phase_label: str, data_confidence: str, case_source_totals: dict[str, int]) -> int:
    case_total = int(case_source_totals.get(case_name, 0))
    phase_cap = PHASE_SOURCE_CAP[phase_label]
    adjusted = phase_cap + CONFIDENCE_ADJUSTMENT[data_confidence]
    if case_total:
        return max(2, min(case_total, adjusted))
    return max(2, adjusted)


def build_backup_path(dataset_path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return dataset_path.with_name(f"{dataset_path.stem}_backup_{timestamp}{dataset_path.suffix}")


def apply_first_pass_codes(dataset_path: Path) -> tuple[Path, pd.DataFrame]:
    df = pd.read_csv(dataset_path)
    backup_path = build_backup_path(dataset_path)
    df.to_csv(backup_path, index=False)

    case_source_totals = load_case_source_totals()
    filled_rows: list[dict[str, object]] = []

    for _, row in df.iterrows():
        case_name = str(row["case_name"])
        period_start = int(row["period_start"])
        period_end = int(row["period_end"])
        matched_segment = get_segment(case_name, period_start, period_end)
        scores = build_scores(*matched_segment["template_names"], **matched_segment["overrides"])

        updated_row = row.to_dict()
        for factor_name, factor_value in scores.items():
            updated_row[factor_name] = int(factor_value)

        phase_label = str(matched_segment["phase_label"])
        data_confidence = str(matched_segment["data_confidence"])
        updated_row["phase_label"] = phase_label
        updated_row["collapse_outcome"] = int(matched_segment["collapse_outcome"])
        updated_row["data_confidence"] = data_confidence
        updated_row["source_count"] = derive_source_count(case_name, phase_label, data_confidence, case_source_totals)
        updated_row["notes"] = str(matched_segment["note"])
        filled_rows.append(updated_row)

    filled_df = pd.DataFrame(filled_rows, columns=df.columns)
    filled_df = filled_df.sort_values(["case_name", "period_start", "period_end"]).reset_index(drop=True)
    filled_df["collapse_within_next_window"] = 0

    for case_name, group in filled_df.groupby("case_name", sort=False):
        ordered_indexes = group.sort_values(["period_start", "period_end"]).index.tolist()
        for offset, current_index in enumerate(ordered_indexes):
            next_outcome = None
            if offset + 1 < len(ordered_indexes):
                next_outcome = int(filled_df.loc[ordered_indexes[offset + 1], "collapse_outcome"])
            current_outcome = int(filled_df.loc[current_index, "collapse_outcome"])
            filled_df.loc[current_index, "collapse_within_next_window"] = int(next_outcome == 3 and current_outcome < 3)

    for factor_name in FACTOR_COLUMNS:
        filled_df[factor_name] = filled_df[factor_name].astype(int)

    filled_df["collapse_outcome"] = filled_df["collapse_outcome"].astype(int)
    filled_df["collapse_within_next_window"] = filled_df["collapse_within_next_window"].astype(int)
    filled_df["source_count"] = filled_df["source_count"].astype(int)

    invalid_values = validate_factor_values(filled_df)
    if not invalid_values.empty:
        raise ValueError(f"Invalid factor values detected after coding: {invalid_values.head()}")

    if filled_df[FACTOR_COLUMNS].isna().any().any():
        raise ValueError("Blank factor cells remain after coding.")

    if not set(pd.unique(filled_df["phase_label"])).issubset(set(PHASE_SOURCE_CAP)):
        raise ValueError("Unexpected phase labels were written.")

    if not set(pd.unique(filled_df["data_confidence"])).issubset(set(CONFIDENCE_ADJUSTMENT)):
        raise ValueError("Unexpected data_confidence values were written.")

    filled_df.to_csv(dataset_path, index=False)
    return backup_path, filled_df


def write_audit(df: pd.DataFrame) -> Path:
    audit_path = PROCESSED_DATA_DIR / "auto_coding_audit.csv"
    audit_df = df[["case_id", "case_name", "period_start", "period_end"]].copy()
    audit_df["factors_filled_count"] = df[FACTOR_COLUMNS].notna().sum(axis=1).astype(int)
    audit_df["unknown_9_count"] = (df[FACTOR_COLUMNS] == 9).sum(axis=1).astype(int)
    audit_df["phase_label"] = df["phase_label"]
    audit_df["collapse_outcome"] = df["collapse_outcome"].astype(int)
    audit_df["collapse_within_next_window"] = df["collapse_within_next_window"].astype(int)
    audit_df["data_confidence"] = df["data_confidence"]
    audit_df["notes"] = df["notes"]
    audit_df.to_csv(audit_path, index=False)
    return audit_path


def write_summary(df: pd.DataFrame, backup_path: Path) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "auto_coding_summary.md"
    factor_numeric_count = int(df[FACTOR_COLUMNS].isin([0, 1, 2, 3]).sum().sum())
    factor_unknown_count = int((df[FACTOR_COLUMNS] == 9).sum().sum())
    uncertainty_by_case = (
        (df[FACTOR_COLUMNS] == 9)
        .sum(axis=1)
        .groupby(df["case_name"])
        .mean()
        .sort_values(ascending=False)
    )
    debated_cases = {
        "Bronze Age Collapse States": "multi-polity and multi-causal regional case",
        "Easter Island": "transformation case with major debate about pre-contact collapse",
        "Classic Mesopotamian States": "heterogeneous regional comparison with repeated crisis and recovery",
        "Akkadian Empire": "climate, subsistence, and collapse timing remain debated",
        "Maya": "regional and uneven collapse with strong subregional variation",
        "Byzantine Decline": "long decline with partial recoveries and repeated rupture",
    }

    lines = [
        "# Auto Coding Summary",
        "",
        "This file documents the first-pass machine-assisted literature-based coding draft applied to the historical collapse dataset.",
        "",
        f"- Backup created: `{backup_path.name}`",
        f"- Total rows updated: `{len(df)}`",
        f"- Total factor cells filled with `0/1/2/3`: `{factor_numeric_count}`",
        f"- Total factor cells filled with `9`: `{factor_unknown_count}`",
        "",
        "**Cases With Highest Average Uncertainty**",
        "",
    ]
    for case_name, average_unknown in uncertainty_by_case.head(6).items():
        lines.append(f"- `{case_name}`: average `{average_unknown:.1f}` factors scored `9` per row")

    lines.extend(["", "**Especially Debated Or Heterogeneous Cases**", ""])
    for case_name, reason in debated_cases.items():
        lines.append(f"- `{case_name}`: {reason}")

    lines.extend(
        [
            "",
            "**Methodological Note**",
            "",
            "This is a first-pass machine-assisted coding draft built from the case analyses already generated in the project from reputable secondary literature.",
            "It is not final historical ground truth and requires later human review, source checking, and row-level refinement before any substantive interpretation or modeling.",
        ]
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> None:
    backup_path, filled_df = apply_first_pass_codes(COLLAPSE_DATASET_PATH)
    audit_path = write_audit(filled_df)
    report_path = write_summary(filled_df, backup_path)

    print(f"Backup created: {backup_path}")
    print(f"Updated dataset: {COLLAPSE_DATASET_PATH}")
    print(f"Audit written: {audit_path}")
    print(f"Summary written: {report_path}")


CASE_SEGMENTS.update(
    {
        "Byzantine Decline": [
            segment(1000, 1025, "stable", 0, "medium", "The empire remains strong before the post-Basil II decline begins.", "stable_empire"),
            segment(1025, 1075, "stressed", 1, "medium", "Post-Basil II succession problems and elite rivalry weaken the military-fiscal core.", "stressed_empire", succession_crisis=2, fiscal_crisis=1, external_invasion_pressure=2),
            segment(1075, 1175, "decline", 2, "medium", "Anatolian loss and military strain transform the empire even as partial Komnenian recovery moderates the damage.", "decline_empire", political_fragmentation=1, legitimacy_crisis=1, fiscal_crisis=2, external_invasion_pressure=3, military_overstretch=3, territorial_loss=2, adaptive_capacity=2, recovery_capacity=2),
            segment(1175, 1200, "decline", 2, "medium", "Late Komnenian weakening and fiscal strain leave the empire vulnerable before 1204.", "decline_empire", trade_disruption=2, legitimacy_crisis=2, adaptive_capacity=1),
            segment(1200, 1225, "collapse", 3, "medium", "The Fourth Crusade produces imperial fragmentation, territorial loss, and a true collapse of the Byzantine center.", "collapse_empire", external_invasion_pressure=3, civil_war_internal_conflict=2, trade_disruption=3),
            segment(1225, 1275, "post-collapse", 2, "medium", "Nicaean recovery and restoration revive imperial institutions, but the empire remains weaker and more fragmented than before.", "postcollapse_empire", political_fragmentation=2, adaptive_capacity=2, recovery_capacity=2),
            segment(1275, 1325, "decline", 2, "medium", "Commercial dependence, fiscal weakness, and renewed external pressure deepen the long post-1204 decline.", "decline_empire", resource_dependency=2, trade_disruption=2, external_invasion_pressure=2),
            segment(1325, 1400, "decline", 2, "medium", "Civil wars and foreign encroachment intensify late Byzantine fiscal and territorial erosion.", "decline_empire", elite_conflict=3, social_unrest_rebellion=2, migration_pressure=2, urban_decline=2, inflation_currency_instability=2, civil_war_internal_conflict=3, territorial_loss=3, institutional_rigidity=3),
            segment(1400, 1450, "decline", 2, "medium", "The empire survives as a much smaller polity with weak alliances and very limited recovery capacity.", "decline_empire", external_invasion_pressure=3, territorial_loss=3, military_overstretch=2, alliance_network_strength=1, recovery_capacity=1),
            segment(1450, 1453, "collapse", 3, "medium", "Final Ottoman conquest ends the Byzantine state after centuries of cumulative decline.", "collapse_empire", external_invasion_pressure=3, urban_decline=3, territorial_loss=3),
        ],
        "Sassanian Empire": [
            segment(500, 575, "stable", 0, "medium", "The empire remains coherent, though later fragility is already visible in crown-nobility relations.", "stable_empire"),
            segment(575, 600, "stressed", 1, "medium", "Elite rivalry and military rebellion reveal growing weakness in royal control before the final crisis.", "stressed_empire", elite_conflict=2, succession_crisis=2, legitimacy_crisis=2, civil_war_internal_conflict=2),
            segment(600, 625, "decline", 2, "medium", "The long war with Byzantium overextends the empire and weakens its fiscal and alliance systems.", "decline_empire", trade_disruption=2, resource_dependency=2, external_invasion_pressure=3, military_overstretch=3),
            segment(625, 650, "collapse", 3, "medium", "War exhaustion, plague, succession chaos, civil war, and Arab conquest combine in terminal collapse.", "collapse_empire", trade_disruption=2, agricultural_decline=2, food_insecurity=2, civil_war_internal_conflict=3, institutional_rigidity=2),
            segment(650, 651, "post-collapse", 3, "medium", "The imperial framework has disintegrated and no meaningful recovery capacity remains.", "postcollapse_empire"),
        ],
        "Easter Island": [
            segment(1200, 1300, "stable", 0, "low", "Early settlement and adaptation do not yet support a clear pre-contact collapse narrative.", "transformation_island"),
            segment(1300, 1450, "stressed", 1, "low", "Resource constraints and ecological change increase, but evidence for island-wide collapse remains weak.", "transformation_island", ecological_degradation=2, resource_dependency=2, adaptive_capacity=3, recovery_capacity=3),
            segment(1450, 1550, "decline", 1, "low", "Regional land-use contraction and ecological change are visible, but warfare and demographic-collapse claims remain debated.", "transformation_island", resource_dependency=3, ecological_degradation=3, agricultural_decline=1, food_insecurity=1, adaptive_capacity=3, recovery_capacity=2),
            segment(1550, 1700, "decline", 2, "low", "Late pre-contact drought and freshwater stress likely intensified an already transformed island system without securely proving total collapse.", "transformation_island", migration_pressure=1, resource_dependency=3, agricultural_decline=2, drought_climate_stress=2, ecological_degradation=2, food_insecurity=2, adaptive_capacity=2, logistics_food_storage_resilience=2, recovery_capacity=2),
        ],
        "Classic Mesopotamian States": [
            segment(-2100, -2050, "stable", 0, "low", "Ur III and related systems maintain order, though they remain resource- and infrastructure-dependent.", "stable_empire", resource_dependency=2, administrative_overload=2),
            segment(-2050, -2025, "stressed", 1, "low", "Fiscal and agrarian strain rise before the final Ur III breakdown.", "stressed_empire", resource_dependency=2, food_insecurity=1),
            segment(-2025, -2000, "collapse", 3, "low", "The end of Ur III combines fragmentation, famine risk, external attack, and territorial loss.", "collapse_empire", drought_climate_stress=2, food_insecurity=2, external_invasion_pressure=2),
            segment(-2000, -1950, "post-collapse", 2, "low", "Post-Ur III fragmentation persists, but institutional continuity and regional recovery remain real.", "postcollapse_regional", political_fragmentation=3, trade_disruption=1, adaptive_capacity=2, recovery_capacity=2),
            segment(-1950, -1850, "stressed", 1, "low", "The Isin-Larsa world is politically fragmented yet still economically interactive and regionally resilient.", "stressed_regional", political_fragmentation=3, elite_conflict=2, trade_disruption=1, adaptive_capacity=2, recovery_capacity=2),
            segment(-1850, -1775, "stressed", 1, "low", "Fragmented but adaptive interstate competition persists before Hammurabi's reconsolidation.", "stressed_regional", political_fragmentation=2, elite_conflict=2, adaptive_capacity=2, recovery_capacity=2),
            segment(-1775, -1750, "stable", 1, "low", "Hammurabi's reconsolidation temporarily lowers fragmentation without eliminating longer-term structural vulnerability.", "stable_empire", political_fragmentation=1, elite_conflict=2, administrative_overload=2, military_overstretch=2),
            segment(-1750, -1700, "decline", 2, "low", "Post-Hammurabi contraction brings renewed internal conflict, urban weakening, and territorial loss.", "decline_empire", civil_war_internal_conflict=2, urban_decline=1),
            segment(-1700, -1600, "decline", 2, "low", "Late Old Babylonian weakness grows, but the final sack falls just beyond the dataset's last window.", "decline_empire", external_invasion_pressure=2, territorial_loss=2, recovery_capacity=1),
        ],
        "Ming/Qing Transition": [
            segment(1550, 1600, "stressed", 1, "medium", "Court paralysis, succession conflict, and fiscal strain are visible, but the Ming state is still intact.", "stressed_empire", social_inequality=2, military_overstretch=2, resource_dependency=2, temperature_anomaly=1),
            segment(1600, 1625, "decline", 2, "medium", "Factionalism, military pressure in the northeast, and fiscal weakness move the late Ming into clear decline.", "decline_empire", elite_conflict=3, external_invasion_pressure=3, military_overstretch=3, resource_dependency=2),
            segment(1625, 1650, "collapse", 3, "medium", "Drought-famine crisis, rebellion, fiscal breakdown, and Manchu conquest drive terminal Ming collapse.", "collapse_empire", demographic_pressure=2, agricultural_decline=3, drought_climate_stress=3, flood_environmental_shock=1, temperature_anomaly=1, food_insecurity=3, civil_war_internal_conflict=3),
            segment(1650, 1675, "post-collapse", 2, "medium", "The Qing transition remains violent and unsettled, but the Ming collapse phase has passed.", "postcollapse_empire", political_fragmentation=2, external_invasion_pressure=2, recovery_capacity=2),
            segment(1675, 1700, "post-collapse", 1, "medium", "The dynastic transition stabilizes under Qing rule even though the old Ming order is gone.", "postcollapse_empire", political_fragmentation=1, territorial_loss=1, adaptive_capacity=2, alliance_network_strength=2, recovery_capacity=2),
        ],
        "Aztec Empire": [
            segment(1400, 1450, "stable", 0, "medium", "The imperial core consolidates with low acute collapse indicators and strong logistical capacity.", "stable_empire", social_inequality=1, alliance_network_strength=1),
            segment(1450, 1500, "stressed", 1, "medium", "A coercive tributary empire expands, but subject resentment and weak alliance loyalty create latent fragility.", "stressed_empire", social_inequality=2, resource_dependency=2, alliance_network_strength=1),
            segment(1500, 1525, "collapse", 3, "medium", "Spanish-indigenous coalition warfare, epidemic shock, and subject-polity defection collapse the empire rapidly.", "collapse_empire", elite_conflict=2, social_unrest_rebellion=3, food_insecurity=3, civil_war_internal_conflict=1),
        ],
        "Inca Empire": [
            segment(1400, 1500, "stable", 0, "medium", "A highly centralized imperial system retains strong roads, stores, and ruler-centered authority.", "stable_empire", social_unrest_rebellion=1, taxation_extraction_pressure=1),
            segment(1500, 1525, "stressed", 1, "medium", "Late-imperial succession stress and epidemic disruption begin to weaken an otherwise powerful empire.", "stressed_empire", external_invasion_pressure=1, civil_war_internal_conflict=1, food_insecurity=1),
            segment(1525, 1550, "collapse", 3, "medium", "Civil war, epidemic disruption, and Spanish conquest combine in terminal imperial collapse.", "collapse_empire", social_unrest_rebellion=2, food_insecurity=2, external_invasion_pressure=3, civil_war_internal_conflict=3, military_overstretch=2),
            segment(1550, 1575, "post-collapse", 2, "medium", "Post-conquest resistance persists, but imperial territorial control and recovery capacity are broken.", "postcollapse_empire", external_invasion_pressure=2, territorial_loss=3),
        ],
        "Soviet Union": [
            segment(1950, 1960, "stable", 0, "medium", "The postwar Soviet system is still resilient despite centralization and long-term institutional rigidity.", "stable_modern", corruption_governance_failure=1, military_overstretch=2, resource_dependency=1, adaptive_capacity=2),
            segment(1960, 1970, "stressed", 1, "medium", "Institutional rigidity grows as reform limits become clearer, but fragmentation remains low.", "stressed_modern", ethnic_sectarian_fragmentation=1, military_overstretch=2, institutional_rigidity=2),
            segment(1970, 1980, "stressed", 1, "high", "Stagnation, corruption, and institutional rigidity deepen while overt fragmentation remains limited.", "stressed_modern", elite_conflict=1, legitimacy_crisis=1, corruption_governance_failure=2, resource_dependency=2, military_overstretch=2, institutional_rigidity=3),
            segment(1980, 1990, "decline", 2, "high", "Failed reform, shortages, strikes, and nationalist mobilization push the late USSR into clear decline.", "decline_modern", social_unrest_rebellion=2, food_insecurity=2, military_overstretch=2),
            segment(1990, 1991, "collapse", 3, "high", "Republican sovereignty, elite rupture, and terminal legitimacy crisis break the Union apart in 1991.", "collapse_modern", external_invasion_pressure=0, civil_war_internal_conflict=2, military_overstretch=1, food_insecurity=2),
        ],
        "Yugoslavia": [
            segment(1945, 1965, "stable", 0, "medium", "Federal Yugoslavia remains intact, with limited overt fragmentation under Tito's authority.", "stable_modern", military_overstretch=1),
            segment(1965, 1975, "stressed", 1, "medium", "Decentralization and uneven development increase structural strain without yet breaking the federation.", "stressed_modern", ethnic_sectarian_fragmentation=1),
            segment(1975, 1985, "stressed", 1, "high", "The 1974 constitution, Tito's death, and worsening debt and inflation deepen institutional fragility.", "stressed_modern", political_fragmentation=2, legitimacy_crisis=2, fiscal_crisis=2, inflation_currency_instability=2, recovery_capacity=1),
            segment(1985, 1995, "collapse", 3, "high", "Elite nationalist mobilization, economic crisis, and the breakdown of federal coercive institutions drive violent fragmentation.", "collapse_modern", external_invasion_pressure=0, migration_pressure=3, urban_decline=2, inflation_currency_instability=3, food_insecurity=1),
            segment(1995, 2000, "post-collapse", 2, "high", "Post-fragmentation successor states persist amid weak recovery and residual territorial and ethnic conflict.", "postcollapse_modern", ethnic_sectarian_fragmentation=3, migration_pressure=2, urban_decline=2),
        ],
    }
)
