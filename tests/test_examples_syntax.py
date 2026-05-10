"""Stdlib-only tests for openterms-examples."""
import ast
import json
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(ROOT, "examples")
FIXTURES = os.path.join(ROOT, "fixtures")
EXAMPLE_FILES = ["core_sdk_minimal.py","core_sdk_fail_closed.py","langchain_guarded_tool.py","crewai_permission_check.py","permissive_opt_in.py","mock_openterms_json.py"]
FIXTURE_FILES = ["allow.json","deny.json","not_specified.json","conditional.json"]
CANONICAL_KEYS = ["read_content","scrape_data","api_access","create_account","make_purchases","post_content","allow_training"]
LIVE_NETWORK_PATTERNS = [r"\\brequests\\.get\\b", r"\\brequests\\.post\\b", r"\\bhttpx\\.get\\b", r"\\bhttpx\\.post\\b", r"\\burllib\\.request\\.urlopen\\b", r"\\bsocket\\.connect\\b", r"\\baiohttp\\.ClientSession\\b"]
FORBIDDEN_PHRASES = ["official integration","certified","certification","compliance","verifiable compliance","tamper-evident","audit trail","non-repudiation","endorsed","partner","validated by crewai","validated by langchain","legal determination","professional advice","authoritative interpretation"," ors "]

class TestFiles(unittest.TestCase):
    def test_examples_exist_and_parse(self):
        for fn in EXAMPLE_FILES:
            path = os.path.join(EXAMPLES, fn)
            self.assertTrue(os.path.isfile(path), fn)
            with open(path) as f:
                src = f.read()
            ast.parse(src)
            lower = src.lower()
            for phrase in FORBIDDEN_PHRASES:
                self.assertNotIn(phrase, lower, f"{phrase} in {fn}")
            for pattern in LIVE_NETWORK_PATTERNS:
                self.assertIsNone(re.search(pattern, src), f"{pattern} in {fn}")

    def test_fixtures_valid(self):
        expected = {"allow.json": "allowed", "deny.json": "denied", "not_specified.json": "not_specified", "conditional.json": "conditional"}
        for fn, status in expected.items():
            path = os.path.join(FIXTURES, fn)
            self.assertTrue(os.path.isfile(path), fn)
            with open(path) as f:
                data = json.load(f)
            self.assertTrue({"version","service","last_updated","permissions"} <= set(data))
            for key in CANONICAL_KEYS:
                self.assertIn(key, data["permissions"])
                self.assertEqual(data["permissions"][key]["status"], status)

class TestFailClosedLogic(unittest.TestCase):
    def decision(self, status: str) -> str:
        return "allow" if status == "allowed" else ("deny" if status == "denied" else "not_specified")
    def permitted(self, decision: str, permissive: bool = False) -> bool:
        if decision == "deny":
            return False
        if decision == "allow":
            return True
        return permissive
    def test_strict(self):
        self.assertTrue(self.permitted(self.decision("allowed")))
        self.assertFalse(self.permitted(self.decision("denied")))
        self.assertFalse(self.permitted(self.decision("not_specified")))
        self.assertFalse(self.permitted(self.decision("conditional")))
    def test_permissive(self):
        self.assertFalse(self.permitted(self.decision("denied"), True))
        self.assertTrue(self.permitted(self.decision("not_specified"), True))

if __name__ == "__main__":
    unittest.main(verbosity=2)
