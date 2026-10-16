#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

Recommendation = Literal[
    "BID",
    "BID_WITH_PARTNER",
    "SUB_ONLY",
    "MONITOR_AND_SHAPE",
    "NO_BID",
]

SCORING_FACTORS = [
    "customer_fit",
    "capability_fit",
    "past_performance",
    "price_fit",
    "competition",
    "delivery",
    "strategy",
    "readiness",
]


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc)


def days_until(target: datetime | None) -> int | None:
    if target is None:
        return None

    now = datetime.now(timezone.utc)
    return max((target - now).days, 0)


def to_string_list(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    text = str(value).strip()
    return [text] if text else []


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    bounded = {key: max(float(value), 0.0) for key, value in weights.items()}
    total = sum(bounded.values()) or 1.0
    return {key: value / total for key, value in bounded.items()}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def text_similarity(left: str, right: str) -> float:
    left_tokens = tokenize(left)
    right_tokens = tokenize(right)

    if not left_tokens or not right_tokens:
        return 0.0

    left_counter = Counter(left_tokens + [f"{a}_{b}" for a, b in zip(left_tokens, left_tokens[1:])])
    right_counter = Counter(right_tokens + [f"{a}_{b}" for a, b in zip(right_tokens, right_tokens[1:])])

    overlap = set(left_counter) & set(right_counter)
    numerator = sum(left_counter[token] * right_counter[token] for token in overlap)
    left_norm = math.sqrt(sum(value * value for value in left_counter.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counter.values()))

    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0

    return numerator / (left_norm * right_norm)


def overlap_score(required: list[str], available: list[str]) -> float:
    required_set = {item.strip().lower() for item in required if item}
    available_set = {item.strip().lower() for item in available if item}

    if not required_set:
        return 0.7

    if not available_set:
        return 0.0

    return len(required_set & available_set) / len(required_set)


def recency_decay(award_date: datetime | None, half_life_years: float = 3.0) -> float:
    if award_date is None:
        return 0.5

    now = datetime.now(timezone.utc)
    years = max((now - award_date).days / 365.25, 0.0)
    return math.exp(-math.log(2) * years / half_life_years)


def ratio_fit(left: float | None, right: float | None) -> float:
    if left is None or right is None or left <= 0 or right <= 0:
        return 0.5

    return max(0.0, 1.0 - min(abs(math.log(left / right)), 1.5) / 1.5)


def mean(values: list[float]) -> float:
    if not values:
        return 0.0

    return sum(values) / len(values)


@dataclass
class Award:
    award_id: str
    buyer: str
    office: str
    description: str
    naics: str | None = None
    psc: str | None = None
    contract_type: str | None = None
    value: float | None = None
    award_date: datetime | None = None
    is_prime: bool = True
    set_aside: str | None = None
    vehicle: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Award":
        return cls(
            award_id=str(payload.get("award_id") or payload.get("id") or ""),
            buyer=str(payload.get("buyer") or ""),
            office=str(payload.get("office") or ""),
            description=str(payload.get("description") or ""),
            naics=payload.get("naics"),
            psc=payload.get("psc"),
            contract_type=payload.get("contract_type"),
            value=float(payload["value"]) if payload.get("value") is not None else None,
            award_date=parse_datetime(payload.get("award_date")),
            is_prime=bool(payload.get("is_prime", True)),
            set_aside=payload.get("set_aside"),
            vehicle=payload.get("vehicle"),
        )


@dataclass
class PriceBand:
    low: float | None = None
    median: float | None = None
    high: float | None = None
    comparable_count: int = 0

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> "PriceBand | None":
        if payload is None:
            return None

        return cls(
            low=float(payload["low"]) if payload.get("low") is not None else None,
            median=float(payload["median"]) if payload.get("median") is not None else None,
            high=float(payload["high"]) if payload.get("high") is not None else None,
            comparable_count=int(payload.get("comparable_count", 0) or 0),
        )


@dataclass
class Competitor:
    name: str
    is_incumbent: bool = False
    strength_score: float = 50.0
    likely_role: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Competitor":
        return cls(
            name=str(payload.get("name") or ""),
            is_incumbent=bool(payload.get("is_incumbent", False)),
            strength_score=float(payload.get("strength_score", 50.0) or 50.0),
            likely_role=payload.get("likely_role"),
        )


@dataclass
class Opportunity:
    opportunity_id: str
    buyer: str
    office: str
    description: str
    naics: str | None = None
    psc: str | None = None
    contract_type: str | None = None
    estimated_value: float | None = None
    realistic_order_value: float | None = None
    set_aside: str | None = None
    vehicle_required: str | None = None
    due_date: datetime | None = None
    phase: str = "solicitation"
    required_capabilities: list[str] = field(default_factory=list)
    required_clearances: list[str] = field(default_factory=list)
    required_certifications: list[str] = field(default_factory=list)
    evaluation_weights: dict[str, float] = field(default_factory=dict)
    small_business_participation_material: bool = False
    far_5222246_included: bool = False
    incumbent_vendor: str | None = None
    transition_complexity: float = 50.0
    recruiting_difficulty: float = 50.0
    key_personnel_coverage_score: float = 50.0

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Opportunity":
        return cls(
            opportunity_id=str(payload.get("opportunity_id") or payload.get("id") or ""),
            buyer=str(payload.get("buyer") or ""),
            office=str(payload.get("office") or ""),
            description=str(payload.get("description") or ""),
            naics=payload.get("naics"),
            psc=payload.get("psc"),
            contract_type=payload.get("contract_type"),
            estimated_value=float(payload["estimated_value"]) if payload.get("estimated_value") is not None else None,
            realistic_order_value=float(payload["realistic_order_value"]) if payload.get("realistic_order_value") is not None else None,
            set_aside=payload.get("set_aside"),
            vehicle_required=payload.get("vehicle_required"),
            due_date=parse_datetime(payload.get("due_date")),
            phase=str(payload.get("phase") or "solicitation"),
            required_capabilities=to_string_list(payload.get("required_capabilities")),
            required_clearances=to_string_list(payload.get("required_clearances")),
            required_certifications=to_string_list(payload.get("required_certifications")),
            evaluation_weights={
                str(key): float(value)
                for key, value in (payload.get("evaluation_weights") or {}).items()
            },
            small_business_participation_material=bool(payload.get("small_business_participation_material", False)),
            far_5222246_included=bool(payload.get("far_5222246_included", False)),
            incumbent_vendor=payload.get("incumbent_vendor"),
            transition_complexity=float(payload.get("transition_complexity", 50.0) or 50.0),
            recruiting_difficulty=float(payload.get("recruiting_difficulty", 50.0) or 50.0),
            key_personnel_coverage_score=float(payload.get("key_personnel_coverage_score", 50.0) or 50.0),
        )


@dataclass
class BuyerHistory:
    comparable_awards: list[Award] = field(default_factory=list)
    price_band: PriceBand | None = None
    concentration: float = 0.0
    switching_rate: float = 0.5
    competitors: list[Competitor] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> "BuyerHistory":
        payload = payload or {}
        concentration = float(payload.get("concentration", 0.0) or 0.0)

        if concentration > 1.0:
            concentration = concentration / 100.0

        switching_rate = float(payload.get("switching_rate", 0.5) or 0.5)
        if switching_rate > 1.0:
            switching_rate = switching_rate / 100.0

        return cls(
            comparable_awards=[Award.from_dict(item) for item in payload.get("comparable_awards", [])],
            price_band=PriceBand.from_dict(payload.get("price_band")),
            concentration=clamp(concentration, 0.0, 1.0),
            switching_rate=clamp(switching_rate, 0.0, 1.0),
            competitors=[Competitor.from_dict(item) for item in payload.get("competitors", [])],
        )


@dataclass
class ContractorProfile:
    name: str
    capabilities: list[str] = field(default_factory=list)
    clearances: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    vehicles: list[str] = field(default_factory=list)
    socio_statuses: list[str] = field(default_factory=list)
    awards: list[Award] = field(default_factory=list)
    available_fte: int = 0
    margin_floor: float = 0.12
    bid_cost: float = 50_000.0
    opportunity_cost: float = 0.0
    proposal_assets_score: float = 50.0
    strategic_priority_score: float = 50.0
    expected_margin_at_market_price: float | None = None
    expected_margin_at_low_price: float | None = None
    expected_margin_at_high_price: float | None = None
    differentiators: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ContractorProfile":
        return cls(
            name=str(payload.get("name") or ""),
            capabilities=to_string_list(payload.get("capabilities")),
            clearances=to_string_list(payload.get("clearances")),
            certifications=to_string_list(payload.get("certifications")),
            vehicles=to_string_list(payload.get("vehicles")),
            socio_statuses=to_string_list(payload.get("socio_statuses")),
            awards=[Award.from_dict(item) for item in payload.get("awards", [])],
            available_fte=int(payload.get("available_fte", 0) or 0),
            margin_floor=float(payload.get("margin_floor", 0.12) or 0.12),
            bid_cost=float(payload.get("bid_cost", 50_000.0) or 50_000.0),
            opportunity_cost=float(payload.get("opportunity_cost", 0.0) or 0.0),
            proposal_assets_score=float(payload.get("proposal_assets_score", 50.0) or 50.0),
            strategic_priority_score=float(payload.get("strategic_priority_score", 50.0) or 50.0),
            expected_margin_at_market_price=float(payload["expected_margin_at_market_price"]) if payload.get("expected_margin_at_market_price") is not None else None,
            expected_margin_at_low_price=float(payload["expected_margin_at_low_price"]) if payload.get("expected_margin_at_low_price") is not None else None,
            expected_margin_at_high_price=float(payload["expected_margin_at_high_price"]) if payload.get("expected_margin_at_high_price") is not None else None,
            differentiators=to_string_list(payload.get("differentiators")),
        )


@dataclass
class EngineSettings:
    weights: dict[str, float] = field(
        default_factory=lambda: {
            "customer_fit": 0.15,
            "capability_fit": 0.20,
            "past_performance": 0.15,
            "price_fit": 0.20,
            "competition": 0.10,
            "delivery": 0.10,
            "strategy": 0.05,
            "readiness": 0.05,
        }
    )
    pwin_floor_bid: float = 0.55
    pwin_floor_partner: float = 0.40
    readiness_floor_bid: float = 60.0
    sub_only_share_estimate: float = 0.30
    monitor_shaping_cost: float = 10_000.0
    strategic_floor_monitor: float = 70.0

    @classmethod
    def from_dict(cls, payload: dict[str, Any] | None) -> "EngineSettings":
        payload = payload or {}
        defaults = cls()
        merged_weights = dict(defaults.weights)
        merged_weights.update(
            {
                str(key): float(value)
                for key, value in (payload.get("weights") or {}).items()
            }
        )
        return cls(
            weights=normalize_weights(merged_weights),
            pwin_floor_bid=float(payload.get("pwin_floor_bid", defaults.pwin_floor_bid) or defaults.pwin_floor_bid),
            pwin_floor_partner=float(payload.get("pwin_floor_partner", defaults.pwin_floor_partner) or defaults.pwin_floor_partner),
            readiness_floor_bid=float(payload.get("readiness_floor_bid", defaults.readiness_floor_bid) or defaults.readiness_floor_bid),
            sub_only_share_estimate=float(payload.get("sub_only_share_estimate", defaults.sub_only_share_estimate) or defaults.sub_only_share_estimate),
            monitor_shaping_cost=float(payload.get("monitor_shaping_cost", defaults.monitor_shaping_cost) or defaults.monitor_shaping_cost),
            strategic_floor_monitor=float(payload.get("strategic_floor_monitor", defaults.strategic_floor_monitor) or defaults.strategic_floor_monitor),
        )


@dataclass
class FactorResult:
    name: str
    score: float
    confidence: float
    rationale: str
    evidence: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "score": round(self.score, 2),
            "confidence": round(self.confidence, 4),
            "rationale": self.rationale,
            "evidence": self.evidence,
            "flags": self.flags,
        }


