import json
import os
import pandas as pd

class SplunkConnector:
    """
    Handles connections to the Splunk REST API.
    Can operate in Mock Mode for hackathon demonstrations without a live server.
    """
    def __init__(self, use_mock=True):
        self.use_mock = use_mock
        self.mock_data_path = os.path.join(os.path.dirname(__file__), '..', 'mock_data', 'sample_alerts.json')

    def get_alerts(self):
        """Fetches high-severity alerts from Splunk."""
        if self.use_mock:
            with open(self.mock_data_path, 'r') as f:
                return json.load(f)
        else:
            # Real implementation would use requests.get() against Splunk REST API endpoints
            # e.g., /services/search/jobs/export with search="index=_internal log_level=ERROR"
            pass

    def run_spl_query(self, spl_query):
        """Executes an SPL query and returns a pandas dataframe of results."""
        if self.use_mock:
            # Return dummy dataframe that looks like Splunk search results
            data = {
                "_time": ["2026-06-15 08:21:10", "2026-06-15 08:21:12", "2026-06-15 08:23:10", "2026-06-15 08:23:11"],
                "EventCode": [4625, 4625, 4624, 4104],
                "user": ["service_admin", "service_admin", "service_admin", "service_admin"],
                "Message": ["Failed Login", "Failed Login", "Successful Login", "Creating Scriptblock text (PowerShell)"]
            }
            return pd.DataFrame(data)
        else:
            # Real implementation using Splunk SDK or REST API
            pass