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


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


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


def keyword_overlap(left: str, right: str) -> float:
    left_tokens = set(tokenize(left))
    right_tokens = set(tokenize(right))
    if not left_tokens or not right_tokens:
        return 0.0

    return len(left_tokens & right_tokens) / len(left_tokens)


def mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def percentile(sorted_values: list[float], pct: float) -> float | None:
    if not sorted_values:
        return None

    if len(sorted_values) == 1:
        return sorted_values[0]

    position = clamp(pct, 0.0, 1.0) * (len(sorted_values) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]

    fraction = position - lower
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * fraction


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


def recency_score(date_value: datetime | None, half_life_years: float = 3.0) -> float:
    if date_value is None:
        return 0.5

    years = max((datetime.now(timezone.utc) - date_value).days / 365.25, 0.0)
    return math.exp(-math.log(2) * years / half_life_years)


def ratio_fit(left: float | None, right: float | None) -> float:
    if left is None or right is None or left <= 0 or right <= 0:
        return 0.5

    return max(0.0, 1.0 - min(abs(math.log(left / right)), 1.5) / 1.5)


def qualitative_standing(score: float, eval_method: str, acceptability_threshold: float) -> str:
    if eval_method == "lpta":
        return "ACCEPTABLE" if score >= acceptability_threshold else "UNACCEPTABLE"

    if score >= 0.85:
        return "OUTSTANDING"
    if score >= 0.70:
        return "GOOD"
    if score >= 0.55:
        return "ACCEPTABLE"
    if score >= 0.40:
        return "MARGINAL"

    return "UNACCEPTABLE"


@dataclass
class Requirement:
    id: str
    factor: str
    text: str
    weight: float = 1.0
    required_clearance: str | None = None
    required_place: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Requirement":
        return cls(
            id=str(payload.get("id") or ""),
            factor=str(payload.get("factor") or "general"),
            text=str(payload.get("text") or ""),
            weight=float(payload.get("weight", 1.0) or 1.0),
            required_clearance=payload.get("required_clearance"),
            required_place=payload.get("required_place"),
        )


@dataclass
class Factor:
    id: str
    name: str
    weight: float = 1.0
    minimum_acceptability: float = 0.60

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Factor":
        return cls(
            id=str(payload.get("id") or ""),
            name=str(payload.get("name") or payload.get("id") or ""),
            weight=float(payload.get("weight", 1.0) or 1.0),
            minimum_acceptability=float(payload.get("minimum_acceptability", 0.60) or 0.60),
        )


@dataclass
class EvaluationModel:
    eval_method: str
    contract_type: str
    required_vehicle: str | None
    estimated_value: float | None
    factors: list[Factor]
    requirements: list[Requirement]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EvaluationModel":
        return cls(
            eval_method=str(payload.get("eval_method") or "unknown").lower(),
            contract_type=str(payload.get("contract_type") or payload.get("contractType") or "unknown"),
            required_vehicle=payload.get("required_vehicle"),
            estimated_value=float(payload["estimated_value"]) if payload.get("estimated_value") is not None else None,
            factors=[Factor.from_dict(item) for item in payload.get("factors", [])],
            requirements=[Requirement.from_dict(item) for item in payload.get("requirements", [])],
        )

    def factor_map(self) -> dict[str, Factor]:
        return {factor.id: factor for factor in self.factors}

    def to_dict(self) -> dict[str, Any]:
        return {
            "eval_method": self.eval_method,
            "contract_type": self.contract_type,
            "required_vehicle": self.required_vehicle,
            "estimated_value": self.estimated_value,
            "factors": [
                {
                    "id": factor.id,
                    "name": factor.name,
                    "weight": factor.weight,
                    "minimum_acceptability": factor.minimum_acceptability,
                }
                for factor in self.factors
            ],
            "requirements": [
                {
                    "id": requirement.id,
                    "factor": requirement.factor,
                    "text": requirement.text,
                    "weight": requirement.weight,
                    "required_clearance": requirement.required_clearance,
                    "required_place": requirement.required_place,
                }
                for requirement in self.requirements
            ],
        }


@dataclass
class Opportunity:
    id: str
    agency: str
    buyer: str
    office: str
    description: str
    contract_type: str
    required_vehicle: str | None
    estimated_value: float | None
    place_of_performance: str | None
    set_aside: str | None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Opportunity":
        agency = str(payload.get("agency") or payload.get("buyer") or "")
        return cls(
            id=str(payload.get("id") or ""),
            agency=agency,
            buyer=str(payload.get("buyer") or agency),
            office=str(payload.get("office") or ""),
            description=str(payload.get("description") or ""),
            contract_type=str(payload.get("contract_type") or "unknown"),
            required_vehicle=payload.get("required_vehicle"),
            estimated_value=float(payload["estimated_value"]) if payload.get("estimated_value") is not None else None,
            place_of_performance=payload.get("place_of_performance"),
            set_aside=payload.get("set_aside"),
        )


