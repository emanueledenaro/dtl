"""Unit tests for scripts/dtl_engine.py — run in CI, no model required.

Usage: python -m unittest discover -s tests -p "test_*.py"
Requires: pip install tiktoken
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from dtl_engine import compress_text, compress_json, mine_codebook, tcount


class TestCompressText(unittest.TestCase):
    def test_removes_fillers_and_rewrites_phrases(self):
        src = "Could you please make sure that the deployment runs as soon as possible? Thank you!"
        out = compress_text(src)
        self.assertIn("ensure", out)
        self.assertIn("immediately", out)
        self.assertNotIn("please", out.lower())
        self.assertNotIn("thank", out.lower())

    def test_saves_tokens(self):
        src = ("I would like you to basically just refactor this module in order to "
               "make sure that it is able to handle errors, if possible, thanks in advance.")
        out = compress_text(src)
        self.assertLess(tcount(out), tcount(src))

    def test_preserves_numbers_and_units(self):
        out = compress_text("The rate limit is 1,000,000 requests per 60 seconds.")
        self.assertIn("1000000", out)
        self.assertIn("60 seconds", out)

    def test_preserves_negations(self):
        out = compress_text("Please do not delete the production database.")
        self.assertIn("not delete", out)


class TestCompressJson(unittest.TestCase):
    def test_records_to_toon(self):
        payload = ('{"users":[{"user_id":1,"name":"Ada","created_at":"2026-01-01T12:00:00Z"},'
                   '{"user_id":2,"name":"Bob","created_at":"2026-01-02T08:30:00Z"}]}')
        out = compress_json(payload)
        self.assertTrue(out.startswith("users[2]{"))
        self.assertIn("2026-01-01", out)
        self.assertNotIn("12:00:00", out)  # time stripped from ISO timestamps
        self.assertLess(tcount(out), tcount(payload))

    def test_single_object_minified(self):
        out = compress_json('{"name": "Ada", "role": "admin"}')
        self.assertEqual(out, '{"name":"Ada","role":"admin"}')


class TestMineCodebook(unittest.TestCase):
    def test_extracts_macro_from_repetitive_corpus(self):
        base = ("Parse the trading signal from the following text and output csv with "
                "pair, direction, entry, stop loss and take profits: ")
        prompts = [base + tail for tail in ("BTCUSDT long 64k", "ETHUSDT short 3.2k",
                                            "SOLUSDT long 140", "XRPUSDT short 0.52")]
        book, compressed, macros = mine_codebook(prompts)
        self.assertGreaterEqual(len(macros), 1)
        self.assertTrue(book.startswith("CODEBOOK:"))
        before = sum(tcount(p) for p in prompts)
        after = sum(tcount(p) for p in compressed)
        self.assertLess(after, before)


if __name__ == "__main__":
    unittest.main()
