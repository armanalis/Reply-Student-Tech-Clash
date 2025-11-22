# ==========================================
# C.A.L.M. SYSTEM - COMPREHENSIVE MOCK DATA
# ==========================================
# This file simulates a live stream of data from an ICU block.
# It includes vital signs, lab results, and device logs for multiple patients.

# ------------------------------------------
# 1. ELECTRONIC MEDICAL RECORDS (EMR)
# ------------------------------------------
# The "Historian" Agent uses this to understand context.

patient_emr = {
    # --- EXISTING PATIENTS ---
    "P-808": {
        "name": "Alessandro Rossi",
        "age": 28,
        "condition": "Post-Op Knee Surgery",
        "medications": ["Atenolol (Beta-Blocker) - 08:00 AM", "Morphine (PRN)"],
        "history": "Competitive swimmer. Resting HR 40-45 bpm. No known allergies.",
        "notes": "Patient is currently sleeping. Post-op recovery normal."
    },
    "P-909": {
        "name": "Maria Bianchi",
        "age": 75,
        "condition": "Pneumonia",
        "medications": ["Antibiotics IV", "Saline Drip"],
        "history": "Hypertension, T2 Diabetes. History of Sepsis.",
        "notes": "Monitor for fever spikes. Fall risk high."
    },
    "P-707": {
        "name": "John Smith",
        "age": 45,
        "condition": "Trauma - Rib Fractures",
        "medications": ["Pain Management"],
        "history": "Smoker (1 pack/day).",
        "notes": "Patient is agitated. Frequently moves pulse oximeter finger probe."
    },

    # --- NEW PATIENTS (ADDED FOR COMPLEXITY) ---
    "P-606": {
        "name": "Lucas Green",
        "age": 6, 
        "condition": "Severe Asthma Exacerbation",
        "medications": ["Albuterol Nebulizer", "Prednisone"],
        "history": " pediatric asthma. Normal resting HR for age is 80-120.",
        "notes": "Parents at bedside. Watch for respiratory distress."
    },
    "P-505": {
        "name": "Robert Chen",
        "age": 82,
        "condition": "Heart Failure Exacerbation",
        "medications": ["Lasix", "Digoxin"],
        "history": "Pacemaker implanted 2020 (Fixed rate 60 bpm). Chronic Afib.",
        "notes": "Pacemaker spikes may appear on ECG monitor."
    },
    "P-404": {
        "name": "Unknown Male (John Doe)",
        "age": "Unknown (~30s)",
        "condition": "Motor Vehicle Accident (Trauma)",
        "medications": ["IV Fluids", "Blood Transfusion"],
        "history": "NO RECORDS FOUND.",
        "notes": "Identity unconfirmed. Treat all alarms as CRITICAL."
    }
}

# ------------------------------------------
# 2. LIVE EVENT STREAM
# ------------------------------------------
# The "Sentinel" Agent watches this stream.
# Includes: Vitals, Labs, IoT Device Status, Nurse Logs.

events_stream = [
    # --- SCENARIO 1: NORMAL BASELINE ---
    {"id": 100, "patient_id": "P-808", "type": "VITALS", "metric": "Heart Rate", "value": 72, "timestamp": "10:00:01"},
    {"id": 101, "patient_id": "P-909", "type": "VITALS", "metric": "Temp (C)", "value": 37.1, "timestamp": "10:00:05"},
    
    # --- SCENARIO 2: THE "FALSE ALARM" (Athlete + Meds) ---
    # Sentinel will panic (HR < 50). Historian should object (Athlete + Beta Blockers).
    {"id": 102, "patient_id": "P-808", "type": "VITALS", "metric": "Heart Rate", "value": 42, "timestamp": "10:05:00"},
    
    # --- SCENARIO 3: THE "SILENT KILLER" (Sepsis Trend) ---
    # Individually, these might look like "Medium" alerts, but combined they are CRITICAL.
    {"id": 103, "patient_id": "P-909", "type": "VITALS", "metric": "Temp (C)", "value": 39.4, "timestamp": "10:15:00"},
    {"id": 104, "patient_id": "P-909", "type": "VITALS", "metric": "BP Systolic", "value": 85, "timestamp": "10:15:30"},
    {"id": 105, "patient_id": "P-909", "type": "VITALS", "metric": "Heart Rate", "value": 115, "timestamp": "10:16:00"},
    
    # --- SCENARIO 4: TECHNICAL ARTIFACT vs REALITY ---
    # Sensor reading goes to zero (Technical fault), but patient is fine.
    {"id": 106, "patient_id": "P-707", "type": "VITALS", "metric": "SpO2", "value": 0, "timestamp": "10:30:00"},
    {"id": 107, "patient_id": "P-707", "type": "LOG", "metric": "Nurse Note", "value": "Probe disconnected, patient repositioning", "timestamp": "10:30:05"},
    
    # --- SCENARIO 5: CRITICAL EVENT (Code Blue) ---
    {"id": 108, "patient_id": "P-808", "type": "VITALS", "metric": "Heart Rate", "value": 0, "timestamp": "11:00:00"},

    # --- SCENARIO 6: PEDIATRIC CONTEXT (New) ---
    # HR 110 is Tachycardia for an adult, but normal for a stressed 6yo.
    # Historian should OBJECT to a high-severity alarm.
    {"id": 109, "patient_id": "P-606", "type": "VITALS", "metric": "Heart Rate", "value": 110, "timestamp": "11:15:00"},
    # BUT... SpO2 dropping is real danger for asthma.
    {"id": 110, "patient_id": "P-606", "type": "VITALS", "metric": "SpO2", "value": 88, "timestamp": "11:16:00"},

    # --- SCENARIO 7: PACEMAKER LOGIC (New) ---
    # HR 58 might flag as bradycardia (<60), but Historian knows he has a fixed-rate pacemaker.
    {"id": 111, "patient_id": "P-505", "type": "VITALS", "metric": "Heart Rate", "value": 58, "timestamp": "11:30:00"},

    # --- SCENARIO 8: THE UNKNOWN (New) ---
    # P-404 has NO records. Historian returns "NO DATA". 
    # Triage Officer must default to SAFE mode (assume the worst) -> CODE RED.
    {"id": 112, "patient_id": "P-404", "type": "VITALS", "metric": "BP Systolic", "value": 70, "timestamp": "11:45:00"},
]