@dataclass
class ScenarioEvaluation:
    scenario_key: str
    scenario_display_name: str
    recommendation: Recommendation
    weighted_score: float
    pwin: float
    expected_value: float
    confidence: float
    gate_failures: list[str]
    factor_results: list[FactorResult]
    next_actions: list[str]
    teammate_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenarioKey": self.scenario_key,
            "scenarioDisplayName": self.scenario_display_name,
            "teammateName": self.teammate_name,
            "recommendation": self.recommendation,
            "weightedScore": round(self.weighted_score, 2),
            "pwin": round(self.pwin, 4),
            "expectedValue": round(self.expected_value, 2),
            "confidence": round(self.confidence, 4),
            "gateFailures": self.gate_failures,
            "factorResults": [result.to_dict() for result in self.factor_results],
            "nextActions": self.next_actions,
        }


@dataclass
class Decision:
    recommendation: Recommendation
    selected_scenario_key: str
    selected_scenario_display_name: str
    pwin: float
    expected_value: float
    confidence: float
    missing_data_warnings: list[str]
    scenarios: list[ScenarioEvaluation]

    def to_dict(self) -> dict[str, Any]:
        return {
            "recommendation": self.recommendation,
            "selectedScenarioKey": self.selected_scenario_key,
            "selectedScenarioDisplayName": self.selected_scenario_display_name,
            "pwin": round(self.pwin, 4),
            "expectedValue": round(self.expected_value, 2),
            "confidence": round(self.confidence, 4),
            "missingDataWarnings": self.missing_data_warnings,
            "scenarios": [scenario.to_dict() for scenario in self.scenarios],
        }


