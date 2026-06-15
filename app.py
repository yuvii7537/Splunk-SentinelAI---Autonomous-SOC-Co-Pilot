import streamlit as st
import time
import os
from ai_agent import SecurityAgent
from splunk_connector import SplunkConnector

# Setup Page Configuration
st.set_page_config(page_title="Splunk SentinelAI", page_icon="🛡️", layout="wide")

# Initialize modules
use_mock = os.getenv("USE_MOCK_DATA", "True").lower() == "true"
splunk = SplunkConnector(use_mock=use_mock)
ai_agent = SecurityAgent(use_mock=use_mock)

# --- THE FIX: SESSION STATE ---
# This forces Streamlit to remember what we clicked!
if 'selected_alert' not in st.session_state:
    st.session_state.selected_alert = None
if 'investigating' not in st.session_state:
    st.session_state.investigating = False

# Header
st.title("🛡️ Splunk SentinelAI")
st.markdown("### Autonomous SOC Co-Pilot powered by Splunk AI")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://www.vectorlogo.zone/logos/splunk/splunk-icon.svg", width=80)
    st.markdown("## System Status")
    st.success("Splunk Connection: Online" if not use_mock else "Splunk Connection: MOCK MODE")
    st.success("AI Engine: Active")
    st.markdown("---")
    st.markdown("### Triage Queue")
    
    # Load alerts
    alerts = splunk.get_alerts()
    
    for alert in alerts:
        # If a sidebar button is clicked, save it to session state
        if st.button(f"🔴 {alert['id']} - {alert['host']}", key=alert['id'], help=alert['title'], use_container_width=True):
            st.session_state.selected_alert = alert
            st.session_state.investigating = False  # Reset investigation when a new alert is picked

# Main Panel
if not st.session_state.selected_alert:
    st.info("👈 Select an alert from the Triage Queue to begin AI-assisted investigation.")
    
    # Dashboard metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Open Alerts", len(alerts))
    col2.metric("Mean Time to Triage (MTTT)", "45s", "-90%")
    col3.metric("AI Auto-Resolutions", "12", "+3")

else:
    # Retrieve the saved alert from state
    alert = st.session_state.selected_alert
    st.subheader(f"Alert Details: {alert['id']}")
    
    # Display Alert Info
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Severity", alert['severity'])
    col2.metric("Host", alert['host'])
    col3.metric("User", alert['user'])
    col4.metric("Timestamp", alert['timestamp'])
    
    st.code(f"Title: {alert['title']}\nDescription: {alert['description']}", language="text")
    
    # When "Investigate" is clicked, save THAT to session state
    if st.button("🤖 Investigate with SentinelAI", type="primary"):
        st.session_state.investigating = True

    # If we are investigating, show the tabs!
    if st.session_state.investigating:
        with st.spinner("SentinelAI is analyzing the alert payload..."):
            time.sleep(1.5) # Simulate API latency
            
            # Step 1: AI Analysis
            analysis = ai_agent.analyze_alert(alert)
            st.success("Analysis Complete!")
            
            # Display Tabs
            tab1, tab2, tab3 = st.tabs(["🧠 AI Summary & IoCs", "🔍 Generated SPL & Logs", "🛠️ Remediation Playbook"])
            
            with tab1:
                st.markdown("### Plain-English Threat Summary")
                st.write(analysis["summary"])
                
                st.markdown("### Extracted Indicators of Compromise (IoCs)")
                for ioc in analysis["iocs"]:
                    st.markdown(f"- `{ioc}`")
            
            with tab2:
                st.markdown("### Splunk AI Generated SPL Query")
                st.markdown("SentinelAI automatically generated this query to identify the blast radius around the compromised host.")
                st.code(analysis["spl_query"], language="sql")
                
                st.markdown("### Surrounding Log Context (Blast Radius)")
                # Simulate running the SPL query
                logs = splunk.run_spl_query(analysis["spl_query"])
                st.dataframe(logs)
                
            with tab3:
                st.markdown("### Recommended Remediation Playbook")
                for step in analysis["playbook"]:
                    st.markdown(f"✅ {step}")
                
                st.markdown("---")
                st.markdown("### Automated Actions")
                colA, colB = st.columns(2)
                if colA.button("🚫 Isolate Host via SOAR", use_container_width=True, key="isolate"):
                    st.error(f"Host {alert['host']} has been isolated.")
                if colB.button("🔒 Suspend User Account", use_container_width=True, key="suspend"):
                    st.warning(f"User {alert['user']} has been suspended.")
