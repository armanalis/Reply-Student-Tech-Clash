import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from colorama import Fore, Style

# Load API Key securely
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt(system_prompt, user_input):
    """Helper function to call the API and clean the response"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Switch to "gpt-3.5-turbo" if needed
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.0 
        )
        content = response.choices[0].message.content.strip()
        
        # Clean Markdown Formatting
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        return content.strip()

    except Exception as e:
        print(f"{Fore.RED}API Error: {e}{Style.RESET_ALL}")
        return "{}"

# --- AGENT 1: THE SENTINEL (Observer) ---
class SentinelAgent:
    def analyze(self, event):
        print(f"{Fore.CYAN}🚑 SENTINEL is scanning event...{Style.RESET_ALL}")
        
        prompt = """
        You are the SENTINEL, an ICU monitoring AI.
        Your job is to look at raw vital signs and flag anomalies based on STANDARD medical thresholds.
        THRESHOLDS: HR < 50 or > 120 is ABNORMAL. HR 0 is CRITICAL.
        
        Output JSON ONLY:
        {
            "status": "NORMAL" or "ANOMALY",
            "reason": "Short explanation",
            "severity": "LOW", "MEDIUM", or "CRITICAL"
        }
        """
        response = call_gpt(prompt, f"Event Data: {json.dumps(event)}")
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"status": "NORMAL", "reason": "Error parsing AI response", "severity": "LOW"}

# --- AGENT 2: THE HISTORIAN (Context) ---
class HistorianAgent:
    def check_context(self, event, emr_data, sentinel_alert):
        print(f"{Fore.YELLOW}📚 HISTORIAN is consulting records...{Style.RESET_ALL}")
        
        prompt = f"""
        You are the HISTORIAN. You have access to the Patient's Medical Record (EMR).
        The Sentinel has flagged an anomaly: {sentinel_alert.get('reason')} (Severity: {sentinel_alert.get('severity')}).
        
        Check the EMR below. Does the patient's history (e.g., athlete, chronic condition) EXPLAIN this anomaly?
        
        Output JSON ONLY:
        {{
            "verdict": "CONFIRM" or "OBJECT",
            "explanation": "Why you think this is safe or unsafe based on history."
        }}
        """
        response = call_gpt(prompt, f"Patient EMR: {json.dumps(emr_data)}")
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"verdict": "CONFIRM", "explanation": "Error parsing AI response"}

# --- AGENT 3: THE PHARMACIST (Safety Net) ---
class PharmacistAgent:
    def check_meds(self, event, emr_data, sentinel_alert):
        print(f"{Fore.GREEN}💊 PHARMACIST is checking drug interactions...{Style.RESET_ALL}")
        
        prompt = f"""
        You are the PHARMACIST. Your job is to check if a patient's medication explains a vital sign change.
        The Sentinel has flagged: {sentinel_alert.get('reason')}.
        
        Patient Medications: {emr_data.get('medications')}
        
        Task:
        1. Look at the medications. Do any of them cause side effects matching the Sentinel's flag? (e.g., Beta-blockers cause low HR).
        2. If YES, this might be a "false alarm" caused by meds.
        
        Output JSON ONLY:
        {{
            "interaction_detected": true or false,
            "drug_name": "Name of drug or 'None'",
            "comment": "Explain the side effect connection if any."
        }}
        """
        response = call_gpt(prompt, f"Event Metric: {event.get('metric')} Value: {event.get('value')}")
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"interaction_detected": False, "drug_name": "None", "comment": "Error parsing"}

# --- AGENT 4: THE TRIAGE OFFICER (Decision) ---
class TriageAgent:
    def decide(self, sentinel_data, historian_data, pharmacist_data):
        print(f"{Fore.MAGENTA}👮 TRIAGE OFFICER is judging...{Style.RESET_ALL}")
        
        prompt = """
        You are the TRIAGE OFFICER. You are the boss.
        Your goal is to prevent Alarm Fatigue by synthesizing data from your team.
        
        TEAM REPORTS:
        1. Sentinel: {sentinel_reason} (Severity: {sentinel_sev})
        2. Historian: {historian_verdict} ({historian_exp})
        3. Pharmacist: Interaction Detected: {pharma_detected} ({pharma_comment})
        
        DECISION RULES:
        - CRITICAL (Life Threatening) -> CODE RED (Always).
        - If Pharmacist detects a known side effect (e.g., beta-blocker lowering HR) -> YELLOW LOG (Suppress alarm, notify doctor gently).
        - If Historian says it's normal for this specific patient -> YELLOW LOG or SUPPRESS.
        - Otherwise -> CODE RED.
        
        Output JSON ONLY:
        {
            "final_action": "CODE RED" or "YELLOW LOG" or "SUPPRESS",
            "message_to_doctor": "Brief, clear message for the dashboard."
        }
        """
        
        user_input = (f"Sentinel: {sentinel_data.get('reason')} ({sentinel_data.get('severity')}) \n"
                      f"Historian: {historian_data.get('verdict')} ({historian_data.get('explanation')}) \n"
                      f"Pharmacist: {pharmacist_data.get('interaction_detected')} ({pharmacist_data.get('comment')})")
        
        response = call_gpt(prompt, user_input)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"final_action": "ERROR", "message_to_doctor": "System Malfunction"}