def merge_profiles(primary: ContractorProfile, teammate: ContractorProfile) -> ContractorProfile:
    return ContractorProfile(
        name=f"{primary.name} + {teammate.name}",
        capabilities=sorted(set(primary.capabilities) | set(teammate.capabilities)),
        clearances=sorted(set(primary.clearances) | set(teammate.clearances)),
        certifications=sorted(set(primary.certifications) | set(teammate.certifications)),
        vehicles=sorted(set(primary.vehicles) | set(teammate.vehicles)),
        socio_statuses=sorted(set(primary.socio_statuses) | set(teammate.socio_statuses)),
        awards=[*primary.awards, *teammate.awards],
        available_fte=primary.available_fte + teammate.available_fte,
        margin_floor=min(
            [value for value in [primary.margin_floor, teammate.margin_floor] if value > 0],
            default=primary.margin_floor,
        ),
        bid_cost=primary.bid_cost + teammate.bid_cost,
        opportunity_cost=primary.opportunity_cost + teammate.opportunity_cost,
        proposal_assets_score=max(primary.proposal_assets_score, teammate.proposal_assets_score),
        strategic_priority_score=max(primary.strategic_priority_score, teammate.strategic_priority_score),
        expected_margin_at_market_price=min(
            [value for value in [primary.expected_margin_at_market_price, teammate.expected_margin_at_market_price] if value is not None],
            default=primary.expected_margin_at_market_price,
        ),
        expected_margin_at_low_price=min(
            [value for value in [primary.expected_margin_at_low_price, teammate.expected_margin_at_low_price] if value is not None],
            default=primary.expected_margin_at_low_price,
        ),
        expected_margin_at_high_price=min(
            [value for value in [primary.expected_margin_at_high_price, teammate.expected_margin_at_high_price] if value is not None],
            default=primary.expected_margin_at_high_price,
        ),
        differentiators=sorted(set(primary.differentiators) | set(teammate.differentiators)),
    )