@dataclass
class AwardRecord:
    award_id: str
    agency: str
    office: str
    description: str
    value: float | None = None
    contract_type: str | None = None
    end_date: datetime | None = None
    cpars_rating: float | None = None
    official_source: bool = False
    cross_source_agreement: float = 0.5
    place_of_performance: str | None = None
    clearance: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AwardRecord":
        return cls(
            award_id=str(payload.get("award_id") or payload.get("id") or ""),
            agency=str(payload.get("agency") or payload.get("buyer") or ""),
            office=str(payload.get("office") or ""),
            description=str(payload.get("description") or ""),
            value=float(payload["value"]) if payload.get("value") is not None else None,
            contract_type=payload.get("contract_type"),
            end_date=parse_datetime(payload.get("end_date")),
            cpars_rating=float(payload["cpars_rating"]) if payload.get("cpars_rating") is not None else None,
            official_source=bool(payload.get("official_source", False)),
            cross_source_agreement=float(payload.get("cross_source_agreement", 0.5) or 0.5),
            place_of_performance=payload.get("place_of_performance"),
            clearance=payload.get("clearance"),
        )


@dataclass
class Bidder:
    vendor_id: str
    name: str
    capabilities_text: str = ""
    vehicles: list[str] = field(default_factory=list)
    clearances: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    socio_statuses: list[str] = field(default_factory=list)
    places: list[str] = field(default_factory=list)
    awards: list[AwardRecord] = field(default_factory=list)
    is_incumbent: bool = False
    teammates: list[str] = field(default_factory=list)
    momentum_score: float = 0.5
    engagement_score: float = 0.5
    likely_role: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Bidder":
        return cls(
            vendor_id=str(payload.get("vendor_id") or ""),
            name=str(payload.get("name") or ""),
            capabilities_text=str(payload.get("capabilities_text") or ""),
            vehicles=[str(item) for item in payload.get("vehicles", [])],
            clearances=[str(item) for item in payload.get("clearances", [])],
            certifications=[str(item) for item in payload.get("certifications", [])],
            socio_statuses=[str(item) for item in payload.get("socio_statuses", [])],
            places=[str(item) for item in payload.get("places", [])],
            awards=[AwardRecord.from_dict(item) for item in payload.get("awards", [])],
            is_incumbent=bool(payload.get("is_incumbent", False)),
            teammates=[str(item) for item in payload.get("teammates", [])],
            momentum_score=float(payload.get("momentum_score", 0.5) or 0.5),
            engagement_score=float(payload.get("engagement_score", 0.5) or 0.5),
            likely_role=payload.get("likely_role"),
        )


@dataclass
class EvidenceEntry:
    evidence_id: str
    vendor_id: str
    category: str
    source_id: str
    support_score: float
    note: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "vendor_id": self.vendor_id,
            "category": self.category,
            "source_id": self.source_id,
            "support_score": round(self.support_score, 4),
            "note": self.note,
        }


