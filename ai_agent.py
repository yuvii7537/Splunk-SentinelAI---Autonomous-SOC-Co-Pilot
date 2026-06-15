import time

class SecurityAgent:
    """
    Simulates the AI capabilities (e.g. Splunk AI Assistant / External LLM integration)
    to parse alerts, generate SPL, and create playbooks.
    """
    def __init__(self, use_mock=True):
        self.use_mock = use_mock

    def analyze_alert(self, alert_data):
        """
        Takes raw alert data and returns a structured AI analysis including:
        - Plain English Summary
        - Extracted IoCs
        - Generated SPL Query to investigate further
        - Step-by-step remediation playbook
        """
        if self.use_mock:
            # Simulated AI response logic
            return self._mock_analysis(alert_data)
        else:
            # Here you would implement calls to Splunk AI API or OpenAI/LangChain
            # e.g., prompt = f"Analyze this Splunk alert: {alert_data}"
            raise NotImplementedError("Live LLM integration requires API keys. Run in Mock Mode.")

    def _mock_analysis(self, alert):
        # Generate dynamic responses based on the mock alert data
        host = alert.get("host", "Unknown")
        user = alert.get("user", "Unknown")
        
        return {
            "summary": f"The system detected an anomaly on host '{host}'. User '{user}' experienced multiple failed authentication attempts, immediately followed by a successful login and execution of an obfuscated payload. This matches the MITRE ATT&CK T1059.001 (PowerShell) pattern.",
            "iocs": [
                f"Host: {host}",
                f"User: {user}",
                "IP: 192.168.1.104",
                "Hash: 8743b52063cd84097a65d1633f5c74f5"
            ],
            "spl_query": f"index=main sourcetype=WinEventLog:Security host={host} \n| transaction user maxspan=15m \n| search EventCode=4625 OR EventCode=4624 OR EventCode=4104 \n| table _time, EventCode, user, host, Message",
            "playbook": [
                f"1. **Containment:** Immediately isolate host `{host}` from the production network.",
                f"2. **Identity Protection:** Force a password reset and revoke active sessions for user `{user}`.",
                "3. **Eradication:** Run an endpoint AV scan to remove the obfuscated PowerShell script.",
                "4. **Investigation:** Review firewall logs for outbound C2 traffic originating from `192.168.1.104`."
            ]
        }