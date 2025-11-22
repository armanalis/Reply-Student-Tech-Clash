🏥 C.A.L.M. (Critical Agent Logic Module)
Student Clash 2025 > Category: Tech

📖 Overview
C.A.L.M. is an autonomous Clinical Decision Support System designed to restore order to the chaotic environment of the Intensive Care Unit (ICU).

ICU clinicians suffer from severe Alarm Fatigue, caused by thousands of daily alerts from uncoordinated devices. C.A.L.M. solves this not by silencing sensors, but by employing a "Digital Team" of specialized AI agents that negotiate in real-time to filter noise and surface only Critical Logic.


🚀 The Problem
Cognitive Overload: Clinicians must synthesize data from 10+ disconnected screens.

Alarm Fatigue: 72-99% of clinical alarms are false or non-actionable, leading to desensitization.

Context Blindness: Standard monitors scream "Low Heart Rate" even if the patient is a sleeping athlete; they lack the logic to understand why.

💡 The Solution: C.A.L.M. Architecture
We utilize a Level 3 Multi-Agent Approach  to separate detection, pharmacological analysis, and reasoning. The system does not just react; it thinks before it notifies.


The Agentic Workflow
The module consists of four autonomous agents working in a collaborative loop:

The Sentinel (Input Agent)

Function: Pure data ingestion (Vitals, Labs, IoT).

Logic: High sensitivity. If a number is out of range, it flags an "Anomaly Candidate".

Motto: "Miss nothing."

The Historian (Context Agent)

Function: Deep EMR analysis (Patient History, Chronic Conditions, Surgery Notes).

Logic: Checks if the anomaly is normal for this specific patient (e.g., "Patient is a marathon runner, low resting HR is expected").

Motto: "Know the patient."

The Pharmacist (Chemical Agent)

Function: Real-time Medication Timeline Tracking.

Logic: Analyzes When (timestamps) and What (active ingredients) was administered. It cross-references the Sentinel's anomaly against known drug side effects.

Action: Communicates directly with the Triage Officer if an anomaly is a likely drug reaction (e.g., “Notifying Agent C: The BP drop aligns perfectly with the Propofol bolus given 3 minutes ago”).

Motto: "Respect the chemistry."

The Triage Officer (Decider Agent)

Function: Decision, Consensus & Communication.

Logic: It acts as the team leader. It weighs the Sentinel's fear against the Historian's context and the Pharmacist's drug analysis.

Action: Autonomously decides the Alert Level:

🔴 Code Red: Audible Alarm (Unknown cause or life-threatening).

🟡 Yellow Log: Silent update to the dashboard (Expected side effect/Watchlist).

🟢 Suppress: False alarm dismissed with a log entry.

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
Start the logic engine simulation with the full agent team:

Bash

python main.py
