import unittest

from scripts.scan_secrets import find_secret_findings


class SecretScannerTests(unittest.TestCase):
    def test_detects_aws_access_key_id_shape(self) -> None:
        findings = find_secret_findings("key = AKIA1234567890ABCDEF", "sample.txt")  # secret-scan: allow-test-fixture
        self.assertTrue(findings)

    def test_detects_private_key_header(self) -> None:
        findings = find_secret_findings("-----BEGIN PRIVATE KEY-----", "sample.pem")  # secret-scan: allow-test-fixture
        self.assertTrue(findings)

    def test_ignores_documented_variable_names_without_values(self) -> None:
        text = "AWS_ACCESS_KEY_ID\nAWS_SECRET_ACCESS_KEY\nAWS_SESSION_TOKEN"
        findings = find_secret_findings(text, "SECURITY.md")
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
