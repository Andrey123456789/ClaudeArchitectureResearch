#!/usr/bin/env python3
"""
Build the audited hidden-oracle revision of research/policy/inventory.json.

The script is intentionally deterministic and conservative:
- it requires the exact current v0.3 oracle shape/count/tree SHA;
- it never overwrites the source inventory by default;
- it removes only the two research-shared entries that are not V2-derived;
- it appends only audited V2-derived policies;
- it repairs known source-reference defects;
- it writes the moved research-shared invariants to a separate file;
- it validates IDs, counts, origins, source paths, and Markdown heading anchors.

All repository artifacts produced by this script are English-only.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any


EXPECTED_SCHEMA = "0.3"
EXPECTED_POLICY_COUNT = 180
EXPECTED_GROUP_COUNT = 10
EXPECTED_BASELINE_TREE_SHA = "563f575316fd60997b73a91187868459cdb15630"

REMOVED_RESEARCH_SHARED_IDS = ("GOV-017", "GOV-018")


def policy(
    policy_id: str,
    name: str,
    *,
    related_groups: list[str],
    normative_strength: str,
    trigger_class: str,
    scope: str,
    source_refs: list[str],
    normalized_policy: str,
) -> dict[str, Any]:
    return {
        "id": policy_id,
        "name": name,
        "related_groups": related_groups,
        "origin": "v2",
        "normative_strength": normative_strength,
        "trigger_class": trigger_class,
        "scope": scope,
        "source_refs": source_refs,
        "normalized_policy": normalized_policy,
        "status": "accepted_in_frozen_oracle",
    }


ADDITIONS: dict[str, list[dict[str, Any]]] = {
    "governance-product": [
        policy(
            "GOV-021",
            "Custom settings changes propagate across affected surfaces",
            related_groups=["persistence-data", "frontend", "testing-quality"],
            normative_strength="MUST",
            trigger_class="workflow",
            scope="common",
            source_refs=[
                "templates/v2-baseline/.claude/skills/custom-settings/SKILL.md#When Adding a New Setting",
                "templates/v2-baseline/.claude/skills/custom-settings/SKILL.md#When CUSTOM_SETTINGS.md Changes",
                "templates/v2-baseline/.claude/skills/custom-settings/SKILL.md#Verification",
            ],
            normalized_policy=(
                "When an approved CUSTOM_SETTINGS.md value is added, changed, or removed, "
                "identify and update every affected implementation, validation, configuration, "
                "test, documentation, and mirrored frontend/backend surface; search for stale "
                "references and run the normal verification workflow. Changing one literal alone "
                "does not establish synchronization."
            ),
        ),
    ],
    "architecture": [
        policy(
            "ARC-028",
            "Test-project production references stay narrow",
            related_groups=["testing-quality"],
            normative_strength="MUST_NOT",
            trigger_class="path",
            scope="backend-tests",
            source_refs=[
                "templates/v2-baseline/.claude/skills/project-structure/references/backend-layout.md#Test References"
            ],
            normalized_policy=(
                "Do not give backend test projects broader production-project references than "
                "their test scope requires; preserve the same inward dependency discipline used "
                "by the production architecture."
            ),
        ),
        policy(
            "ARC-029",
            "Transport contracts avoid gratuitous duplication",
            related_groups=["api-errors-validation"],
            normative_strength="MUST_NOT",
            trigger_class="path",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/project-structure/references/backend-layout.md#Contracts"
            ],
            normalized_policy=(
                "Do not duplicate equivalent DTOs across API and Application merely to create "
                "layer-shaped types; introduce transport-specific request/response contracts when "
                "separation from Application models provides a concrete boundary benefit."
            ),
        ),
    ],
    "persistence-data": [
        policy(
            "PST-009",
            "Schema-affecting custom settings co-change with persistence artifacts",
            related_groups=["governance-product", "testing-quality"],
            normative_strength="MUST",
            trigger_class="workflow",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/custom-settings/SKILL.md#Database Impact"
            ],
            normalized_policy=(
                "When a CUSTOM_SETTINGS.md change affects schema constraints, indexes, column "
                "lengths, or other persistence metadata, update EF Core mapping, create the "
                "appropriate migration according to the project's migration workflow, verify "
                "Development seeding remains valid, and update provider-sensitive persistence or "
                "integration tests when needed; do not casually alter existing migrations."
            ),
        ),
        policy(
            "PST-010",
            "EF Core migrations are reviewed source code",
            related_groups=["workflows-delivery"],
            normative_strength="MUST",
            trigger_class="workflow",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/ef-core/SKILL.md#Migrations"
            ],
            normalized_policy=(
                "Treat EF Core migrations as source code and review generated migrations before "
                "committing them, paying particular attention to destructive schema changes, "
                "unexpected column recreation, data migrations, indexes, foreign keys, and delete "
                "behavior."
            ),
        ),
    ],
    "api-errors-validation": [
        policy(
            "API-021",
            "Normal client cancellation is not a server failure",
            related_groups=["runtime-code-performance"],
            normative_strength="MUST_NOT",
            trigger_class="path",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/rules/error-handling.md#Cancellation",
                "templates/v2-baseline/.claude/skills/error-handling/SKILL.md#Cancellation",
            ],
            normalized_policy=(
                "Do not map normal client-request cancellation to a generic 500 response or log "
                "it as an unhandled application failure."
            ),
        ),
        policy(
            "API-022",
            "API deprecation preserves the promised migration window",
            related_groups=["dependencies-stack"],
            normative_strength="MUST",
            trigger_class="workflow",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/api-versioning/SKILL.md#Deprecation"
            ],
            normalized_policy=(
                "When deprecating an externally consumed API version, mark the deprecation in "
                "versioning metadata, document the replacement, communicate a realistic migration/"
                "removal timeline, and keep the old version working for the promised support "
                "period; do not remove it without considering the published support contract."
            ),
        ),
    ],
    "security": [
        policy(
            "SEC-016",
            "Authentication uses established platform mechanisms",
            related_groups=["architecture"],
            normative_strength="MUST_NOT",
            trigger_class="path",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/authentication/SKILL.md#Core Principles",
                "templates/v2-baseline/.claude/skills/authentication/SKILL.md#Local User Accounts",
            ],
            normalized_policy=(
                "Do not implement custom token/password security, password hashing, or reset-token "
                "cryptography when established ASP.NET Core authentication/Identity facilities "
                "cover the requirement."
            ),
        ),
        policy(
            "SEC-017",
            "Bearer authentication keeps effective token validation",
            related_groups=["api-errors-validation"],
            normative_strength="MUST",
            trigger_class="path",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/authentication/SKILL.md#Bearer Authentication",
                "templates/v2-baseline/.claude/skills/security-scan/references/scan-layers.md#Authentication Configuration",
            ],
            normalized_policy=(
                "For Bearer/OIDC authentication, validate the properties required by the actual "
                "issuer/provider, including issuer, audience where applicable, signature/signing "
                "authority, and lifetime; do not disable validation merely to make a token work."
            ),
        ),
        policy(
            "SEC-018",
            "Authentication failures avoid account-enumeration leaks",
            related_groups=["api-errors-validation"],
            normative_strength="MUST_NOT",
            trigger_class="path",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/authentication/SKILL.md#Authentication Errors"
            ],
            normalized_policy=(
                "Do not expose authentication-failure detail that unnecessarily reveals secrets "
                "or account state; login behavior should avoid account-enumeration leaks where "
                "relevant."
            ),
        ),
    ],
    "runtime-code-performance": [
        policy(
            "RUN-023",
            "Cache entries have explicit expiration or invalidation semantics",
            related_groups=[],
            normative_strength="MUST",
            trigger_class="path",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/caching/SKILL.md#Core Principles"
            ],
            normalized_policy=(
                "Every cache entry must have a lifetime or another explicit invalidation strategy."
            ),
        ),
        policy(
            "RUN-024",
            "C# file and async naming conventions remain conventional",
            related_groups=[],
            normative_strength="DEFAULT",
            trigger_class="path",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/rules/coding-style.md#Files and Namespaces",
                "templates/v2-baseline/.claude/rules/coding-style.md#Async Naming",
            ],
            normalized_policy=(
                "For new C# code, prefer file-scoped namespaces when consistent with the project, "
                "normally keep one primary top-level type per matching file, and use the Async "
                "suffix for Task/ValueTask-returning methods unless an existing or framework "
                "contract makes that inappropriate."
            ),
        ),
    ],
    "dependencies-stack": [
        policy(
            "DEP-025",
            "npm peer-dependency conflicts are not bypassed by force flags",
            related_groups=["frontend"],
            normative_strength="MUST_NOT",
            trigger_class="workflow",
            scope="frontend",
            source_refs=[
                "templates/v2-baseline/.claude/rules/dependencies.md#npm"
            ],
            normalized_policy=(
                "Do not use npm --force or --legacy-peer-deps merely to bypass incompatible peer "
                "dependencies; resolve the actual compatibility problem."
            ),
        ),
        policy(
            "DEP-026",
            "Local Development database configuration is usable and non-secret",
            related_groups=["persistence-data", "security"],
            normative_strength="DEFAULT",
            trigger_class="path",
            scope="backend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Development Database Configuration"
            ],
            normalized_policy=(
                "For the SQL Server baseline, appsettings.Development.json should provide a usable "
                "local Development connection string when it contains no secret credentials; "
                "credential-bearing local values must be supplied through user-secrets or another "
                "approved local secret mechanism."
            ),
        ),
    ],
    "frontend": [
        policy(
            "FE-011",
            "Avoid nested manual RxJS subscriptions",
            related_groups=[],
            normative_strength="DEFAULT",
            trigger_class="path",
            scope="frontend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/angular/SKILL.md#RxJS"
            ],
            normalized_policy=(
                "Avoid manual nested RxJS subscriptions and prefer composition operators when "
                "stream composition expresses the behavior clearly."
            ),
        ),
        policy(
            "FE-012",
            "Manual RxJS subscriptions follow framework lifecycle",
            related_groups=[],
            normative_strength="MUST",
            trigger_class="path",
            scope="frontend",
            source_refs=[
                "templates/v2-baseline/.claude/skills/angular/SKILL.md#RxJS"
            ],
            normalized_policy=(
                "When manually subscribing from Angular framework-managed code, tie the "
                "subscription lifetime to the component/service lifecycle using the project's "
                "current Angular facilities."
            ),
        ),
    ],
}


INTENTIONAL_NON_ORACLE_MATERIAL = [
    {
        "id": "EXC-001",
        "source_refs": ["templates/v2-baseline/SPECIFICATION.md"],
        "classification": "empty_product_input_placeholder",
        "rationale": (
            "The frozen V2 SPECIFICATION.md is empty. Product-input authority is represented by "
            "GOV-001..GOV-007; the empty placeholder contains no additional normative content."
        ),
    },
    {
        "id": "EXC-002",
        "source_refs": ["templates/v2-baseline/.claude/skills/modern-csharp/SKILL.md"],
        "classification": "optional_language_technique",
        "rationale": (
            "Primary-constructor, required-member, field-keyword, collection-expression, and "
            "immutability guidance is context-sensitive technique. Durable behavior is already "
            "bounded by RUN-009, RUN-024, and GOV-014."
        ),
    },
    {
        "id": "EXC-003",
        "source_refs": ["templates/v2-baseline/.claude/rules/coding-style.md"],
        "classification": "remaining_low_level_style_guidance",
        "rationale": (
            "Unmapped constructor/record/visibility/type-inference/modern-syntax preferences are "
            "low-level style guidance rather than architecture-policy oracle items. Repository "
            "conventions remain authoritative through RUN-009; file/async conventions are now "
            "captured by RUN-024."
        ),
    },
    {
        "id": "EXC-004",
        "source_refs": [
            "templates/v2-baseline/.claude/skills/project-structure/references/backend-layout.md"
        ],
        "classification": "remaining_layout_examples_and_naming_heuristics",
        "rationale": (
            "Illustrative directory trees, type-role suffix suggestions, and local organization "
            "examples are implementation/navigation technique. Architectural boundaries, physical "
            "layout, narrow test references, and DTO-boundary behavior are represented by existing "
            "ARC/DEP policies plus ARC-028 and ARC-029."
        ),
    },
    {
        "id": "EXC-005",
        "source_refs": [
            "templates/v2-baseline/.claude/skills/dependency-injection/SKILL.md"
        ],
        "classification": "optional_di_technique",
        "rationale": (
            "Decorator and assembly-scanning examples are optional technique. Core injection, "
            "lifetime, ownership, and composition policy is represented by ARC-021..ARC-023."
        ),
    },
    {
        "id": "EXC-006",
        "source_refs": ["templates/v2-baseline/.claude/skills/docker/SKILL.md"],
        "classification": "conditional_container_technique",
        "rationale": (
            "Dockerfile shape, Compose examples, health-probe mechanics, and image-size options "
            "are conditional deployment technique. Docker adoption/runtime-image policy is "
            "represented by DEP-018/DEP-019 and health policy by API-018..API-020."
        ),
    },
    {
        "id": "EXC-007",
        "source_refs": ["templates/v2-baseline/.claude/skills/resilience/SKILL.md"],
        "classification": "conditional_resilience_technique",
        "rationale": (
            "Circuit-breaker, hedging, database-retry, and message-delivery examples are "
            "conditional technique. Core timeout/retry/fallback/cancellation semantics are "
            "represented by RUN-015..RUN-019 and DEP-020."
        ),
    },
    {
        "id": "EXC-008",
        "source_refs": ["templates/v2-baseline/.claude/skills/swagger/SKILL.md"],
        "classification": "openapi_tooling_technique",
        "rationale": (
            "Setup snippets, launch-profile examples, metadata syntax, and document partitioning "
            "are tooling technique. Runtime/documentation truth and environment exposure are "
            "represented by API-016/API-017 and DEP-012."
        ),
    },
    {
        "id": "EXC-009",
        "source_refs": ["templates/v2-baseline/.claude/skills/http-api/SKILL.md"],
        "classification": "detailed_http_reference",
        "rationale": (
            "Individual less-common status-code examples and detailed controller snippets remain "
            "reference material. Core success/error/auth/conflict/versioning semantics are "
            "represented by API policies."
        ),
    },
    {
        "id": "EXC-010",
        "source_refs": ["templates/v2-baseline/.claude/skills/health-check/SKILL.md"],
        "classification": "health_check_implementation_technique",
        "rationale": (
            "Tagging, endpoint, topology, and test examples are implementation technique. "
            "Cheap/deterministic checks, liveness/readiness semantics, and safe public output are "
            "represented by API-018..API-020."
        ),
    },
    {
        "id": "EXC-011",
        "source_refs": ["templates/v2-baseline/.claude/skills/ef-core/SKILL.md"],
        "classification": "remaining_ef_core_technique",
        "rationale": (
            "Projection, tracking, include/split-query, interceptor, compiled-query, and raw-SQL "
            "examples are implementation technique or are already covered by architecture, "
            "performance, and security policies. Migration review is now captured by PST-010."
        ),
    },
    {
        "id": "EXC-012",
        "source_refs": [
            "templates/v2-baseline/.claude/skills/testing/SKILL.md",
            "templates/v2-baseline/.claude/rules/testing.md",
        ],
        "classification": "remaining_test_technique",
        "rationale": (
            "Mock/fake choice, builders/fixtures, snapshot-testing examples, and other local test "
            "technique remain outside the oracle. Test level, behavior, isolation, fidelity, "
            "regression, probe preservation, coverage, and naming are represented by TST policies."
        ),
    },
    {
        "id": "EXC-013",
        "source_refs": [
            "templates/v2-baseline/.claude/skills/logging/SKILL.md",
            "templates/v2-baseline/.claude/skills/configuration/SKILL.md",
        ],
        "classification": "operational_technique",
        "rationale": (
            "Correlation implementation, source-generated logging, exact provider precedence, and "
            "options examples are technique. Structured/sensitive logging and typed/validated "
            "configuration are represented by RUN-013/RUN-014/RUN-022 and security policies."
        ),
    },
    {
        "id": "EXC-014",
        "source_refs": ["templates/v2-baseline/.claude/skills/ci-cd/SKILL.md"],
        "classification": "conditional_delivery_technique",
        "rationale": (
            "Artifact-publishing shape, build-once/promote preference, and platform-specific "
            "deployment examples are conditional technique. CI truthfulness, frontend install, "
            "and production migration obligations are represented by WF-017..WF-019."
        ),
    },
    {
        "id": "EXC-015",
        "source_refs": [
            "templates/v2-baseline/.claude/skills/security-scan/SKILL.md",
            "templates/v2-baseline/.claude/skills/security-scan/references/scan-layers.md",
        ],
        "classification": "investigation_heuristics",
        "rationale": (
            "Detailed scan-layer search patterns and false-positive examples are investigative "
            "prompts rather than independent runtime policy. Evidence/severity discipline and "
            "tool independence are represented by WF-020/WF-021; concrete security invariants are "
            "represented by SEC policies."
        ),
    },
    {
        "id": "EXC-016",
        "source_refs": [
            "templates/v2-baseline/.claude/agents/code-reviewer.md",
            "templates/v2-baseline/.claude/skills/code-review/SKILL.md",
        ],
        "classification": "review_routing_and_examples",
        "rationale": (
            "Specialized-skill routing and repeated examples are not separate oracle items. "
            "Independent read-only review, defect prioritization, no manufactured findings, and "
            "risk-scoped verification are represented by WF-010..WF-012 and related policies."
        ),
    },
    {
        "id": "EXC-017",
        "source_refs": [
            "templates/v2-baseline/.claude/skills/project-structure/SKILL.md",
            "templates/v2-baseline/.claude/skills/project-structure/references/solution-layout.md",
        ],
        "classification": "scaffolding_procedure_and_examples",
        "rationale": (
            "Step-by-step scaffolding commands and illustrative directory trees remain workflow "
            "technique. Stack/layout/simplicity/dependency invariants are represented by DEP-022.."
            "DEP-024, ARC-001, ARC-027..ARC-029, and governance policies."
        ),
    },
    {
        "id": "EXC-018",
        "source_refs": ["templates/v2-baseline/.claude/skills/angular/SKILL.md"],
        "classification": "remaining_frontend_technique",
        "rationale": (
            "Component snippets, detailed test targeting, and other Angular implementation "
            "examples remain technique. Structural/state/HTTP/forms/error/RxJS invariants are "
            "represented by FE-001..FE-012 and related security/dependency policies."
        ),
    },
]


SOURCE_REF_REPLACEMENTS = {
    "TST-010": {
        "templates/v2-baseline/.claude/skills/verify/SKILL.md#Preserve Behavioral Verification":
        "templates/v2-baseline/.claude/skills/verify/SKILL.md#4. Preserve Behavioral Verification",
    },
    "WF-004": {
        "templates/v2-baseline/.claude/skills/verify/SKILL.md#Inspect the Change":
        "templates/v2-baseline/.claude/skills/verify/SKILL.md#1. Inspect the Change",
    },
    "WF-005": {
        "templates/v2-baseline/.claude/skills/verify/SKILL.md#Build":
        "templates/v2-baseline/.claude/skills/verify/SKILL.md#2. Build",
    },
    "WF-007": {
        "templates/v2-baseline/.claude/skills/verify/SKILL.md#Architecture Check":
        "templates/v2-baseline/.claude/skills/verify/SKILL.md#5. Architecture Check",
    },
}


SOURCE_REF_ADDITIONS = {
    "GOV-012": [
        "templates/v2-baseline/.claude/rules/architecture.md#Architectural Simplicity",
    ],
    "GOV-013": [
        "templates/v2-baseline/.claude/rules/architecture.md#Architectural Simplicity",
    ],
    "ARC-020": [
        "templates/v2-baseline/.claude/rules/architecture.md#Architectural Simplicity",
    ],
    "API-018": [
        "templates/v2-baseline/.claude/skills/health-check/SKILL.md#Database Health",
    ],
    "API-019": [
        "templates/v2-baseline/.claude/skills/health-check/SKILL.md#Readiness",
        "templates/v2-baseline/.claude/skills/health-check/SKILL.md#Startup Readiness",
    ],
    "TST-007": [
        "templates/v2-baseline/.claude/rules/testing.md#Database Tests",
    ],
    "DEP-010": [
        "templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Logging",
    ],
    "DEP-011": [
        "templates/v2-baseline/.claude/skills/project-structure/references/technology-stack.md#Resilience",
    ],
    "WF-016": [
        "templates/v2-baseline/.claude/skills/angular/SKILL.md#API Client Generation",
    ],
}


WF016_NORMALIZED = (
    "When generated output is wrong or its source contract/configuration changes, fix or update "
    "the authoritative source and regenerate; do not manually patch disposable generated output "
    "unless the repository or generation workflow intentionally treats that output as maintained "
    "source."
)


def flatten_policies(doc: dict[str, Any]) -> list[dict[str, Any]]:
    return [p for g in doc["policygroups"] for p in g["policies"]]


def group_by_id(doc: dict[str, Any], group_id: str) -> dict[str, Any]:
    matches = [g for g in doc["policygroups"] if g["id"] == group_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one policy group {group_id!r}; found {len(matches)}.")
    return matches[0]


def policy_by_id(doc: dict[str, Any], policy_id: str) -> dict[str, Any]:
    matches = [p for p in flatten_policies(doc) if p["id"] == policy_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one policy {policy_id!r}; found {len(matches)}.")
    return matches[0]


def validate_source_v03(doc: dict[str, Any]) -> None:
    if doc.get("schema_version") != EXPECTED_SCHEMA:
        raise ValueError(
            f"Expected schema_version {EXPECTED_SCHEMA}, got {doc.get('schema_version')!r}."
        )
    if doc.get("group_count") != EXPECTED_GROUP_COUNT:
        raise ValueError(
            f"Expected group_count {EXPECTED_GROUP_COUNT}, got {doc.get('group_count')!r}."
        )
    if doc.get("policy_count") != EXPECTED_POLICY_COUNT:
        raise ValueError(
            f"Expected policy_count {EXPECTED_POLICY_COUNT}, got {doc.get('policy_count')!r}."
        )
    if doc.get("baseline_tree_sha") != EXPECTED_BASELINE_TREE_SHA:
        raise ValueError(
            "The inventory is not pinned to the audited V2 baseline tree. "
            f"Expected {EXPECTED_BASELINE_TREE_SHA}, got {doc.get('baseline_tree_sha')!r}."
        )

    policies = flatten_policies(doc)
    if len(policies) != EXPECTED_POLICY_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_POLICY_COUNT} stored policies, found {len(policies)}."
        )

    ids = [p["id"] for p in policies]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate policy IDs exist in source inventory.")

    for pid in REMOVED_RESEARCH_SHARED_IDS:
        p = policy_by_id(doc, pid)
        if p.get("origin") != "research_shared":
            raise ValueError(f"{pid} no longer has origin=research_shared; review manually.")


def replace_source_refs(doc: dict[str, Any]) -> None:
    for pid, replacements in SOURCE_REF_REPLACEMENTS.items():
        p = policy_by_id(doc, pid)
        refs = list(p["source_refs"])
        for old, new in replacements.items():
            if old not in refs:
                raise ValueError(f"{pid}: expected source ref not found: {old}")
            refs[refs.index(old)] = new
        p["source_refs"] = refs


def add_source_refs(doc: dict[str, Any]) -> None:
    for pid, additions in SOURCE_REF_ADDITIONS.items():
        p = policy_by_id(doc, pid)
        refs = list(p["source_refs"])
        for ref in additions:
            if ref not in refs:
                refs.append(ref)
        p["source_refs"] = refs


def remove_research_shared(doc: dict[str, Any]) -> list[dict[str, Any]]:
    moved: list[dict[str, Any]] = []
    for group in doc["policygroups"]:
        kept = []
        for p in group["policies"]:
            if p["id"] in REMOVED_RESEARCH_SHARED_IDS:
                moved.append(copy.deepcopy(p))
            else:
                kept.append(p)
        group["policies"] = kept

    moved_ids = {p["id"] for p in moved}
    expected = set(REMOVED_RESEARCH_SHARED_IDS)
    if moved_ids != expected:
        raise ValueError(f"Moved research-shared IDs {moved_ids}, expected {expected}.")
    return sorted(moved, key=lambda p: p["id"])


def append_additions(doc: dict[str, Any]) -> None:
    existing = {p["id"] for p in flatten_policies(doc)}
    for group_id, additions in ADDITIONS.items():
        group = group_by_id(doc, group_id)
        for p in additions:
            if p["id"] in existing:
                raise ValueError(f"New policy ID already exists: {p['id']}")
            group["policies"].append(copy.deepcopy(p))
            existing.add(p["id"])


def sort_group_policies(doc: dict[str, Any]) -> None:
    def key(p: dict[str, Any]) -> tuple[str, int]:
        m = re.fullmatch(r"([A-Z]+)-(\d+)", p["id"])
        if not m:
            return (p["id"], 0)
        return (m.group(1), int(m.group(2)))

    for group in doc["policygroups"]:
        group["policies"].sort(key=key)


def update_existing_semantics(doc: dict[str, Any]) -> None:
    policy_by_id(doc, "WF-016")["normalized_policy"] = WF016_NORMALIZED


def recompute_counts(doc: dict[str, Any]) -> None:
    for group in doc["policygroups"]:
        group["policy_count"] = len(group["policies"])
    doc["group_count"] = len(doc["policygroups"])
    doc["policy_count"] = len(flatten_policies(doc))


def update_top_level_metadata(doc: dict[str, Any]) -> None:
    doc["schema_version"] = "0.4"
    doc["status"] = "frozen_hidden_post_generation_oracle"
    doc["purpose"] = (
        "Frozen V2-only normative oracle for post-generation validation of M/L0/L1/K0/K1. "
        "Candidate-construction Claude must not see this file; generation uses the frozen "
        "V2 baseline as the visible source of truth, while this inventory is revealed only "
        "during evaluation."
    )

    principles = doc["principles"]
    principles["one_normative_owner"] = (
        "Every policy ID must have exactly one authoritative owner in each experimental candidate."
    )
    principles["content_equivalence"] = (
        "All experimental candidates are evaluated against the same normalized V2 policy semantics. "
        "Candidate generation starts from the same frozen V2 baseline, not from this oracle."
    )
    principles["source_traceability"] = (
        "Every policy in this oracle is V2-derived and retains source_refs into the frozen baseline."
    )
    principles.pop("research_shared", None)
    principles["v2_only"] = (
        "Every policy in this oracle has origin=v2. Research-introduced shared requirements are "
        "stored separately and are not scored as V2 policy preservation."
    )
    principles["hidden_oracle"] = (
        "The candidate-construction model and benchmark-execution model must not receive this "
        "inventory or derived policy lists before their outputs are frozen."
    )
    principles["single_storage"] = (
        "A policy appears in exactly one policygroups[].policies array. Cross-topic relationships "
        "use related_groups rather than duplication."
    )

    coverage = doc["coverage_policy"]
    coverage["inventory_role"] = "hidden_post_generation_normative_oracle"
    coverage["includes"] = (
        "Stable V2-derived normative statements, defaults, prohibitions, approved technology "
        "decisions, approval gates, and workflow obligations whose loss or semantic drift would "
        "materially change candidate behavior."
    )
    coverage["excludes"] = (
        "Research-introduced requirements, pure examples, explanatory prose, code samples, optional "
        "technique, troubleshooting detail, and private knowledge that does not itself impose a "
        "material normative requirement."
    )
    coverage["source_file_coverage_rule"] = (
        "A V2 file may legitimately have zero policy references when it contains only product input, "
        "examples, or technique. Material normative statements must map to an inventory policy; "
        "audited borderline/technique material is recorded in intentional_non_oracle_material."
    )
    coverage["candidate_visibility"] = "forbidden"
    coverage["benchmark_execution_visibility"] = "forbidden"
    coverage["evaluation_visibility"] = "required"
    coverage["validation_usage"] = (
        "After candidate generation is frozen, compare candidate runtime instructions to this "
        "oracle for missing owners, duplicate owners, semantic weakening/strengthening, and "
        "unapproved additional normative policy."
    )

    doc["intentional_non_oracle_material"] = copy.deepcopy(INTENTIONAL_NON_ORACLE_MATERIAL)


def validate_v04(doc: dict[str, Any]) -> None:
    if doc["schema_version"] != "0.4":
        raise ValueError("Output schema_version must be 0.4.")
    if doc["group_count"] != EXPECTED_GROUP_COUNT:
        raise ValueError("Group count changed unexpectedly.")
    if doc["policy_count"] != 194:
        raise ValueError(f"Expected 194 policies after audit, got {doc['policy_count']}.")

    policies = flatten_policies(doc)
    ids = [p["id"] for p in policies]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate policy IDs exist in v0.4 output.")

    origins = {p.get("origin") for p in policies}
    if origins != {"v2"}:
        raise ValueError(f"Hidden V2 oracle must contain only origin=v2; got {origins}.")

    for p in policies:
        refs = p.get("source_refs") or []
        if not refs:
            raise ValueError(f"{p['id']} has no source_refs.")
        non_v2 = [r for r in refs if not r.startswith("templates/v2-baseline/")]
        if non_v2:
            raise ValueError(f"{p['id']} has non-V2 source_refs: {non_v2}")

    for pid in REMOVED_RESEARCH_SHARED_IDS:
        if pid in ids:
            raise ValueError(f"{pid} must not remain in the V2-only oracle.")


def normalize_heading(text: str) -> str:
    return text.replace("`", "").strip()


def validate_source_refs_against_repo(doc: dict[str, Any], repo_root: Path) -> None:
    missing_paths: list[str] = []
    missing_anchors: list[str] = []

    cache: dict[Path, set[str]] = {}

    for p in flatten_policies(doc):
        for ref in p["source_refs"]:
            if "#" in ref:
                rel, heading = ref.split("#", 1)
            else:
                rel, heading = ref, None

            path = repo_root / rel
            if not path.is_file():
                missing_paths.append(f"{p['id']}: {ref}")
                continue

            if heading is None:
                continue

            if path not in cache:
                content = path.read_text(encoding="utf-8")
                headings = set()
                for line in content.splitlines():
                    m = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
                    if m:
                        headings.add(normalize_heading(m.group(1)))
                cache[path] = headings

            if normalize_heading(heading) not in cache[path]:
                missing_anchors.append(f"{p['id']}: {ref}")

    if missing_paths or missing_anchors:
        details = []
        if missing_paths:
            details.append("Missing source files:\n  " + "\n  ".join(missing_paths))
        if missing_anchors:
            details.append("Missing Markdown headings:\n  " + "\n  ".join(missing_anchors))
        raise ValueError("\n\n".join(details))


def build_shared_research_file(moved: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "status": "shared_construction_constraints",
        "purpose": (
            "Research-introduced requirements applied equally to candidate construction but excluded "
            "from the V2 policy-preservation oracle because they are not derived from V2."
        ),
        "visibility": {
            "candidate_construction": (
                "May be expressed through the common TASK/CANDIDATE construction contract."
            ),
            "v2_policy_evaluation": "excluded",
        },
        "invariants": moved,
    }


def build(source: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_source_v03(source)
    doc = copy.deepcopy(source)

    moved = remove_research_shared(doc)
    replace_source_refs(doc)
    add_source_refs(doc)
    update_existing_semantics(doc)
    append_additions(doc)
    sort_group_policies(doc)
    update_top_level_metadata(doc)
    recompute_counts(doc)
    validate_v04(doc)

    return doc, build_shared_research_file(moved)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Root of ClaudeArchitectureResearch (default: current directory).",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Source inventory path. Default: <repo-root>/research/policy/inventory.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path. Default: <repo-root>/research/policy/inventory.v0.4.proposed.json",
    )
    parser.add_argument(
        "--shared-output",
        type=Path,
        default=None,
        help=(
            "Output path for moved research-shared invariants. Default: "
            "<repo-root>/research/policy/shared-research-invariants.proposed.json"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    source_path = (
        args.source.resolve()
        if args.source is not None
        else repo_root / "research/policy/inventory.json"
    )
    output_path = (
        args.output.resolve()
        if args.output is not None
        else repo_root / "research/policy/inventory.v0.4.proposed.json"
    )
    shared_output_path = (
        args.shared_output.resolve()
        if args.shared_output is not None
        else repo_root / "research/policy/shared-research-invariants.proposed.json"
    )

    source = json.loads(source_path.read_text(encoding="utf-8"))
    revised, shared = build(source)

    # Validate every policy source reference against the local frozen baseline.
    validate_source_refs_against_repo(revised, repo_root)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    shared_output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(revised, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    shared_output_path.write_text(
        json.dumps(shared, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote: {output_path}")
    print(f"Wrote: {shared_output_path}")
    print(f"Policy count: {revised['policy_count']}")
    print("Origins: v2 only")
    print("Source-reference validation: PASS")
    print("Candidate visibility: forbidden")


if __name__ == "__main__":
    main()
