from agents import SentinelAgent, HistorianAgent, PharmacistAgent, TriageAgent
from mock_data import events_stream, patient_emr
import time

def run_calm_system():
    # Initialize the Digital Team
    sentinel = SentinelAgent()
    historian = HistorianAgent()
    pharmacist = PharmacistAgent()
    triage = TriageAgent()

    print("🏥 --- C.A.L.M. SYSTEM ONLINE ---\n")

    for event in events_stream:
        print("-" * 50)
        print(f"Incoming Data: {event['metric']} = {event['value']}")
        
        # STEP 1: Sentinel watches the stream
        sentinel_result = sentinel.analyze(event)
        
        if sentinel_result['status'] == "NORMAL":
            print(f"✅ System: {sentinel_result['reason']}")
            continue 
            
        print(f"⚠️  SENTINEL FLAG: {sentinel_result['reason']}")

        # Fetch Patient Data
        patient_data = patient_emr.get(event['patient_id'])

        # STEP 2 & 3: Historian and Pharmacist analyze in parallel
        historian_result = historian.check_context(event, patient_data, sentinel_result)
        print(f"📝 HISTORIAN: {historian_result['verdict']} - {historian_result['explanation']}")

        pharmacist_result = pharmacist.check_meds(event, patient_data, sentinel_result)
        print(f"💊 PHARMACIST: Interaction? {pharmacist_result['interaction_detected']} - {pharmacist_result['comment']}")

        # STEP 4: Triage Officer makes the final call
        final_decision = triage.decide(sentinel_result, historian_result, pharmacist_result)

        # FINAL OUTPUT
        print(f"\n🚀 FINAL DECISION: {final_decision['final_action']}")
        print(f"📟 DASHBOARD MESSAGE: \"{final_decision['message_to_doctor']}\"")
        
        time.sleep(2) 

if __name__ == "__main__":
    run_calm_system()