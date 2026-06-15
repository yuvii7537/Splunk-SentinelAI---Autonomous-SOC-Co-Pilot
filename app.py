import streamlit as st
import time
import os
from ai_agent import SecurityAgent
from splunk_connector import SplunkConnector

st.set_page_config(page_title="Splunk SentinelAI", page_icon="🛡️", layout="wide")

use_mock = os.getenv("USE_MOCK_DATA", "True").lower() == "true"
splunk = SplunkConnector(use_mock=use_mock)
ai_agent = SecurityAgent(use_mock=use_mock)

if 'selected_alert' not in st.session_state:
    st.session_state.selected_alert = None
if 'investigating' not in st.session_state:
    st.session_state.investigating = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("🛡️ Splunk SentinelAI")
st.markdown("### Autonomous SOC Co-Pilot powered by Splunk AI")
st.markdown("---")

with st.sidebar:
    st.image("https://www.vectorlogo.zone/logos/splunk/splunk-icon.svg", width=80)
    st.markdown("## System Status")
    st.success("Splunk Connection: Online" if not use_mock else "Splunk Connection: MOCK MODE")
    st.success("AI Engine: Active")
    st.markdown("---")
    st.markdown("### Triage Queue")
    
    alerts = splunk.get_alerts()
    for alert in alerts:
        if st.button(f"🔴 {alert['id']} - {alert['host']}", key=alert['id'], help=alert['title'], use_container_width=True):
            st.session_state.selected_alert = alert
            st.session_state.investigating = False
            st.session_state.chat_history = [{"role": "assistant", "content": f"Hello! I am SentinelAI. How can I help you investigate alert {alert['id']}?"}]

if not st.session_state.selected_alert:
    st.info("👈 Select an alert from the Triage Queue to begin AI-assisted investigation.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Open Alerts", len(alerts))
    col2.metric("Mean Time to Triage (MTTT)", "45s", "-90%")
    col3.metric("AI Auto-Resolutions", "12", "+3")

else:
    alert = st.session_state.selected_alert
    st.subheader(f"Alert Details: {alert['id']}")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Severity", alert['severity'])
    col2.metric("Host", alert['host'])
    col3.metric("User", alert['user'])
    col4.metric("Timestamp", alert['timestamp'])
    
    st.code(f"Title: {alert['title']}\nDescription: {alert['description']}", language="text")
    
    if st.button("🤖 Investigate with SentinelAI", type="primary"):
        st.session_state.investigating = True

    if st.session_state.investigating:
        with st.spinner("SentinelAI is parsing logs and mapping MITRE tactics..."):
            time.sleep(1.5) 
            analysis = ai_agent.analyze_alert(alert)
            
            # --- NEW FEATURE: AI Confidence Score ---
            st.markdown(f"**AI Threat Confidence Score:** `{analysis['confidence_score']}%`")
            st.progress(analysis['confidence_score'] / 100.0)
            st.write("")
            
            # Display Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🧠 AI Summary & IoCs", "🔍 Generated SPL", "🛠️ Remediation", "💬 Chat with Copilot"])
            
            with tab1:
                st.markdown("### Plain-English Threat Summary")
                st.write(analysis["summary"])
                
                # --- NEW FEATURE: MITRE Mapping ---
                st.markdown("### 🎯 MITRE ATT&CK Framework Mapping")
                for tactic in analysis["mitre_tactics"]:
                    st.markdown(f"🛡️ `{tactic}`")
                
                st.markdown("### Extracted Indicators of Compromise (IoCs)")
                for ioc in analysis["iocs"]:
                    st.markdown(f"- `{ioc}`")
            
            with tab2:
                st.markdown("### Splunk AI Generated SPL Query")
                st.code(analysis["spl_query"], language="sql")
                st.markdown("### Surrounding Log Context (Blast Radius)")
                logs = splunk.run_spl_query(analysis["spl_query"])
                st.dataframe(logs)
                
            with tab3:
                st.markdown("### Recommended Remediation Playbook")
                for step in analysis["playbook"]:
                    st.markdown(f"✅ {step}")
                st.markdown("---")
                st.markdown("### Automated Actions")
                colA, colB = st.columns(2)
                if colA.button("🚫 Isolate Host via SOAR", use_container_width=True):
                    st.error(f"Host {alert['host']} has been isolated.")
                if colB.button("🔒 Suspend User", use_container_width=True):
                    st.warning(f"User {alert['user']} has been suspended.")

            # --- NEW FEATURE: Live SOC Chatbot ---
            with tab4:
                st.markdown("### Ask SentinelAI Follow-up Questions")
                
                # Display chat history
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                # Chat input
                if prompt := st.chat_input("E.g., 'What should I do about the IP address?'"):
                    # Add user message to state
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Get AI response
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            time.sleep(1)
                            response = ai_agent.chat_response(prompt, alert['id'])
                            st.markdown(response)
                            st.session_state.chat_history.append({"role": "assistant", "content": response})
