from __future__ import annotations

import json
import re
from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ..schemas import AgentCandidate, Capability
from .base import DiscoveryAdapter

JsonTransport = Callable[[str, float], dict[str, Any]]


def _http_json(url: str, timeout: float) -> dict[str, Any]:
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "agent-builder-lab/0.1"})
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - URL is explicit adapter configuration
        return json.loads(response.read().decode("utf-8"))


def _terms(value: str) -> set[str]:
    return {term for term in re.split(r"[^a-z0-9]+", value.lower()) if len(term) > 2}


class AgntcyDirectoryAdapter(DiscoveryAdapter):
    """Read AGNTCY Directory's AI Catalog/ARD HTTP surface.

    Matching is intentionally conservative and inspectable: exact OASF tag matches
    rank above lexical overlap. Returned records remain unverified claims.
    """

    name = "agntcy-directory"

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        *,
        page_size: int = 100,
        max_records: int = 100,
        max_candidates: int = 20,
        timeout: float = 5.0,
        transport: JsonTransport = _http_json,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.page_size = min(max(page_size, 1), 100)
        self.max_records = max(max_records, 1)
        self.max_candidates = max(max_candidates, 1)
        self.timeout = timeout
        self._transport = transport
        self.last_scan_truncated = False

    def _records(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        token: str | None = None
        self.last_scan_truncated = False
        while True:
            params: dict[str, str | int] = {"page_size": self.page_size}
            if token:
                params["page_token"] = token
            payload = self._transport(f"{self.base_url}/v1/agents?{urlencode(params)}", self.timeout)
            page = payload.get("results", payload.get("agents", []))
            if not isinstance(page, list):
                raise ValueError("AGNTCY response must contain a results or agents list")
            records.extend(item for item in page if isinstance(item, dict))
            token = payload.get("nextPageToken") or payload.get("next_page_token")
            if len(records) >= self.max_records:
                self.last_scan_truncated = bool(token) or len(records) > self.max_records
                return records[:self.max_records]
            if not token:
                return records

    def discover(self, capability: Capability) -> tuple[AgentCandidate, ...]:
        wanted = _terms(f"{capability.id} {capability.description}")
        matches: list[tuple[int, AgentCandidate]] = []
        for record in self._records():
            tags = tuple(str(tag) for tag in record.get("tags", []))
            searchable = " ".join([
                str(record.get("displayName", "")), str(record.get("description", "")), *tags
            ])
            exact = capability.id in tags or any(tag.endswith(f"/{capability.id}") for tag in tags)
            overlap = wanted.intersection(_terms(searchable))
            if not exact and not overlap:
                continue
            identifier = str(record.get("identifier", ""))
            media_type = str(record.get("mediaType", "application/octet-stream"))
            trust = record.get("trustManifest") if isinstance(record.get("trustManifest"), dict) else {}
            score = 2 if exact else 1
            confidence = 0.75 if exact else min(0.25 + 0.05 * len(overlap), 0.50)
            matches.append((score, AgentCandidate(
                id=identifier or str(record.get("displayName", "unnamed")),
                name=str(record.get("displayName", identifier or "Unnamed AGNTCY record")),
                capabilities=tags,
                source=self.name,
                interface=media_type,
                endpoint=self._endpoint(record),
                claim_confidence=confidence,
                evidence_refs=(f"{self.base_url}/v1/agents/{identifier}",) if identifier else (),
                metadata={
                    "identifier": identifier,
                    "media_type": media_type,
                    "description": record.get("description"),
                    "version": record.get("version"),
                    "tags": list(tags),
                    "trust_manifest": {
                        "identity": trust.get("identity"),
                        "identity_type": trust.get("identityType"),
                        "attestation_count": len(trust.get("attestations", [])),
                        "provenance_count": len(trust.get("provenance", [])),
                        "signature_present": bool(trust.get("signature")),
                    },
                    "match": "exact-oasf-tag" if exact else "lexical",
                    "matched_terms": sorted(overlap),
                    "catalog_scan_truncated": self.last_scan_truncated,
                },
            )))
        ranked = sorted(matches, key=lambda item: (-item[0], -item[1].claim_confidence, item[1].id))
        return tuple(candidate for _, candidate in ranked[:self.max_candidates])

    @staticmethod
    def _endpoint(record: dict[str, Any]) -> str | None:
        data = record.get("data")
        if not isinstance(data, dict):
            return None
        for key in ("url", "endpoint", "transport"):
            value = data.get(key)
            if isinstance(value, str):
                return value
        return None
