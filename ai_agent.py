class SecurityAgent:
    """
    Simulates the AI capabilities to parse alerts, generate SPL, and create playbooks.
    """
    def __init__(self, use_mock=True):
        self.use_mock = use_mock

    def analyze_alert(self, alert_data):
        if self.use_mock:
            return self._mock_analysis(alert_data)
        else:
            raise NotImplementedError("Live LLM integration requires API keys. Run in Mock Mode.")

    def _mock_analysis(self, alert):
        host = alert.get("host", "Unknown")
        user = alert.get("user", "Unknown")
        
        return {
            "summary": f"The system detected an anomaly on host '{host}'. User '{user}' experienced multiple failed authentication attempts, immediately followed by a successful login and execution of an obfuscated payload.",
            "confidence_score": 94,
            "mitre_tactics": ["T1059.001 - PowerShell", "T1078 - Valid Accounts", "T1105 - Ingress Tool Transfer"],
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
                "3. **Eradication:** Run an endpoint AV scan to remove the obfuscated script.",
                "4. **Investigation:** Review firewall logs for outbound C2 traffic."
            ]
        }

    def chat_response(self, user_prompt, alert_id):
        """Generates dynamic AI chat responses for the SOC Analyst."""
        prompt = user_prompt.lower()
        if "ip" in prompt or "192" in prompt:
            return "The IP `192.168.1.104` is an internal staging server, but I noticed it is currently communicating over port 443 with an unregistered external domain in Russia. I recommend blocking this IP at the firewall immediately."
        elif "spl" in prompt or "search" in prompt:
            return "Sure! Here is an SPL query to investigate further: \n`index=firewall src_ip=\"192.168.1.104\" | stats count by dest_ip, dest_port`"
        elif "user" in prompt or "who" in prompt:
            return "This user account has standard privileges, but the recent logs show an attempt to escalate to local admin. Active directory logs confirm the password was brute-forced."
        else:
            return f"Based on the telemetry for alert {alert_id}, I recommend isolating the host. Would you like me to execute the SOAR playbook for you?"
