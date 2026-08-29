import unittest

from app import authorize, retrieve


class AgentLabTests(unittest.TestCase):
    def test_retrieval_never_crosses_tenant(self):
        self.assertEqual([m["id"] for m in retrieve("acme", "refund")], ["m1", "m2"])

    def test_high_impact_action_needs_approval(self):
        decision = authorize("refund", "acme", "acme", amount=75)
        self.assertEqual(decision.status, "needs_approval")

    def test_cross_tenant_action_denies(self):
        decision = authorize("read", "other", "acme")
        self.assertEqual(decision.status, "deny")


if __name__ == "__main__":
    unittest.main()
