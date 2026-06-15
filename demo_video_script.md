# Splunk SentinelAI - Demo Video Script
**Target Duration:** 2 minutes 45 seconds
**Theme/Tone:** Professional, Urgent, Innovative

---

### [0:00 - 0:30] Introduction & The Problem
**Visual:** The presenter is on screen with a background showing a chaotic, scrolling Splunk search terminal with thousands of red alerts.
**Audio (Voiceover/Presenter):** 
"Hello everyone. In modern Security Operations Centers, analysts face an overwhelming challenge: Alert Fatigue. When a critical alert fires in Splunk, an analyst typically spends 30 to 45 minutes manually pivoting through logs, writing complex SPL queries, and identifying the blast radius. That’s time adversaries use to move laterally."

### [0:30 - 1:15] The Solution: Splunk SentinelAI
**Visual:** Transition to a clean, modern dashboard (The Streamlit App). The logo "Splunk SentinelAI" pulses on screen.
**Audio:** 
"Enter Splunk SentinelAI—an autonomous SOC co-pilot built on Splunk's AI platform. Submitted for the Security Track of the Splunk AI Hackathon, SentinelAI intercepts high-fidelity alerts and does the heavy lifting for you."
**Visual:** Screen recording of the UI. The user clicks on a critical alert titled "Suspicious PowerShell Execution". 
**Audio:** 
"Watch what happens when an alert arrives. Instead of manual triage, SentinelAI's agent immediately analyzes the raw payload. It uses Splunk's AI capabilities to summarize the technical jargon into a plain-english threat description."

### [1:15 - 2:00] Deep Dive & AI Integration (Architecture)
**Visual:** Screen splits. Left side: Architecture Diagram highlighting the "AI Agent Router" and "GenAI/Splunk" modules. Right side: The app generating SPL in real time.
**Audio:** 
"But summarization isn't enough. We integrated a Natural Language to SPL translation engine. SentinelAI autonomously writes an SPL query to search the last 15 minutes of logs around the compromised host. It queries the Splunk REST API, retrieves the blast radius context, and correlates the data."
**Visual:** The UI populates with "Extracted IoCs" (IP addresses, Usernames) and an AI-generated "Remediation Playbook".
**Audio:** 
"The result? A dynamically generated remediation playbook tailored specifically to this incident, saving analysts precious time."

### [2:00 - 2:30] One-Click Remediation & Value Proposition
**Visual:** The user clicks the red "Isolate Host" button in the app. A success toast appears: "Host isolated via SOAR."
**Audio:** 
"With the attack chain fully understood, the analyst can execute one-click remediations directly from the dashboard, communicating back to Splunk SOAR or external firewalls. We've taken a 45-minute manual investigation down to just 45 seconds."

### [2:30 - 2:45] Conclusion
**Visual:** The repository link and team name appear on the screen alongside the MIT open source logo.
**Audio:** 
"Splunk SentinelAI enhances security teams, accelerates threat detection, and integrates seamlessly with Splunk data. All code is fully open-source and available on GitHub. Thank you for watching!"