class BidNoBidEngine:
    def __init__(
        self,
        opportunity: Opportunity,
        buyer_history: BuyerHistory,
        contractor_profile: ContractorProfile,
        teammates: list[ContractorProfile],
        settings: EngineSettings,
    ) -> None:
        self.opportunity = opportunity
        self.buyer_history = buyer_history
        self.contractor_profile = contractor_profile
        self.teammates = teammates
        self.settings = settings

    def build_missing_data_warnings(self) -> list[str]:
        warnings: list[str] = []

        if not self.opportunity.description:
            warnings.append("Opportunity description is missing.")
        if not self.opportunity.due_date:
            warnings.append("Opportunity due date is missing.")
        if self.opportunity.estimated_value is None and self.opportunity.realistic_order_value is None:
            warnings.append("Opportunity value is missing.")
        if not self.buyer_history.price_band or self.buyer_history.price_band.median is None:
            warnings.append("Comparable-award price band is missing or incomplete.")
        if not self.contractor_profile.awards:
            warnings.append("Contractor award history is missing.")
        if not self.buyer_history.competitors:
            warnings.append("Competitive-field input is missing.")
        if self.contractor_profile.expected_margin_at_market_price is None:
            warnings.append("Expected margin at the likely winning price is missing.")

        return warnings

    def resolve_weights(self) -> dict[str, float]:
        merged = dict(self.settings.weights)
        merged.update(self.opportunity.evaluation_weights)
        return normalize_weights(merged)

    def expected_contract_value(self, mode: str) -> float:
        baseline = (
            self.opportunity.realistic_order_value
            or (self.buyer_history.price_band.median if self.buyer_history.price_band else None)
            or self.opportunity.estimated_value
            or 0.0
        )

        if mode == "sub_only":
            return baseline * self.settings.sub_only_share_estimate

        return baseline

    def expected_margin(self, profile: ContractorProfile, mode: str) -> float | None:
        if mode == "sub_only":
            return profile.expected_margin_at_high_price or profile.expected_margin_at_market_price

        return profile.expected_margin_at_market_price

    def run_gates(self, profile: ContractorProfile, mode: str) -> list[str]:
        failures: list[str] = []

        prime_mode = mode in {"prime_solo", "prime_with_teammate"}

        if prime_mode and self.opportunity.set_aside:
            statuses = {status.lower() for status in profile.socio_statuses}
            if self.opportunity.set_aside.lower() not in statuses:
                failures.append(f"Set-aside mismatch: {self.opportunity.set_aside}")

        if prime_mode and self.opportunity.vehicle_required:
            vehicles = {vehicle.lower() for vehicle in profile.vehicles}
            if self.opportunity.vehicle_required.lower() not in vehicles:
                failures.append(f"Missing vehicle access: {self.opportunity.vehicle_required}")

        if not set(map(str.lower, self.opportunity.required_clearances)).issubset(
            set(map(str.lower, profile.clearances))
        ):
            failures.append("Missing required clearance coverage")

        if not set(map(str.lower, self.opportunity.required_certifications)).issubset(
            set(map(str.lower, profile.certifications))
        ):
            failures.append("Missing required certification coverage")

        if mode != "monitor_and_shape" and profile.available_fte <= 0:
            failures.append("No available delivery capacity")

        if mode != "monitor_and_shape" and not profile.awards:
            failures.append("No credible past performance path")

        if mode != "monitor_and_shape":
            expected_margin = self.expected_margin(profile, mode)
            if expected_margin is not None and expected_margin < max(profile.margin_floor * 0.75, profile.margin_floor - 0.05):
                failures.append("Cannot price competitively without breaking margin floor")

        days_left = days_until(self.opportunity.due_date)
        if mode != "monitor_and_shape" and days_left is not None and days_left <= 7 and profile.proposal_assets_score < 40:
            failures.append("Insufficient proposal readiness for the remaining timeline")

        return failures

    def score_customer_fit(self, profile: ContractorProfile, mode: str) -> FactorResult:
        same_office = sum(
            1
            for award in profile.awards
            if award.buyer.lower() == self.opportunity.buyer.lower()
            and award.office.lower() == self.opportunity.office.lower()
        )
        same_buyer = sum(
            1
            for award in profile.awards
            if award.buyer.lower() == self.opportunity.buyer.lower()
        )
        contract_type_hits = sum(
            1
            for award in profile.awards
            if award.contract_type
            and self.opportunity.contract_type
            and award.contract_type.lower() == self.opportunity.contract_type.lower()
        )
        vehicle_fit = (
            1.0
            if not self.opportunity.vehicle_required
            or self.opportunity.vehicle_required.lower() in {vehicle.lower() for vehicle in profile.vehicles}
            or mode == "sub_only"
            else 0.0
        )
        set_aside_fit = (
            1.0
            if not self.opportunity.set_aside
            or self.opportunity.set_aside.lower() in {status.lower() for status in profile.socio_statuses}
            or mode == "sub_only"
            else 0.0
        )
        incumbent_bonus = 1.0 if self.opportunity.incumbent_vendor and self.opportunity.incumbent_vendor.lower() == profile.name.lower() else 0.0

        score = 100 * (
            0.35 * min(same_office / 3.0, 1.0)
            + 0.25 * min(same_buyer / 5.0, 1.0)
            + 0.15 * min(contract_type_hits / 3.0, 1.0)
            + 0.15 * vehicle_fit
            + 0.05 * set_aside_fit
            + 0.05 * incumbent_bonus
        )

        return FactorResult(
            name="customer_fit",
            score=clamp(score),
            confidence=0.8 if profile.awards else 0.3,
            rationale=f"{same_office} same-office awards, {same_buyer} same-buyer awards, {contract_type_hits} same-structure wins.",
            evidence=[
                f"same_office_awards={same_office}",
                f"same_buyer_awards={same_buyer}",
                f"vehicle_fit={vehicle_fit}",
                f"set_aside_fit={set_aside_fit}",
            ],
        )

    def score_capability_fit(self, profile: ContractorProfile) -> FactorResult:
        capability_overlap = overlap_score(self.opportunity.required_capabilities, profile.capabilities)
        clearance_overlap = overlap_score(self.opportunity.required_clearances, profile.clearances)
        certification_overlap = overlap_score(self.opportunity.required_certifications, profile.certifications)
        best_award_similarity = max(
            [text_similarity(self.opportunity.description, award.description) for award in profile.awards],
            default=0.0,
        )
        differentiator_score = min(len(profile.differentiators) / 3.0, 1.0)

        score = 100 * (
            0.45 * capability_overlap
            + 0.15 * clearance_overlap
            + 0.10 * certification_overlap
            + 0.20 * best_award_similarity
            + 0.10 * differentiator_score
        )

        flags: list[str] = []
        if self.opportunity.small_business_participation_material and not profile.socio_statuses:
            flags.append("Small-business participation looks material but no qualifying status is present.")

        return FactorResult(
            name="capability_fit",
            score=clamp(score),
            confidence=0.75 if self.opportunity.required_capabilities else 0.5,
            rationale="Blend of capability overlap, clearance and certification coverage, prior similar work, and differentiators.",
            evidence=[
                f"capability_overlap={capability_overlap:.2f}",
                f"clearance_overlap={clearance_overlap:.2f}",
                f"certification_overlap={certification_overlap:.2f}",
                f"best_award_similarity={best_award_similarity:.2f}",
            ],
            flags=flags,
        )

    def score_past_performance(self, profile: ContractorProfile, mode: str) -> FactorResult:
        if not profile.awards:
            return FactorResult(
                name="past_performance",
                score=0.0,
                confidence=0.2,
                rationale="No award history provided.",
                flags=["No internal past performance examples"],
            )

        scenario_value = self.expected_contract_value(mode)
        scores: list[float] = []
        for award in profile.awards:
            prime_role_bonus = 1.0 if award.is_prime else 0.7
            if mode == "sub_only":
                prime_role_bonus = 1.0 if not award.is_prime else 0.85

            score = 100 * (
                0.40 * text_similarity(self.opportunity.description, award.description)
                + 0.15 * recency_decay(award.award_date)
                + 0.15 * ratio_fit(award.value, scenario_value)
                + 0.10 * float(
                    award.contract_type is not None
                    and self.opportunity.contract_type is not None
                    and award.contract_type.lower() == self.opportunity.contract_type.lower()
                )
                + 0.10 * float(award.buyer.lower() == self.opportunity.buyer.lower())
                + 0.10 * prime_role_bonus
            )
            scores.append(score)

        top_three = sorted(scores, reverse=True)[:3]
        return FactorResult(
            name="past_performance",
            score=clamp(mean(top_three)),
            confidence=min(0.9, 0.4 + 0.1 * len(top_three)),
            rationale=f"Top {len(top_three)} comparable examples averaged instead of flattening the full award history.",
            evidence=[f"top_example_scores={[round(score, 2) for score in top_three]}"],
        )

    def score_price_fit(self, profile: ContractorProfile, mode: str) -> FactorResult:
        price_band = self.buyer_history.price_band
        if price_band is None or price_band.median is None:
            return FactorResult(
                name="price_fit",
                score=50.0,
                confidence=0.25,
                rationale="No reliable comparable-award price band is available.",
                flags=["Pricing data gap"],
            )

        expected_margin = self.expected_margin(profile, mode)
        if expected_margin is None:
            return FactorResult(
                name="price_fit",
                score=50.0,
                confidence=0.25,
                rationale="Comparable pricing exists, but the contractor margin posture is missing.",
                evidence=[f"median_price={price_band.median:,.0f}"],
                flags=["Missing expected margin at market price"],
            )

        if expected_margin >= profile.margin_floor:
            score = 85.0 if price_band.comparable_count >= 10 else 75.0
            flags: list[str] = []
        elif expected_margin >= profile.margin_floor * 0.8:
            score = 55.0
            flags = ["Thin margin at the likely winning price"]
        else:
            score = 20.0
            flags = ["Cannot hit the likely market band without breaking margin floor"]

        return FactorResult(
            name="price_fit",
            score=score,
            confidence=min(0.95, 0.3 + 0.03 * price_band.comparable_count),
            rationale=f"Median comparable price is {price_band.median:,.0f} with expected margin {expected_margin:.1%}.",
            evidence=[
                f"low={price_band.low}",
                f"median={price_band.median}",
                f"high={price_band.high}",
                f"comparables={price_band.comparable_count}",
            ],
            flags=flags,
        )

    def score_competition(self, profile: ContractorProfile) -> FactorResult:
        competitors = self.buyer_history.competitors
        competitor_count = len(competitors)
        incumbent_present = any(competitor.is_incumbent for competitor in competitors)
        concentration_penalty = 25.0 * self.buyer_history.concentration
        switch_bonus = 10.0 * self.buyer_history.switching_rate
        discriminator_bonus = 5.0 if profile.differentiators else 0.0

        score = 100.0 - (10.0 * min(competitor_count, 6)) - (20.0 if incumbent_present else 0.0) - concentration_penalty + switch_bonus + discriminator_bonus

        return FactorResult(
            name="competition",
            score=clamp(score),
            confidence=0.65 if competitors else 0.3,
            rationale=f"{competitor_count} serious competitors, incumbent present={incumbent_present}, buyer concentration={self.buyer_history.concentration:.2f}.",
            evidence=[
                f"competitor_count={competitor_count}",
                f"incumbent_present={incumbent_present}",
                f"switching_rate={self.buyer_history.switching_rate:.2f}",
            ],
        )

    def score_delivery(self, profile: ContractorProfile, mode: str) -> FactorResult:
        clearance_overlap = overlap_score(self.opportunity.required_clearances, profile.clearances)
        certification_overlap = overlap_score(self.opportunity.required_certifications, profile.certifications)
        fte_score = 1.0 if profile.available_fte >= 3 else max(profile.available_fte / 3.0, 0.0)
        transition_score = 1.0 - clamp(self.opportunity.transition_complexity, 0.0, 100.0) / 100.0
        recruiting_score = 1.0 - clamp(self.opportunity.recruiting_difficulty, 0.0, 100.0) / 100.0
        teammate_dependence_penalty = 0.85 if mode == "prime_with_teammate" else 1.0

        score = 100 * teammate_dependence_penalty * (
            0.30 * clearance_overlap
            + 0.10 * certification_overlap
            + 0.25 * fte_score
            + 0.20 * transition_score
            + 0.15 * recruiting_score
        )

        return FactorResult(
            name="delivery",
            score=clamp(score),
            confidence=0.7,
            rationale="Blend of labor availability, credential coverage, transition complexity, and recruiting difficulty.",
            evidence=[
                f"fte_available={profile.available_fte}",
                f"transition_complexity={self.opportunity.transition_complexity}",
                f"recruiting_difficulty={self.opportunity.recruiting_difficulty}",
            ],
        )

    def score_strategy(self, profile: ContractorProfile) -> FactorResult:
        score = clamp(profile.strategic_priority_score)
        flags: list[str] = []
        if self.opportunity.incumbent_vendor and self.opportunity.incumbent_vendor.lower() == profile.name.lower():
            score = clamp(score + 10.0)
            flags.append("Incumbent defense value present.")

        return FactorResult(
            name="strategy",
            score=score,
            confidence=0.8,
            rationale="Internal strategic value and franchise importance.",
            flags=flags,
        )

    def score_readiness(self, profile: ContractorProfile, mode: str) -> FactorResult:
        days_left = days_until(self.opportunity.due_date)
        if days_left is None:
            time_score = 50.0
            time_evidence = "days_to_due=unknown"
        elif days_left >= 21:
            time_score = 100.0
            time_evidence = f"days_to_due={days_left}"
        else:
            time_score = max(20.0, 100.0 * (days_left / 21.0))
            time_evidence = f"days_to_due={days_left}"

        if mode == "monitor_and_shape":
            time_score = max(time_score, 70.0)

        score = (
            0.50 * profile.proposal_assets_score
            + 0.30 * time_score
            + 0.20 * self.opportunity.key_personnel_coverage_score
        )

        flags: list[str] = []
        if self.opportunity.far_5222246_included and self.opportunity.key_personnel_coverage_score < 60:
            flags.append("Compensation realism risk looks material.")

        return FactorResult(
            name="readiness",
            score=clamp(score),
            confidence=0.8,
            rationale="Blend of proposal assets, remaining time, and key-person coverage.",
            evidence=[
                time_evidence,
                f"proposal_assets_score={profile.proposal_assets_score}",
                f"key_personnel_coverage_score={self.opportunity.key_personnel_coverage_score}",
            ],
            flags=flags,
        )

    def score_all_factors(self, profile: ContractorProfile, mode: str) -> dict[str, FactorResult]:
        return {
            "customer_fit": self.score_customer_fit(profile, mode),
            "capability_fit": self.score_capability_fit(profile),
            "past_performance": self.score_past_performance(profile, mode),
            "price_fit": self.score_price_fit(profile, mode),
            "competition": self.score_competition(profile),
            "delivery": self.score_delivery(profile, mode),
            "strategy": self.score_strategy(profile),
            "readiness": self.score_readiness(profile, mode),
        }

    def compute_weighted_score(self, factors: dict[str, FactorResult], weights: dict[str, float]) -> float:
        return sum(weights[name] * factors[name].score for name in SCORING_FACTORS)

    def compute_confidence(self, factors: dict[str, FactorResult], weights: dict[str, float]) -> float:
        return sum(weights[name] * factors[name].confidence for name in SCORING_FACTORS)

    def compute_pwin(self, weighted_score: float) -> float:
        return 1.0 / (1.0 + math.exp(-8.0 * ((weighted_score / 100.0) - 0.60)))

    def compute_expected_value(self, profile: ContractorProfile, delivery_score: float, pwin: float, mode: str) -> float:
        contract_value = self.expected_contract_value(mode)
        if mode == "monitor_and_shape":
            return -(self.settings.monitor_shaping_cost + profile.opportunity_cost * 0.25)

        expected_margin = self.expected_margin(profile, mode) or profile.margin_floor
        expected_gross_profit = contract_value * expected_margin
        risk_reserve = max(0.0, (70.0 - delivery_score)) * 1_000.0
        return (pwin * expected_gross_profit) - profile.bid_cost - profile.opportunity_cost - risk_reserve

    def recommend(
        self,
        mode: str,
        gate_failures: list[str],
        pwin: float,
        expected_value: float,
        factors: dict[str, FactorResult],
    ) -> Recommendation:
        early_phase = self.opportunity.phase.lower() in {"sources_sought", "rfi", "presolicitation", "forecast"}

        if mode == "monitor_and_shape":
            if early_phase and factors["strategy"].score >= self.settings.strategic_floor_monitor:
                return "MONITOR_AND_SHAPE"
            return "NO_BID"

        if gate_failures:
            if mode == "prime_with_teammate" and not any("clearance" in failure.lower() for failure in gate_failures):
                return "MONITOR_AND_SHAPE" if early_phase else "NO_BID"
            if mode == "sub_only" and not any("clearance" in failure.lower() or "certification" in failure.lower() for failure in gate_failures):
                return "SUB_ONLY" if expected_value > 0 else "NO_BID"
            return "MONITOR_AND_SHAPE" if early_phase and factors["strategy"].score >= self.settings.strategic_floor_monitor else "NO_BID"

        if mode == "prime_solo" and pwin >= self.settings.pwin_floor_bid and expected_value > 0 and factors["readiness"].score >= self.settings.readiness_floor_bid:
            return "BID"

        if mode == "prime_with_teammate" and pwin >= self.settings.pwin_floor_partner and expected_value > 0:
            return "BID_WITH_PARTNER"

        if mode == "sub_only" and pwin >= self.settings.pwin_floor_partner and expected_value > 0:
            return "SUB_ONLY"

        if early_phase and factors["strategy"].score >= self.settings.strategic_floor_monitor:
            return "MONITOR_AND_SHAPE"

        return "NO_BID"

    def next_actions(
        self,
        recommendation: Recommendation,
        factors: dict[str, FactorResult],
        teammate_name: str | None,
    ) -> list[str]:
        actions: list[str] = []

        if recommendation == "BID_WITH_PARTNER" and teammate_name:
            actions.append(f"Qualify {teammate_name} as the lead teaming candidate and close the remaining role gaps.")
        if recommendation == "SUB_ONLY":
            actions.append("Identify the most credible prime and shape the opportunity toward a sub role.")
        if recommendation == "MONITOR_AND_SHAPE":
            actions.append("Track buyer signals, close data gaps, and revisit once the requirement and capture posture mature.")
        if factors["price_fit"].score < 60:
            actions.append("Tighten the comparable-award cohort and refine the price-to-win band.")
        if factors["past_performance"].score < 60:
            actions.append("Find stronger relevant past performance examples or partner references.")
        if factors["readiness"].score < 60:
            actions.append("Assess proposal assets, staffing, and timeline before committing.")
        if factors["competition"].score < 50:
            actions.append("Pressure-test the recommendation with a black hat review before final commitment.")

        return actions

    def evaluate_scenario(
        self,
        scenario_key: str,
        scenario_display_name: str,
        profile: ContractorProfile,
        mode: str,
        teammate_name: str | None = None,
    ) -> ScenarioEvaluation:
        gate_failures = self.run_gates(profile, mode)
        weights = self.resolve_weights()
        factors = self.score_all_factors(profile, mode)
        weighted_score = self.compute_weighted_score(factors, weights)
        confidence = self.compute_confidence(factors, weights)
        pwin = self.compute_pwin(weighted_score)
        expected_value = self.compute_expected_value(profile, factors["delivery"].score, pwin, mode)
        recommendation = self.recommend(mode, gate_failures, pwin, expected_value, factors)
        next_actions = self.next_actions(recommendation, factors, teammate_name)

        return ScenarioEvaluation(
            scenario_key=scenario_key,
            scenario_display_name=scenario_display_name,
            recommendation=recommendation,
            weighted_score=weighted_score,
            pwin=pwin,
            expected_value=expected_value,
            confidence=confidence,
            gate_failures=gate_failures,
            factor_results=[factors[name] for name in SCORING_FACTORS],
            next_actions=next_actions,
            teammate_name=teammate_name,
        )

    def evaluate_best_teammate(self) -> ScenarioEvaluation:
        if not self.teammates:
            scenario = self.evaluate_scenario(
                "prime_with_teammate",
                "Prime With Best-Fit Teammate",
                self.contractor_profile,
                "prime_with_teammate",
            )
            scenario.gate_failures.append("No teammate candidates were provided.")
            scenario.recommendation = "NO_BID"
            scenario.next_actions.insert(0, "Identify and qualify teammate candidates before relying on a partnered pursuit posture.")
            return scenario

        teammate_scenarios = [
            self.evaluate_scenario(
                "prime_with_teammate",
                "Prime With Best-Fit Teammate",
                merge_profiles(self.contractor_profile, teammate),
                "prime_with_teammate",
                teammate_name=teammate.name,
            )
            for teammate in self.teammates
        ]

        return max(teammate_scenarios, key=self.scenario_sort_key)

    def scenario_sort_key(self, scenario: ScenarioEvaluation) -> tuple[int, float, float]:
        rank = {
            "BID": 4,
            "BID_WITH_PARTNER": 3,
            "SUB_ONLY": 2,
            "MONITOR_AND_SHAPE": 1,
            "NO_BID": 0,
        }[scenario.recommendation]
        return (rank, scenario.expected_value, scenario.pwin)

    def choose_final(self, scenarios: list[ScenarioEvaluation]) -> ScenarioEvaluation:
        viable = [
            scenario
            for scenario in scenarios
            if scenario.recommendation in {"BID", "BID_WITH_PARTNER", "SUB_ONLY"}
            and scenario.expected_value > 0
        ]
        if viable:
            return max(viable, key=lambda scenario: (scenario.expected_value, scenario.pwin, self.scenario_sort_key(scenario)))

        monitors = [scenario for scenario in scenarios if scenario.recommendation == "MONITOR_AND_SHAPE"]
        if monitors:
            return max(monitors, key=self.scenario_sort_key)

        return max(scenarios, key=self.scenario_sort_key)

    def analyze(self) -> Decision:
        scenarios = [
            self.evaluate_scenario("prime_solo", "Prime Solo", self.contractor_profile, "prime_solo"),
            self.evaluate_best_teammate(),
            self.evaluate_scenario("sub_only", "Sub Only", self.contractor_profile, "sub_only"),
            self.evaluate_scenario("monitor_and_shape", "Monitor and Shape", self.contractor_profile, "monitor_and_shape"),
        ]

        selected = self.choose_final(scenarios)

        return Decision(
            recommendation=selected.recommendation,
            selected_scenario_key=selected.scenario_key,
            selected_scenario_display_name=selected.scenario_display_name,
            pwin=selected.pwin,
            expected_value=selected.expected_value,
            confidence=selected.confidence,
            missing_data_warnings=self.build_missing_data_warnings(),
            scenarios=scenarios,
        )


