# app.py
# Streamlit app — Interference Detector
# True / False only. Randomized. Pronounless. Dual-use (individual / organization)

import streamlit as st
import random
from collections import Counter

# ─────────────────────────────────────────────
# App Config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Interference Detector",
    page_icon="⚠️",
    layout="centered"
)

APP_TITLE = "Interference Detector"
APP_SUBTITLE = "This is not a personality test. It identifies what is in the way."

# ─────────────────────────────────────────────
# Answer Options (LOCKED)
# ─────────────────────────────────────────────

ANSWER_OPTIONS = ["True", "False"]

# ─────────────────────────────────────────────
# 25 Pronounless, Dual-Use, Action-Forcing Questions
# ─────────────────────────────────────────────

QUESTIONS_25 = [
    {"id": "Q1",  "text": "Is real effort being invested in something that does not actually matter?"},
    {"id": "Q2",  "text": "Is it difficult to clearly explain why the current direction deserves the next five years?"},
    {"id": "Q3",  "text": "Is activity being mistaken for progress?"},
    {"id": "Q4",  "text": "Has too much time been invested to admit the wrong ladder may be involved?"},

    {"id": "Q5",  "text": "Does performance degrade when pressure increases instead of sharpening?"},
    {"id": "Q6",  "text": "Are situations avoided where failure would be visible and undeniable?"},
    {"id": "Q7",  "text": "Are comfort tasks prioritized over consequential ones?"},
    {"id": "Q8",  "text": "Is operation occurring below actual capacity because it feels safer?"},

    {"id": "Q9",  "text": "Is long-term progress being traded for short-term relief?"},
    {"id": "Q10", "text": "Is lack of time claimed while time allocation is still controlled?"},
    {"id": "Q11", "text": "Are days primarily reactive rather than intentional?"},
    {"id": "Q12", "text": "Are hard decisions delayed until urgency removes choice?"},

    {"id": "Q13", "text": "Does spending contradict stated priorities?"},
    {"id": "Q14", "text": "Is financial clarity avoided because it would force change?"},
    {"id": "Q15", "text": "Are resources used to manage discomfort instead of fixing root problems?"},
    {"id": "Q16", "text": "Is short-term relief chosen even when it creates long-term pressure?"},

    {"id": "Q17", "text": "Does at least one key relationship benefit from things staying exactly as they are?"},
    {"id": "Q18", "text": "Is ambition limited to avoid disruption or conflict?"},
    {"id": "Q19", "text": "Is honesty withheld to preserve access, approval, or stability?"},
    {"id": "Q20", "text": "Is it already clear who would be uncomfortable if change occurred?"},

    {"id": "Q21", "text": "Is success distrusted because of fear of losing control?"},
    {"id": "Q22", "text": "Are exit routes kept open so full commitment is never required?"},
    {"id": "Q23", "text": "Is retreat chosen when consistency becomes non-negotiable?"},
    {"id": "Q24", "text": "Is scope kept small to keep responsibility manageable?"},

    {"id": "Q25", "text": "If nothing changes, is the outcome already known—and being tolerated?"},
]

# ─────────────────────────────────────────────
# Interference Domains (6 only)
# ─────────────────────────────────────────────

Q_TOPICS = {
    "Q1":  ["misalignment"],
    "Q2":  ["misalignment"],
    "Q3":  ["misalignment"],
    "Q4":  ["misalignment"],

    "Q5":  ["pressure_avoidance"],
    "Q6":  ["pressure_avoidance"],
    "Q7":  ["pressure_avoidance"],
    "Q8":  ["pressure_avoidance"],

    "Q9":  ["execution_avoidance"],
    "Q10": ["execution_avoidance"],
    "Q11": ["execution_avoidance"],
    "Q12": ["execution_avoidance"],

    "Q13": ["resource_misuse"],
    "Q14": ["resource_misuse"],
    "Q15": ["resource_misuse"],
    "Q16": ["resource_misuse"],

    "Q17": ["relationship_constraint"],
    "Q18": ["relationship_constraint"],
    "Q19": ["relationship_constraint"],
    "Q20": ["relationship_constraint"],

    "Q21": ["threshold_fear"],
    "Q22": ["threshold_fear"],
    "Q23": ["threshold_fear"],
    "Q24": ["threshold_fear"],
    "Q25": ["threshold_fear"],
}

# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────

if "answers25" not in st.session_state:
    st.session_state.answers25 = {}

if "question_order" not in st.session_state:
    st.session_state.question_order = random.sample(
        [q["id"] for q in QUESTIONS_25],
        k=len(QUESTIONS_25)
    )

# ─────────────────────────────────────────────
# Signal Detection (True = interference present)
# ─────────────────────────────────────────────

def detect_cluster(answers: dict):
    true_qids = [qid for qid, ans in answers.items() if ans == "True"]

    topic_counts = Counter()
    for qid in true_qids:
        for topic in Q_TOPICS.get(qid, []):
            topic_counts[topic] += 1

    if not topic_counts:
        return None, topic_counts

    top_topic, top_count = topic_counts.most_common(1)[0]

    # thresholds (tight, authoritative)
    if top_count >= 3 and len(true_qids) >= 8:
        return top_topic, topic_counts

    return None, topic_counts

# ─────────────────────────────────────────────
# Synthesis (Pronounless, Verdict-Style)
# ─────────────────────────────────────────────

def synthesize(topic: str) -> str:
    synthesis = {
        "misalignment":
            "Effort is being applied to a direction that does not justify continued investment, creating motion without progress.",

        "pressure_avoidance":
            "Pressure is being avoided rather than absorbed, resulting in sustained operation below actual capacity.",

        "execution_avoidance":
            "Time and attention are being used to reduce discomfort instead of producing forward movement.",

        "resource_misuse":
            "Resources are being spent to manage symptoms rather than resolve the conditions creating pressure.",

        "relationship_constraint":
            "At least one relationship is being protected at the cost of honesty, expansion, or ambition.",

        "threshold_fear":
            "Growth is being limited to avoid the responsibility and exposure that higher capacity would require.",
    }

    return synthesis.get(
        topic,
        "Multiple competing interferences are present, preventing a single corrective action from emerging."
    )


# Collaboration screen
elif st.session_state.stage == "collab":
    st.subheader("Collaboration")
    st.write("Pick what you want to build next:")

    topic = st.session_state.cluster_topic
    st.write(f"Topic focus: **{pretty_topic(topic)}**" if topic else "Topic focus: **(none detected)**") 

    idea = st.text_area(
        "Describe the project idea or outcome you want (short is fine):",
        placeholder="Example: 'I want a 2-week plan to remove avoidance and complete X.'"
    )

    st.write("Optional: where to route this")
    route = st.selectbox(
        "Collaboration route",
        ["Contributionism", "giveittogot.com", "Both", "Not sure yet"],
        index=1
    )

    if st.button("Save & show next steps", use_container_width=True):
        st.success("Captured. Here are next steps:")
        st.write("1) Define the outcome in one sentence.")
        st.write("2) Define constraints (time, money, tools, environment).")
        st.write("3) Define the smallest proof step you can do today (15–30 minutes).")
        st.write("4) Decide what you want me to generate next (plan, copy, UI, code, outreach).")

        if idea.strip():
            st.write("Your project idea:")
            st.write(f"> {idea.strip()}")
        st.write(f"Route selected: **{route}**")

    if st.button("Retake test"):
        reset_all()
