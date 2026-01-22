# app.py — Interference Detector (True/False, Randomized, Pronounless)
# Run: streamlit run app.py
import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="Interference Detector", page_icon="⚠️", layout="centered")

APP_TITLE = "Interference Detector"
APP_SUBTITLE = "Not a personality test. Not therapy. A mirror for interference."

ANSWER_OPTIONS = ["True", "False"]

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

# 6 interference domains
Q_TOPICS = {
    "Q1":  ["misalignment"], "Q2":  ["misalignment"], "Q3":  ["misalignment"], "Q4":  ["misalignment"],
    "Q5":  ["pressure_avoidance"], "Q6":  ["pressure_avoidance"], "Q7":  ["pressure_avoidance"], "Q8":  ["pressure_avoidance"],
    "Q9":  ["execution_avoidance"], "Q10": ["execution_avoidance"], "Q11": ["execution_avoidance"], "Q12": ["execution_avoidance"],
    "Q13": ["resource_misuse"], "Q14": ["resource_misuse"], "Q15": ["resource_misuse"], "Q16": ["resource_misuse"],
    "Q17": ["relationship_constraint"], "Q18": ["relationship_constraint"], "Q19": ["relationship_constraint"], "Q20": ["relationship_constraint"],
    "Q21": ["threshold_fear"], "Q22": ["threshold_fear"], "Q23": ["threshold_fear"], "Q24": ["threshold_fear"], "Q25": ["threshold_fear"],
}

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

def reset_all():
    st.session_state.stage = "intro"
    st.session_state.answers25 = {}
    st.session_state.question_order = random.sample(
        [q["id"] for q in QUESTIONS_25], k=len(QUESTIONS_25)
    )
    st.session_state.cluster_topic = None
    st.session_state.topic_counts = Counter()

def detect_cluster(answers: dict):
    true_qids = [qid for qid, ans in answers.items() if ans == "True"]
    topic_counts = Counter()
    for qid in true_qids:
        for topic in Q_TOPICS.get(qid, []):
            topic_counts[topic] += 1

    if not topic_counts:
        return None, topic_counts, len(true_qids)

    top_topic, top_count = topic_counts.most_common(1)[0]
    # tight thresholds (authoritative)
    if len(true_qids) >= 8 and top_count >= 3:
        return top_topic, topic_counts, len(true_qids)

    return None, topic_counts, len(true_qids)

# ─────────────────────────────────────────────
# Session init
# ─────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
if "answers25" not in st.session_state:
    st.session_state.answers25 = {}
if "question_order" not in st.session_state:
    st.session_state.question_order = random.sample([q["id"] for q in QUESTIONS_25], k=len(QUESTIONS_25))
if "cluster_topic" not in st.session_state:
    st.session_state.cluster_topic = None
if "topic_counts" not in st.session_state:
    st.session_state.topic_counts = Counter()

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────
st.title(APP_TITLE)
st.caption(APP_SUBTITLE)

if st.session_state.stage == "intro":
    st.write("Answer quickly. If something feels too specific, answer anyway.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start", use_container_width=True):
            st.session_state.stage = "q25"
    with col2:
        if st.button("Reset", use_container_width=True):
            reset_all()

elif st.session_state.stage == "q25":
    st.subheader("25 Questions (True / False)")
    st.caption("No scales. No nuance. Interference either exists or it doesn’t.")

    ordered_questions = [
        next(q for q in QUESTIONS_25 if q["id"] == qid)
        for qid in st.session_state.question_order
    ]

    with st.form("form25"):
        for idx, q in enumerate(ordered_questions, start=1):
            default = st.session_state.answers25.get(q["id"], "False")
            st.session_state.answers25[q["id"]] = st.radio(
                f"{idx}. {q['text']}",
                ANSWER_OPTIONS,
                index=ANSWER_OPTIONS.index(default),
                key=f"a_{q['id']}",
                horizontal=True
            )
        submitted = st.form_submit_button("Finish")
        if submitted:
            topic, counts, true_count = detect_cluster(st.session_state.answers25)
            st.session_state.cluster_topic = topic
            st.session_state.topic_counts = counts
            st.session_state.true_count = true_count
            st.session_state.stage = "synthesis"

    if st.button("Retake", use_container_width=True):
        reset_all()

elif st.session_state.stage == "synthesis":
    st.subheader("This is what’s in the way")

    topic = st.session_state.cluster_topic
    verdict = synthesize(topic) if topic else synthesize("")

    st.write(f"**{verdict}**")
    st.write("If nothing changes, this interference will keep recreating itself.")

    st.divider()
    st.write("**Remove this interference — or keep managing around it?**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Collaborate", use_container_width=True):
            st.session_state.stage = "collab"
    with col2:
        if st.button("Exit", use_container_width=True):
            st.session_state.stage = "exit"

elif st.session_state.stage == "collab":
    st.subheader("Collaboration")

    st.write("Collaboration here does not mean advice. It means building structure that makes the right behavior unavoidable.")
    st.write("Route: Contributionism / giveittogot.com")

    outcome = st.text_area(
        "What would change if this interference were removed?",
        placeholder="Example: 'Consistent output becomes normal; money stops leaking; the right work becomes obvious.'"
    )

    route = st.selectbox(
        "Where to route collaboration",
        ["Contributionism", "giveittogot.com", "Both"],
        index=1
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save", use_container_width=True):
            st.success("Captured.")
            if outcome.strip():
                st.write("**Stated outcome:**")
                st.write(f"> {outcome.strip()}")
            st.write(f"**Route:** {route}")

    with col2:
        if st.button("Retake Test", use_container_width=True):
            reset_all()

elif st.session_state.stage == "exit":
    st.subheader("Exit")
    st.write("Understood. Awareness changes some outcomes. Structure changes most.")
    if st.button("Restart", use_container_width=True):
        reset_all()