def load_payload(path: str | None, demo: bool) -> dict[str, Any]:
    if demo:
        return demo_payload()

    if path is None:
        raise ValueError("Provide an input JSON file path or pass --demo.")

    if path == "-":
        return json.load(sys.stdin)

    return json.loads(Path(path).read_text())


def demo_payload() -> dict[str, Any]:
    return {
        "opportunity": {
            "opportunity_id": "opp-001",
            "buyer": "Department of the Air Force",
            "office": "AFLCMC/HB",
            "description": "Provide cyber operations support, cleared engineering staff, and program transition services for a recompete.",
            "naics": "541512",
            "psc": "R425",
            "contract_type": "FFP",
            "estimated_value": 18_000_000,
            "realistic_order_value": 15_000_000,
            "set_aside": "8(a)",
            "vehicle_required": "GSA OASIS SB",
            "due_date": "2026-05-15",
            "phase": "solicitation",
            "required_capabilities": ["cyber operations", "program management", "systems engineering"],
            "required_clearances": ["Secret"],
            "required_certifications": ["ISO 27001"],
            "small_business_participation_material": True,
            "far_5222246_included": True,
            "incumbent_vendor": "Incumbent Systems LLC",
            "transition_complexity": 60,
            "recruiting_difficulty": 55,
            "key_personnel_coverage_score": 70,
        },
        "buyer_history": {
            "price_band": {
                "low": 13_500_000,
                "median": 15_200_000,
                "high": 16_800_000,
                "comparable_count": 14,
            },
            "concentration": 0.42,
            "switching_rate": 0.35,
            "competitors": [
                {"name": "Incumbent Systems LLC", "is_incumbent": True, "strength_score": 85},
                {"name": "Vector Mission Partners", "strength_score": 72},
                {"name": "Apex Technical Group", "strength_score": 68},
            ],
            "comparable_awards": [
                {
                    "award_id": "awd-001",
                    "buyer": "Department of the Air Force",
                    "office": "AFLCMC/HB",
                    "description": "Cyber operations and cleared program support services.",
                    "contract_type": "FFP",
                    "value": 14_800_000,
                    "award_date": "2024-02-01",
                    "is_prime": True,
                }
            ],
        },
        "contractor_profile": {
            "name": "Blue Forge Federal",
            "capabilities": ["cyber operations", "systems engineering", "program management"],
            "clearances": ["Secret", "Top Secret"],
            "certifications": ["ISO 27001"],
            "vehicles": ["GSA OASIS SB"],
            "socio_statuses": ["8(a)"],
            "available_fte": 10,
            "margin_floor": 0.12,
            "bid_cost": 180_000,
            "opportunity_cost": 40_000,
            "proposal_assets_score": 78,
            "strategic_priority_score": 82,
            "expected_margin_at_market_price": 0.15,
            "differentiators": ["same-office cyber ops delivery", "cleared surge staffing"],
            "awards": [
                {
                    "award_id": "pp-001",
                    "buyer": "Department of the Air Force",
                    "office": "AFLCMC/HB",
                    "description": "Delivered cleared cyber operations support and systems engineering services.",
                    "contract_type": "FFP",
                    "value": 13_900_000,
                    "award_date": "2025-01-10",
                    "is_prime": True,
                },
                {
                    "award_id": "pp-002",
                    "buyer": "Department of the Air Force",
                    "office": "AFLCMC/WI",
                    "description": "Program transition and engineering support for mission systems.",
                    "contract_type": "FFP",
                    "value": 9_100_000,
                    "award_date": "2023-08-14",
                    "is_prime": True,
                },
            ],
        },
        "teammates": [
            {
                "name": "Signal Ridge Partners",
                "capabilities": ["cyber operations", "intel support"],
                "clearances": ["Secret"],
                "certifications": ["ISO 27001"],
                "vehicles": ["GSA OASIS SB", "8(a) STARS III"],
                "socio_statuses": ["8(a)"],
                "available_fte": 6,
                "bid_cost": 40_000,
                "opportunity_cost": 15_000,
                "proposal_assets_score": 70,
                "strategic_priority_score": 72,
                "expected_margin_at_market_price": 0.13,
                "awards": [
                    {
                        "award_id": "tm-001",
                        "buyer": "Department of the Air Force",
                        "office": "AFLCMC/HB",
                        "description": "Supported cyber modernization delivery as a major subcontractor.",
                        "contract_type": "FFP",
                        "value": 7_200_000,
                        "award_date": "2024-07-01",
                        "is_prime": False,
                    }
                ],
            }
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deterministic bid / no-bid engine for the GovTribe Capture Workflows skill.",
    )
    parser.add_argument(
        "input_path",
        nargs="?",
        help="Path to the normalized pursuit JSON payload. Use '-' to read from stdin.",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the engine against an embedded demo payload.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        payload = load_payload(args.input_path, demo=args.demo)
        engine = BidNoBidEngine(
            opportunity=Opportunity.from_dict(payload.get("opportunity") or {}),
            buyer_history=BuyerHistory.from_dict(payload.get("buyer_history")),
            contractor_profile=ContractorProfile.from_dict(payload.get("contractor_profile") or {}),
            teammates=[
                ContractorProfile.from_dict(item)
                for item in payload.get("teammates", [])
            ],
            settings=EngineSettings.from_dict(payload.get("settings")),
        )
        decision = engine.analyze().to_dict()
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    if args.pretty:
        print(json.dumps(decision, indent=2))
    else:
        print(json.dumps(decision))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
