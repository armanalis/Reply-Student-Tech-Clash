C.A.L.M. is an autonomous Hospital Orchestration System designed to bridge the silos between Emergency, General Wards, Pharmacy, and Administration.

In a modern hospital, critical information gets trapped in departmental bubbles. An ER doctor might not know a patient in General Ward B is having a reaction to a drug administered hours ago in Surgery. C.A.L.M. solves this by employing a Level 3 Multi-Agent System  that acts as a central nervous system, negotiating data across the entire facility to surface only Critical Logic.

🚀 The Problem
Operational Fragmentation: Critical patient data is siloed. The ER, ICU, and General Wards often operate as separate islands, leading to delayed interventions.

Alert Overload & Desensitization: Across a whole hospital, thousands of alerts trigger hourly. Staff cannot distinguish between a "low battery" warning and a "cardiac event" without manual review.

Medication Reconciliation Errors: 40% of medication errors occur during patient transfer (e.g., moving from Surgery to Recovery). Standard systems lack the "memory" to track active ingredients across these transitions.

💡 The Solution: C.A.L.M. Architecture
We utilize a Multi-Agent Approach  to separate hospital-wide detection, pharmacological safety, and cross-departmental reasoning. The system creates a "digital team"  that thinks before it broadcasts.


The Agentic Workflow
The module consists of four autonomous agents working in a collaborative loop to handle specific roles:

1. The Sentinel (The Watchtower Agent)
Role: Global Data Ingestion (Vitals, IoT, Bed Status, Lab Results).

Logic: Monitors the entire hospital grid. It possesses high sensitivity but low context. If a patient's vitals spike in any ward, or if a lab result is critical, it flags a "Hospital Event Candidate."

Motto: "See everything, everywhere."

2. The Historian (The Context Engine)
Role: Deep EMR & Transfer Analysis.

Logic: Accesses the full longitudinal patient record. It checks: "Is this patient post-op?" "Do they have a history of chronic arrhythmia?" "Did they just transfer from the ER?"

Goal: It validates if the Sentinel's alert is actually abnormal for this specific patient's current journey.

Motto: "Know the patient's journey."

3. The Pharmacist (The Safety Net)
Role: Cross-Departmental Medication Tracking.

Logic: Analyzes the Drug Timeline across transfers. It looks for "stacking" effects—e.g., a sedative given in the ER interacting with a painkiller given 4 hours later in the General Ward.

Action: Communicates with the Triage Officer if a sudden vital sign change correlates with a medication peak time, preventing false "sepsis" alerts that are actually drug side effects.

Motto: "Respect the chemistry."

4. The Triage Officer (The Command Center / "Agent C")

Role: Decision, Consensus & Communication.

Logic: Acts as the Hospital Chief of Staff. It facilitates the negotiation:

Sentinel: "Patient in Room 302 has dropping BP."

Pharmacist: "Wait, they received a beta-blocker 30 mins ago."

Historian: "Patient is also marked as 'Sleeping' in the night shift log."

Action: Autonomously distributes the alert to the correct department:

🔴 Code Red: Immediate Pager Alert to Floor Nurse (Life-threatening/Unexplained).

🟡 Yellow Consult: Silent notification to the resident doctor's tablet (Medication adjustment needed).

🟢 Log Only: Suppress alert (Expected physiological response to treatment).

⚙️ Technical Implementation
Prerequisites
Python 3.8+

OpenAI API Key (or compatible LLM endpoint)

Installation
Clone the repository:

Bash

git clone https://github.com/yourusername/calm-agent.git
cd calm-agent
Install dependencies:

Bash

pip install -r requirements.txt

(Includes openai, python-dotenv, pydantic) 

Security Setup: Create a .env file in the root directory. Do not hardcode keys.

Code snippet

OPENAI_API_KEY=sk-your-secret-key-here
How to Run
Start the hospital logic engine simulation with the full agent team:

Bash

python main.py
Note on Student Clash Requirements:

This project fulfills the Level 3 Multi-Agent Approach by demonstrating agents "reasoning or negotiating with each other".

The pharmacist agent adds the required complexity of specific knowledge domains interacting.