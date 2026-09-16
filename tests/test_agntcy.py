import unittest

from agent_builder_lab.discovery import AgntcyDirectoryAdapter
from agent_builder_lab.schemas import Capability


class AgntcyAdapterTests(unittest.TestCase):
    def test_maps_and_ranks_exact_oasf_tag_above_lexical_match(self) -> None:
        pages = [{
            "results": [
                {
                    "identifier": "urn:lexical",
                    "displayName": "Evidence research helper",
                    "mediaType": "application/a2a-agent-card+json",
                    "description": "Researches public evidence",
                    "tags": [],
                    "data": {"url": "https://example.test/a2a"},
                },
                {
                    "identifier": "urn:exact",
                    "displayName": "OASF Researcher",
                    "mediaType": "application/mcp-server-card+json",
                    "description": "Structured discovery record",
                    "version": "1.0.0",
                    "tags": ["oasf:1.1.0:skills/research.web"],
                    "trustManifest": {"identity": "did:example:publisher"},
                },
            ]
        }]

        def transport(url: str, timeout: float):
            self.assertIn("/v1/agents?page_size=100", url)
            self.assertEqual(5.0, timeout)
            return pages[0]

        adapter = AgntcyDirectoryAdapter("http://directory.test", transport=transport)
        candidates = adapter.discover(Capability("research.web", "Research public evidence"))
        self.assertEqual(["urn:exact", "urn:lexical"], [item.id for item in candidates])
        self.assertEqual("exact-oasf-tag", candidates[0].metadata["match"])
        self.assertEqual("did:example:publisher", candidates[0].metadata["trust_manifest"]["identity"])
        self.assertEqual("https://example.test/a2a", candidates[1].endpoint)

    def test_follows_both_ard_page_token_spellings(self) -> None:
        urls: list[str] = []

        def transport(url: str, timeout: float):
            urls.append(url)
            if len(urls) == 1:
                return {"results": [], "next_page_token": "next one"}
            return {"results": []}

        adapter = AgntcyDirectoryAdapter("http://directory.test", page_size=20, transport=transport)
        self.assertEqual((), adapter.discover(Capability("nothing", "No match")))
        self.assertIn("page_token=next+one", urls[1])

    def test_rejects_malformed_response(self) -> None:
        adapter = AgntcyDirectoryAdapter("http://directory.test", transport=lambda _url, _timeout: {"results": {}})
        with self.assertRaises(ValueError):
            adapter.discover(Capability("x", "x"))

    def test_bounds_catalog_scan_and_marks_partial_evidence(self) -> None:
        record = {
            "identifier": "urn:exact",
            "displayName": "Exact",
            "description": "Exact capability",
            "tags": ["oasf:1.1.0:skills/capability.exact"],
        }
        adapter = AgntcyDirectoryAdapter(
            "http://directory.test", max_records=1,
            transport=lambda _url, _timeout: {"results": [record], "nextPageToken": "more"},
        )
        candidates = adapter.discover(Capability("capability.exact", "Exact capability"))
        self.assertTrue(adapter.last_scan_truncated)
        self.assertTrue(candidates[0].metadata["catalog_scan_truncated"])


if __name__ == "__main__":
    unittest.main()
