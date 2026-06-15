import pandas as pd

class SplunkConnector:
    """
    Handles connections to the Splunk REST API.
    Operates in Mock Mode for hackathon demonstrations.
    """
    def __init__(self, use_mock=True):
        self.use_mock = use_mock

    def get_alerts(self):
        """Fetches high-severity alerts from Splunk."""
        return [
          {
            "id": "SPL-9902",
            "timestamp": "2026-06-15T08:23:11Z",
            "title": "Suspicious PowerShell Execution after Failed Logins",
            "severity": "CRITICAL",
            "host": "prod-db-04",
            "user": "service_admin",
            "status": "New",
            "description": "Multiple failed SSH/RDP attempts followed by successful login and immediate execution of Base64 encoded PowerShell."
          },
          {
            "id": "SPL-9903",
            "timestamp": "2026-06-15T09:15:42Z",
            "title": "Unusual Volume of Data Exfiltration",
            "severity": "HIGH",
            "host": "file-srv-01",
            "user": "m.smith",
            "status": "New",
            "description": "Anomalous outbound traffic volume (50GB+) detected over port 443 to an unknown external IP address."
          },
          {
            "id": "SPL-9904",
            "timestamp": "2026-06-15T10:05:00Z",
            "title": "Privilege Escalation Anomaly",
            "severity": "HIGH",
            "host": "auth-node-02",
            "user": "j.doe",
            "status": "New",
            "description": "Standard user added to local Administrators group outside of approved change window."
          }
        ]

    def run_spl_query(self, spl_query):
        """Executes an SPL query and returns a pandas dataframe of results."""
        data = {
            "_time": ["2026-06-15 08:21:10", "2026-06-15 08:21:12", "2026-06-15 08:23:10", "2026-06-15 08:23:11"],
            "EventCode": [4625, 4625, 4624, 4104],
            "user": ["service_admin", "service_admin", "service_admin", "service_admin"],
            "Message": ["Failed Login", "Failed Login", "Successful Login", "Creating Scriptblock text (PowerShell)"]
        }
        return pd.DataFrame(data)