class BlackHatEngine:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.evaluation_model = EvaluationModel.from_dict(payload.get("evaluation_model") or {})
        self.opportunity = Opportunity.from_dict(payload.get("opportunity") or {})
        self.bidders = [Bidder.from_dict(item) for item in payload.get("bidders", [])]
        self.our_team_vendor_id = payload.get("our_team_vendor_id")
        self.pricing = payload.get("pricing") or {}
        self.settings = payload.get("settings") or {}
        self.evidence_ledger: list[EvidenceEntry] = []

    def data_completeness(self, bidder: Bidder) -> float:
        checks = [
            bool(self.evaluation_model.requirements),
            bool(bidder.capabilities_text),
            bool(bidder.awards),
            bool(self.pricing_samples(bidder.vendor_id)),
        ]
        return mean([1.0 if value else 0.0 for value in checks])

    def source_agreement(self, bidder: Bidder) -> float:
        if not bidder.awards:
            return 0.5

        return mean([award.cross_source_agreement for award in bidder.awards])

    def model_stability(self, bidder: Bidder) -> float:
        signals = [
            1.0 if bidder.awards else 0.0,
            1.0 if self.pricing_samples(bidder.vendor_id) else 0.0,
            1.0 if bidder.capabilities_text else 0.0,
        ]
        return 0.5 + 0.5 * mean(signals)

    def human_override(self) -> float:
        return float(self.settings.get("human_override", 0.0) or 0.0)

    def pricing_samples(self, vendor_id: str) -> list[float]:
        samples = (self.pricing.get("samples_by_vendor") or {}).get(vendor_id, [])
        return sorted(float(value) for value in samples)

    def realism_risk(self, vendor_id: str) -> float | None:
        value = (self.pricing.get("realism_risk_by_vendor") or {}).get(vendor_id)
        if value is None:
            return None

        return clamp(float(value))

    def pricing_band(self, vendor_id: str) -> dict[str, float] | None:
        samples = self.pricing_samples(vendor_id)
        if not samples:
            return None

        return {
            "p10": percentile(samples, 0.10) or samples[0],
            "p50": percentile(samples, 0.50) or samples[0],
            "p90": percentile(samples, 0.90) or samples[-1],
        }

    def relationship_scores(self) -> dict[str, float]:
        adjacency: dict[str, set[str]] = {bidder.vendor_id: set(bidder.teammates) for bidder in self.bidders}
        total_nodes = max(len(self.bidders) - 1, 1)
        scores: dict[str, float] = {}
        for bidder in self.bidders:
            direct = len(adjacency.get(bidder.vendor_id, set()))
            reverse = sum(1 for other in self.bidders if bidder.vendor_id in adjacency.get(other.vendor_id, set()))
            scores[bidder.vendor_id] = clamp((direct + reverse) / (2 * total_nodes))
        return scores

    def requirement_evidence(self, bidder: Bidder, requirement: Requirement) -> tuple[float, str, str]:
        candidate_scores: list[tuple[float, str, str]] = []

        if bidder.capabilities_text:
            capability_score = (
                0.55 * text_similarity(requirement.text, bidder.capabilities_text)
                + 0.15 * keyword_overlap(requirement.text, bidder.capabilities_text)
                + 0.10 * 0.6
                + 0.10 * 0.7
                + 0.10 * self.customer_fit_from_awards(bidder.awards)
            )
            candidate_scores.append(
                (
                    capability_score,
                    f"{bidder.vendor_id}-capabilities",
                    "Capabilities narrative alignment",
                )
            )

        for award in bidder.awards:
            score = (
                0.55 * text_similarity(requirement.text, award.description)
                + 0.15 * keyword_overlap(requirement.text, award.description)
                + 0.10 * ratio_fit(award.value, self.opportunity.estimated_value or self.evaluation_model.estimated_value)
                + 0.10 * recency_score(award.end_date)
                + 0.10 * self.award_customer_fit(award)
            )
            candidate_scores.append(
                (
                    score,
                    award.award_id,
                    f"Award evidence from {award.award_id}",
                )
            )

        if not candidate_scores:
            return 0.0, f"{bidder.vendor_id}-missing-evidence", "No direct evidence available"

        return max(candidate_scores, key=lambda item: item[0])

    def award_customer_fit(self, award: AwardRecord) -> float:
        office_match = 1.0 if award.office and award.office.lower() == self.opportunity.office.lower() else 0.0
        agency_match = 1.0 if award.agency.lower() == self.opportunity.agency.lower() else 0.0
        return 0.6 * agency_match + 0.4 * office_match

    def customer_fit_from_awards(self, awards: list[AwardRecord]) -> float:
        if not awards:
            return 0.5
        return max(self.award_customer_fit(award) for award in awards)

    def coverage_score(self, bidder: Bidder) -> tuple[float, dict[str, float], list[str]]:
        if not self.evaluation_model.requirements:
            return 0.0, {}, ["No atomic requirements were provided."]

        total_weight = sum(requirement.weight for requirement in self.evaluation_model.requirements) or 1.0
        weighted_score = 0.0
        factor_totals: dict[str, list[float]] = {}
        evidence_ids: list[str] = []

        for requirement in self.evaluation_model.requirements:
            score, source_id, note = self.requirement_evidence(bidder, requirement)
            weighted_score += requirement.weight * score
            factor_totals.setdefault(requirement.factor, []).append(score)
            evidence_id = f"{bidder.vendor_id}-{requirement.id}"
            evidence_ids.append(evidence_id)
            self.evidence_ledger.append(
                EvidenceEntry(
                    evidence_id=evidence_id,
                    vendor_id=bidder.vendor_id,
                    category="requirement_coverage",
                    source_id=source_id,
                    support_score=score,
                    note=note,
                )
            )

        factor_scores = {factor_id: mean(scores) for factor_id, scores in factor_totals.items()}
        return weighted_score / total_weight, factor_scores, evidence_ids

    def past_performance_score(self, bidder: Bidder) -> tuple[float, list[str], list[str]]:
        if not bidder.awards:
            return 0.5, [], ["No relevant past performance data available."]

        scores: list[float] = []
        evidence_ids: list[str] = []
        flags: list[str] = []
        for award in bidder.awards:
            relevance = (
                0.35 * text_similarity(self.opportunity.description or " ".join(req.text for req in self.evaluation_model.requirements), award.description)
                + 0.20 * self.award_customer_fit(award)
                + 0.15 * float(
                    award.contract_type is not None
                    and award.contract_type.lower() == self.opportunity.contract_type.lower()
                )
                + 0.15 * ratio_fit(award.value, self.opportunity.estimated_value or self.evaluation_model.estimated_value)
                + 0.10 * recency_score(award.end_date)
                + 0.05 * self.place_or_security_fit(award, bidder)
            )
            data_completeness = mean(
                [
                    1.0 if award.description else 0.0,
                    1.0 if award.value is not None else 0.0,
                    1.0 if award.end_date is not None else 0.0,
                    1.0 if award.contract_type else 0.0,
                ]
            )
            cpars_component = 0.6 if award.cpars_rating is None else clamp(award.cpars_rating / 5.0)
            credibility = (
                0.50 * (1.0 if award.official_source else 0.6)
                + 0.20 * clamp(award.cross_source_agreement)
                + 0.15 * recency_score(award.end_date)
                + 0.15 * data_completeness
            )
            final_score = relevance * credibility * (0.7 + 0.3 * cpars_component)
            scores.append(final_score)
            evidence_id = f"{bidder.vendor_id}-pp-{award.award_id}"
            evidence_ids.append(evidence_id)
            self.evidence_ledger.append(
                EvidenceEntry(
                    evidence_id=evidence_id,
                    vendor_id=bidder.vendor_id,
                    category="past_performance",
                    source_id=award.award_id,
                    support_score=final_score,
                    note=f"Past performance evidence from {award.award_id}",
                )
            )

        if max(scores, default=0.0) < 0.45:
            flags.append("Past performance support is thin or weakly aligned.")

        return max(scores), evidence_ids, flags

    def place_or_security_fit(self, award: AwardRecord, bidder: Bidder) -> float:
        place_match = 0.5
        if self.opportunity.place_of_performance:
            place_match = 1.0 if self.opportunity.place_of_performance in bidder.places else 0.0
            if award.place_of_performance:
                place_match = 1.0 if award.place_of_performance == self.opportunity.place_of_performance else place_match

        if any(requirement.required_clearance for requirement in self.evaluation_model.requirements):
            needed = {requirement.required_clearance for requirement in self.evaluation_model.requirements if requirement.required_clearance}
            bidder_has = needed.issubset(set(bidder.clearances))
            award_has = award.clearance in needed if award.clearance else False
            security_match = 1.0 if bidder_has or award_has else 0.0
        else:
            security_match = 0.5

        return 0.5 * place_match + 0.5 * security_match

    def bid_probability(
        self,
        bidder: Bidder,
        coverage: float,
        past_performance: float,
        relationship: float,
    ) -> float:
        vehicle_fit = 0.5
        required_vehicle = self.evaluation_model.required_vehicle or self.opportunity.required_vehicle
        if required_vehicle:
            vehicle_fit = 1.0 if required_vehicle in bidder.vehicles else 0.0

        size_fit = ratio_fit(
            mean([award.value for award in bidder.awards if award.value is not None]) if bidder.awards else None,
            self.opportunity.estimated_value or self.evaluation_model.estimated_value,
        )
        place_fit = 1.0 if not self.opportunity.place_of_performance or self.opportunity.place_of_performance in bidder.places else 0.0
        clearance_fit = 1.0
        required_clearances = {requirement.required_clearance for requirement in self.evaluation_model.requirements if requirement.required_clearance}
        if required_clearances:
            clearance_fit = 1.0 if required_clearances.issubset(set(bidder.clearances)) else 0.0
        socio_fit = 1.0 if not self.opportunity.set_aside or self.opportunity.set_aside in bidder.socio_statuses else 0.0

        z = (
            -1.8
            + 1.2 * float(bidder.is_incumbent)
            + 1.0 * coverage
            + 0.8 * past_performance
            + 0.5 * vehicle_fit
            + 0.4 * relationship
            + 0.3 * size_fit
            + 0.3 * place_fit
            + 0.3 * clearance_fit
            + 0.2 * socio_fit
            + 0.2 * clamp(bidder.momentum_score)
            + 0.2 * clamp(bidder.engagement_score)
        )

        return 1.0 / (1.0 + math.exp(-z))

    def price_scores(self) -> tuple[dict[str, float], dict[str, dict[str, float] | None], list[str]]:
        price_bands = {bidder.vendor_id: self.pricing_band(bidder.vendor_id) for bidder in self.bidders}
        medians = {
            vendor_id: band["p50"]
            for vendor_id, band in price_bands.items()
            if band is not None
        }
        flags: list[str] = []
        if not medians:
            return {bidder.vendor_id: 0.5 for bidder in self.bidders}, price_bands, ["No price samples were provided."]

        sorted_medians = sorted(medians.items(), key=lambda item: item[1])
        scores: dict[str, float] = {}
        total = max(len(sorted_medians) - 1, 1)
        for rank, (vendor_id, _) in enumerate(sorted_medians):
            scores[vendor_id] = 1.0 - (rank / total)

        for bidder in self.bidders:
            scores.setdefault(bidder.vendor_id, 0.5)

        return scores, price_bands, flags

    def ranked_bidders(self, assessments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return sorted(
            [
                {
                    "vendor_id": assessment["vendor_id"],
                    "name": assessment["name"],
                    "bid_probability": assessment["bid_probability"],
                    "overall_score": assessment["overall_score"],
                    "likely_price_posture": assessment["competitor_view"]["likely_price_posture"],
                }
                for assessment in assessments
            ],
            key=lambda item: item["bid_probability"] * item["overall_score"],
            reverse=True,
        )

    def price_posture(self, score: float) -> str:
        if score >= 0.75:
            return "aggressive"
        if score >= 0.45:
            return "mid-pack"
        return "premium"

    def factor_scorecards(
        self,
        bidder: Bidder,
        coverage_factor_scores: dict[str, float],
        past_performance: float,
        price_score: float,
    ) -> list[dict[str, Any]]:
        factor_map = self.evaluation_model.factor_map()
        acceptability_threshold = float(self.settings.get("lpta_acceptability_threshold", 0.60) or 0.60)
        scorecards: list[dict[str, Any]] = []

        for factor in self.evaluation_model.factors:
            factor_name = factor.name.lower()
            if factor.id in coverage_factor_scores:
                score = coverage_factor_scores[factor.id]
            elif "past" in factor_name:
                score = past_performance
            elif "price" in factor_name or "cost" in factor_name:
                score = price_score
            elif "management" in factor_name or "staff" in factor_name:
                score = mean([coverage_factor_scores.get(factor.id, 0.0), bidder.engagement_score, bidder.momentum_score])
            else:
                score = mean(list(coverage_factor_scores.values())) if coverage_factor_scores else 0.0

            standing = qualitative_standing(score, self.evaluation_model.eval_method, factor.minimum_acceptability or acceptability_threshold)
            strengths: list[str] = []
            weaknesses: list[str] = []
            risks: list[str] = []

            if score >= 0.75:
                strengths.append(f"Likely strength under {factor.name}.")
            elif score < 0.50:
                weaknesses.append(f"Likely weakness under {factor.name}.")
            if self.evaluation_model.eval_method == "tradeoff" and score < 0.40:
                risks.append(f"{factor.name} may create a material tradeoff disadvantage.")
            if self.evaluation_model.eval_method == "lpta" and standing == "UNACCEPTABLE":
                risks.append(f"{factor.name} may fail minimum acceptability.")

            scorecards.append(
                {
                    "factor_id": factor.id,
                    "factor_name": factor.name,
                    "score": round(score, 4),
                    "standing": standing,
                    "strengths": strengths,
                    "weaknesses": weaknesses,
                    "risks": risks,
                }
            )

        return scorecards

    def competitor_assessment(
        self,
        bidder: Bidder,
        relationship_score: float,
        coverage: float,
        coverage_factor_scores: dict[str, float],
        past_performance: float,
        price_score: float,
        bid_probability: float,
        price_band: dict[str, float] | None,
        price_flags: list[str],
    ) -> dict[str, Any]:
        overall_score = clamp(
            0.35 * coverage
            + 0.25 * past_performance
            + 0.15 * price_score
            + 0.15 * relationship_score
            + 0.10 * bid_probability
        )
        confidence = (
            0.40 * self.data_completeness(bidder)
            + 0.30 * self.source_agreement(bidder)
            + 0.20 * self.model_stability(bidder)
            + 0.10 * self.human_override()
        )

        scorecards = self.factor_scorecards(
            bidder=bidder,
            coverage_factor_scores=coverage_factor_scores,
            past_performance=past_performance,
            price_score=price_score,
        )
        strengths = [strength for card in scorecards for strength in card["strengths"]]
        weaknesses = [weakness for card in scorecards for weakness in card["weaknesses"]]
        risks = [risk for card in scorecards for risk in card["risks"]]
        likely_win_themes = []
        likely_attack_themes = []
        if bidder.is_incumbent:
            likely_win_themes.append("Incumbent continuity and lower transition risk.")
        if price_score >= 0.75:
            likely_win_themes.append("Aggressive price posture.")
        if past_performance >= 0.70:
            likely_win_themes.append("Credible past performance against the buyer or lane.")
        if coverage >= 0.70:
            likely_win_themes.append("Strong requirement coverage.")
        if weaknesses:
            likely_attack_themes.append("Coverage gaps can be attacked directly against the scorecard.")
        if price_score < 0.45:
            likely_attack_themes.append("Premium pricing posture may be exposed.")

        realism_risk = self.realism_risk(bidder.vendor_id)
        missing_data_flags: list[str] = []
        if not bidder.awards:
            missing_data_flags.append("Award history is missing.")
        if price_band is None:
            missing_data_flags.append("Price samples are missing.")
        if not bidder.capabilities_text:
            missing_data_flags.append("Capabilities text is missing.")
        if realism_risk is not None and realism_risk > 0.40:
            missing_data_flags.append("Price realism risk looks elevated.")
        missing_data_flags.extend(price_flags)

        return {
            "vendor_id": bidder.vendor_id,
            "name": bidder.name,
            "bid_probability": round(bid_probability, 4),
            "coverage_score": round(coverage, 4),
            "past_performance_score": round(past_performance, 4),
            "relationship_score": round(relationship_score, 4),
            "price_position_score": round(price_score, 4),
            "overall_score": round(overall_score, 4),
            "likely_price_band": price_band,
            "evaluator_view": {
                "factor_scorecards": scorecards,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "risks": risks,
            },
            "competitor_view": {
                "likely_win_themes": likely_win_themes,
                "likely_attack_themes": likely_attack_themes,
                "likely_teaming_move": "incumbent defense" if bidder.is_incumbent else ("team for coverage or access" if bidder.teammates else "unclear"),
                "likely_price_posture": self.price_posture(price_score),
                "realism_risk": round(realism_risk, 4) if realism_risk is not None else None,
            },
            "confidence": round(confidence, 4),
            "missing_data_flags": missing_data_flags,
        }

    def predicted_bidders(self, assessments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        top_count = int(self.settings.get("top_bidder_count", 5) or 5)
        ranked = self.ranked_bidders(assessments)
        return ranked[:top_count]

    def our_position(self, assessments: list[dict[str, Any]]) -> dict[str, Any]:
        if not self.our_team_vendor_id:
            return {
                "status": "unknown",
                "note": "our_team_vendor_id was not provided.",
            }

        ranked = self.ranked_bidders(assessments)
        our_assessment = next(
            (assessment for assessment in assessments if assessment["vendor_id"] == self.our_team_vendor_id),
            None,
        )
        if our_assessment is None:
            return {
                "status": "unknown",
                "note": "our_team_vendor_id did not match any bidder.",
            }

        rank = next(
            (index + 1 for index, bidder in enumerate(ranked) if bidder["vendor_id"] == self.our_team_vendor_id),
            None,
        )
        strengths = our_assessment["evaluator_view"]["strengths"][:3]
        risks = our_assessment["evaluator_view"]["risks"][:3] + our_assessment["evaluator_view"]["weaknesses"][:3]

        return {
            "vendor_id": our_assessment["vendor_id"],
            "name": our_assessment["name"],
            "rank": rank,
            "bid_probability": our_assessment["bid_probability"],
            "overall_score": our_assessment["overall_score"],
            "factor_scorecards": our_assessment["evaluator_view"]["factor_scorecards"],
            "strongest_signals": strengths,
            "largest_exposures": risks,
            "likely_win_themes": our_assessment["competitor_view"]["likely_win_themes"],
            "likely_attack_themes": our_assessment["competitor_view"]["likely_attack_themes"],
            "likely_price_posture": our_assessment["competitor_view"]["likely_price_posture"],
            "realism_risk": our_assessment["competitor_view"]["realism_risk"],
            "evidence_ids": our_assessment["evidence_ids"],
            "confidence": our_assessment["confidence"],
        }

    def price_to_win(self, assessments: list[dict[str, Any]]) -> dict[str, Any]:
        market_samples = sorted(
            sample
            for bidder in self.bidders
            for sample in self.pricing_samples(bidder.vendor_id)
        )
        market_band = None
        if market_samples:
            market_band = {
                "p10": percentile(market_samples, 0.10),
                "p50": percentile(market_samples, 0.50),
                "p90": percentile(market_samples, 0.90),
            }

        likely_winner = max(
            assessments,
            key=lambda assessment: assessment["bid_probability"] * assessment["overall_score"],
            default=None,
        )
        return {
            "market_band": market_band,
            "our_margin_floor": self.pricing.get("our_margin_floor"),
            "our_expected_margin": self.pricing.get("our_expected_margin"),
            "realism_risk_by_vendor": {
                bidder.vendor_id: self.realism_risk(bidder.vendor_id)
                for bidder in self.bidders
                if self.realism_risk(bidder.vendor_id) is not None
            },
            "likely_winner_vendor_id": likely_winner["vendor_id"] if likely_winner else None,
            "likely_winner_price_posture": likely_winner["competitor_view"]["likely_price_posture"] if likely_winner else None,
            "notes": [
                "Price posture and realism are kept separate from pure competitor narrative.",
                "Use the price band as a guardrail, not as a substitute for the solicitation's stated evaluation rules.",
            ],
        }

    def recommended_actions(self, assessments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        our = next((assessment for assessment in assessments if assessment["vendor_id"] == self.our_team_vendor_id), None)
        top_competitor = next(
            (
                assessment
                for assessment in sorted(
                    assessments,
                    key=lambda item: item["bid_probability"] * item["overall_score"],
                    reverse=True,
                )
                if assessment["vendor_id"] != self.our_team_vendor_id
            ),
            None,
        )

        if our is None:
            return []

        actions: list[dict[str, Any]] = []

        if top_competitor and our["coverage_score"] < top_competitor["coverage_score"]:
            actions.append(
                {
                    "action": "Increase coverage on the weakest evaluation factor",
                    "expected_score_lift": round(top_competitor["coverage_score"] - our["coverage_score"], 4),
                    "expected_pwin_lift": round((top_competitor["coverage_score"] - our["coverage_score"]) * 0.25, 4),
                    "proposal_effort": "medium",
                    "margin_impact": "low",
                }
            )

        if our["past_performance_score"] < 0.65:
            actions.append(
                {
                    "action": "Swap in a more relevant past-performance example",
                    "expected_score_lift": round(0.75 - our["past_performance_score"], 4),
                    "expected_pwin_lift": round((0.75 - our["past_performance_score"]) * 0.20, 4),
                    "proposal_effort": "medium",
                    "margin_impact": "none",
                }
            )

        if our["competitor_view"]["likely_price_posture"] == "premium" and self.pricing.get("our_margin_floor") is not None:
            actions.append(
                {
                    "action": "Stress-test price against the modeled competitor band",
                    "expected_score_lift": 0.08,
                    "expected_pwin_lift": 0.05,
                    "proposal_effort": "medium",
                    "margin_impact": "medium",
                }
            )

        our_realism_risk = self.realism_risk(self.our_team_vendor_id)
        if our_realism_risk is not None and our_realism_risk > 0.35:
            actions.append(
                {
                    "action": "Restructure staffing assumptions to improve realism",
                    "expected_score_lift": 0.05,
                    "expected_pwin_lift": 0.03,
                    "proposal_effort": "medium",
                    "margin_impact": "medium",
                }
            )

        if any("transition" in requirement.text.lower() or "staff" in requirement.text.lower() for requirement in self.evaluation_model.requirements):
            actions.append(
                {
                    "action": "Sharpen transition and staffing credibility",
                    "expected_score_lift": 0.06,
                    "expected_pwin_lift": 0.04,
                    "proposal_effort": "medium",
                    "margin_impact": "low",
                }
            )

        if not actions:
            actions.append(
                {
                    "action": "Run an incumbent-plus-challenger scenario before lock",
                    "expected_score_lift": 0.03,
                    "expected_pwin_lift": 0.02,
                    "proposal_effort": "low",
                    "margin_impact": "none",
                }
            )

        return actions

    def confidence_summary(self, assessments: list[dict[str, Any]]) -> dict[str, Any]:
        overall = mean([assessment["confidence"] for assessment in assessments]) if assessments else 0.0
        return {
            "overall_confidence": round(overall, 4),
            "data_completeness": round(mean([self.data_completeness(bidder) for bidder in self.bidders]) if self.bidders else 0.0, 4),
            "source_agreement": round(mean([self.source_agreement(bidder) for bidder in self.bidders]) if self.bidders else 0.0, 4),
            "model_stability": round(mean([self.model_stability(bidder) for bidder in self.bidders]) if self.bidders else 0.0, 4),
            "human_override": round(self.human_override(), 4),
        }

    def run(self) -> dict[str, Any]:
        relationship_scores = self.relationship_scores()
        price_scores, price_bands, price_flags = self.price_scores()

        assessments: list[dict[str, Any]] = []
        for bidder in self.bidders:
            coverage, coverage_factor_scores, coverage_evidence_ids = self.coverage_score(bidder)
            past_performance, past_perf_evidence_ids, pp_flags = self.past_performance_score(bidder)
            bid_probability = self.bid_probability(
                bidder=bidder,
                coverage=coverage,
                past_performance=past_performance,
                relationship=relationship_scores.get(bidder.vendor_id, 0.0),
            )
            assessment = self.competitor_assessment(
                bidder=bidder,
                relationship_score=relationship_scores.get(bidder.vendor_id, 0.0),
                coverage=coverage,
                coverage_factor_scores=coverage_factor_scores,
                past_performance=past_performance,
                price_score=price_scores.get(bidder.vendor_id, 0.5),
                bid_probability=bid_probability,
                price_band=price_bands.get(bidder.vendor_id),
                price_flags=price_flags + pp_flags,
            )
            pricing_evidence_id: str | None = None
            if price_bands.get(bidder.vendor_id) is not None:
                pricing_evidence_id = f"{bidder.vendor_id}-pricing"
                self.evidence_ledger.append(
                    EvidenceEntry(
                        evidence_id=pricing_evidence_id,
                        vendor_id=bidder.vendor_id,
                        category="pricing",
                        source_id=f"{bidder.vendor_id}-price-samples",
                        support_score=price_scores.get(bidder.vendor_id, 0.5),
                        note="Comparable price samples and posture estimate.",
                    )
                )
            assessment["evidence_ids"] = coverage_evidence_ids + past_perf_evidence_ids + ([pricing_evidence_id] if pricing_evidence_id else [])
            assessments.append(assessment)

        predicted = self.predicted_bidders(assessments)
        our_position = self.our_position(assessments)

        competitor_assessments = [
            assessment
            for assessment in assessments
            if assessment["vendor_id"] != self.our_team_vendor_id
        ]

        return {
            "evaluation_model": self.evaluation_model.to_dict(),
            "predicted_bidders": predicted,
            "competitor_assessments": competitor_assessments,
            "our_position": our_position,
            "price_to_win": self.price_to_win(assessments),
            "recommended_actions": self.recommended_actions(assessments),
            "confidence_summary": self.confidence_summary(assessments),
            "evidence_ledger": [entry.to_dict() for entry in self.evidence_ledger],
        }


def demo_payload() -> dict[str, Any]:
    return {
        "evaluation_model": {
            "eval_method": "tradeoff",
            "required_vehicle": "GSA OASIS SB",
            "estimated_value": 22000000,
            "factors": [
                {"id": "technical", "name": "Technical Approach", "weight": 0.4},
                {"id": "past_performance", "name": "Past Performance", "weight": 0.25},
                {"id": "management", "name": "Management and Staffing", "weight": 0.2},
                {"id": "price", "name": "Price", "weight": 0.15},
            ],
            "requirements": [
                {"id": "req-1", "factor": "technical", "text": "Provide cleared cyber operations support.", "weight": 1.0, "required_clearance": "Secret"},
                {"id": "req-2", "factor": "technical", "text": "Support transition and sustainment for mission systems.", "weight": 0.9},
                {"id": "req-3", "factor": "management", "text": "Demonstrate staffing and transition readiness.", "weight": 0.8},
            ],
        },
        "opportunity": {
            "id": "opp-001",
            "agency": "Department of the Air Force",
            "buyer": "Department of the Air Force",
            "office": "AFLCMC/HB",
            "description": "Cyber operations support recompete.",
            "contract_type": "FFP",
            "required_vehicle": "GSA OASIS SB",
            "estimated_value": 22000000,
            "place_of_performance": "CONUS",
            "set_aside": "8(a)",
        },
        "bidders": [
            {
                "vendor_id": "our-team",
                "name": "Blue Forge Federal",
                "capabilities_text": "Cyber operations, systems engineering, transition planning, and sustainment support for mission programs.",
                "vehicles": ["GSA OASIS SB"],
                "clearances": ["Secret", "Top Secret"],
                "certifications": ["ISO 27001"],
                "socio_statuses": ["8(a)"],
                "places": ["CONUS"],
                "is_incumbent": False,
                "teammates": ["signal-ridge"],
                "momentum_score": 0.72,
                "engagement_score": 0.81,
                "awards": [
                    {
                        "award_id": "pp-001",
                        "agency": "Department of the Air Force",
                        "office": "AFLCMC/HB",
                        "description": "Cleared cyber operations support services.",
                        "value": 18000000,
                        "contract_type": "FFP",
                        "end_date": "2025-09-30",
                        "cpars_rating": 4.4,
                        "official_source": True,
                        "cross_source_agreement": 0.8,
                    }
                ],
            },
            {
                "vendor_id": "incumbent",
                "name": "Incumbent Systems LLC",
                "capabilities_text": "Incumbent cyber operations and sustainment support for Air Force mission systems.",
                "vehicles": ["GSA OASIS SB"],
                "clearances": ["Secret"],
                "places": ["CONUS"],
                "is_incumbent": True,
                "momentum_score": 0.78,
                "engagement_score": 0.65,
                "awards": [
                    {
                        "award_id": "pp-010",
                        "agency": "Department of the Air Force",
                        "office": "AFLCMC/HB",
                        "description": "Incumbent cyber operations support contract.",
                        "value": 21000000,
                        "contract_type": "FFP",
                        "end_date": "2026-03-31",
                        "cpars_rating": 4.7,
                        "official_source": True,
                        "cross_source_agreement": 0.9,
                    }
                ],
            },
            {
                "vendor_id": "challenger",
                "name": "Vector Mission Partners",
                "capabilities_text": "Mission engineering and cyber operations support with cleared staffing depth.",
                "vehicles": ["8(a) STARS III"],
                "clearances": ["Secret", "Top Secret"],
                "places": ["CONUS"],
                "is_incumbent": False,
                "teammates": ["signal-ridge"],
                "momentum_score": 0.63,
                "engagement_score": 0.59,
                "awards": [
                    {
                        "award_id": "pp-022",
                        "agency": "Department of the Air Force",
                        "office": "AFLCMC/WI",
                        "description": "Cyber engineering and sustainment support for mission systems.",
                        "value": 16000000,
                        "contract_type": "FFP",
                        "end_date": "2024-12-15",
                        "cpars_rating": 4.1,
                        "official_source": True,
                        "cross_source_agreement": 0.7,
                    }
                ],
            },
        ],
        "our_team_vendor_id": "our-team",
        "pricing": {
            "samples_by_vendor": {
                "our-team": [20500000, 21400000, 21900000],
                "incumbent": [19800000, 20600000, 21100000],
                "challenger": [20100000, 20900000, 21600000],
            },
            "realism_risk_by_vendor": {
                "our-team": 0.25,
                "incumbent": 0.15,
                "challenger": 0.20,
            },
            "our_margin_floor": 0.12,
            "our_expected_margin": 0.15,
        },
        "settings": {
            "top_bidder_count": 5,
            "human_override": 0.0,
            "lpta_acceptability_threshold": 0.60,
        },
    }


def load_payload(path: str | None, demo: bool) -> dict[str, Any]:
    if demo:
        return demo_payload()

    if path is None:
        raise ValueError("Provide an input JSON file path or pass --demo.")

    if path == "-":
        return json.load(sys.stdin)

    return json.loads(Path(path).read_text())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deterministic mock source-selection engine for the GovTribe Conduct Black Hat Review skill.",
    )
    parser.add_argument(
        "input_path",
        nargs="?",
        help="Path to the input JSON payload. Use '-' to read from stdin.",
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
        result = BlackHatEngine(payload).run()
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
