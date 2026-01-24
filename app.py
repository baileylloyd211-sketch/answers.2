import random
from collections import Counter
import streamlit as st

# ──────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Answers (25)", page_icon="🧭", layout="centered")

OPTIONS = ["almost always", "sometimes", "rarely", "never"]

# Treat these as "signal present" for clustering
TRUTHY = {"almost always", "sometimes"}

# ──────────────────────────────────────────────────────────────
# Questions (edit these freely)
# ──────────────────────────────────────────────────────────────
QUESTIONS_25 = [
    {"id": "Q1", "text": "I know what I should do, but I stall anyway."},
    {"id": "Q2", "text": "I avoid pressure until it becomes urgent."},
    {"id": "Q3", "text": "I spend time managing discomfort instead of moving forward."},
    {"id": "Q4", "text": "I keep plans vague to avoid being measured."},
    {"id": "Q5", "text": "I protect peace by not saying what needs to be said."},

    {"id": "Q6", "text": "My effort goes into motion, not outcomes."},
    {"id": "Q7", "text": "I sidestep responsibility that comes with higher capacity."},
    {"id": "Q8", "text": "I overthink to avoid committing."},
    {"id": "Q9", "text": "I use distractions to reduce pressure."},
    {"id": "Q10", "text": "I stay busy but don’t advance the core objective."},

    {"id": "Q11", "text": "I spend resources managing symptoms, not causes."},
    {"id": "Q12", "text": "I avoid conflict even when honesty is required."},
    {"id": "Q13", "text": "I delay decisions to avoid being wrong in public."},
    {"id": "Q14", "text": "I hesitate to scale up because exposure increases."},
    {"id": "Q15", "text": "I compromise ambition to keep relationships stable."},

    {"id": "Q16", "text": "I feel capable but operate below capacity."},
    {"id": "Q17", "text": "I avoid tasks that would clearly reveal my level."},
    {"id": "Q18", "text": "I spend time refining instead of shipping."},
    {"id": "Q19", "text": "I avoid using the resources that would solve the problem."},
    {"id": "Q20", "text": "I keep things small so consequences stay small."},

    {"id": "Q21", "text": "I avoid growth because it changes what people expect from me."},
    {"id": "Q22", "text": "I avoid stepping into roles where failure is visible."},
    {"id": "Q23", "text": "I don’t fully commit because success would demand more."},
    {"id": "Q24", "text": "I hold back because I don’t want the spotlight."},
    {"id": "Q25", "text": "I avoid higher responsibility even when I know I can handle it."},
]

# ──────────────────────────────────────────────────────────────
# Question → Topic map (edit as needed)
# ──────────────────────────────────────────────────────────────
QUESTION_TOPIC_MAP = {
    "Q1": ["execution_avoidance"],
    "Q2": ["pressure_avoidance"],
    "Q3": ["execution_avoidance"],
    "Q4": ["threshold_fear"],
    "Q5": ["relationship_constraint"],

    "Q6": ["misalignment"],
    "Q7": ["threshold_fear"],
    "Q8": ["execution_avoidance"],
    "Q9": ["pressure_avoidance"],
    "Q10": ["misalignment"],

    "Q11": ["resource_misuse"],
    "Q12": ["relationship_constraint"],
    "Q13": ["threshold_fear"],
    "Q14": ["threshold_fear"],
    "Q15": ["relationship_constraint"],

    "Q16": ["pressure_avoidance"],
    "Q17": ["threshold_fear"],
    "Q18": ["execution_avoidance"],
    "Q19": ["resource_misuse"],
    "Q20": ["threshold_fear"],

    "Q21": ["threshold_fear"],
    "Q22": ["threshold_fear"],
    "Q23": ["threshold_fear"],
    "Q24": ["threshold_fear"],
    "Q25": ["threshold_fear"],
}

# ──────────────────────────────────────────────────────────────
# Synthesis – sharp, concise, professional
# ──────────────────────────────────────────────────────────────


def topic_title(topic: str) -> str:
    return {
        "misalignment": "Misalignment",
        "pressure_avoidance": "Pressure Avoidance",
        "execution_avoidance": "Execution Avoidance",
        "resource_misuse": "Resource Misuse",
        "relationsdef synthesize(topic: str) -> str:
    synthesis = {
        "misalignment": "Effort is directed toward activities that do not advance the core objective.",
        "pressure_avoidance": "Pressure is managed through avoidance rather than absorption, limiting sustained performance at full capacity.",
        "execution_avoidance": "Time and attention are allocated to reducing immediate discomfort rather than generating forward progress.",
        "resource_misuse": "Resources are primarily expended on symptom management instead of addressing root causes.",
        "relationship_constraint": "Certain relationships or dynamics are preserved at the expense of required honesty or ambition.",
        "threshold_fear": "Growth is constrained to avoid the increased responsibility and visibility associated with higher performance.",
    }
    return synthesis.get(topic, "Multiple patterns are present at comparable strength, preventing a single dominant interference from emerging.")hip_constraint": "Relationship Constraint",
        "threshold_fear": "Threshold Fear",
    }.get(topic, topic.replace("_", " ").title())

# ──────────────────────────────────────────────────────────────
# State helpers
# ──────────────────────────────────────────────────────────────
def reset_all():
    st.session_state.stage = "intro"
    st.session_state.answers25 = {}
    st.session_state.question_order = random.sample([q["id"] for q in QUESTIONS_25], k=len(QUESTIONS_25))
    st.session_state.idx = 0
    st.session_state.cluster_topic = None
    st.session_state.topic_counts = Counter()

def ensure_state():
    if "stage" not in st.session_state:
        reset_all()

# ──────────────────────────────────────────────────────────────
# Cluster logic
# ──────────────────────────────────────────────────────────────
def detect_cluster(answers: dict):
    true_qids = [qid for qid, ans in answers.items() if ans in TRUTHY]

    counts = Counter()
    for qid in true_qids:
        for t in QUESTION_TOPIC_MAP.get(qid, []):
            counts[t] += 1

    if not counts:
        return None, counts

    top_topic, top_count = counts.most_common(1)[0]
    MIN_HITS = 3
    if top_count >= MIN_HITS:
        return top_topic, counts

    return None, counts

# ──────────────────────────────────────────────────────────────
# UI
# ──────────────────────────────────────────────────────────────
ensure_state()

st.title("Answers (25)")
st.caption("Not a test. No grades. Just signal → correction.")

col_reset, col_spacer = st.columns([1, 4])
with col_reset:
    if st.button("Restart entire session", use_container_width=True):
        reset_all()
        st.rerun()

if st.session_state.stage == "intro":
    st.markdown("""
    Answer 25 prompts honestly.  
    At the end you’ll receive the dominant interference pattern (if one clears the threshold) along with a concise diagnostic statement.
    """)
    if st.button("Begin", type="primary", use_container_width=True):
        st.session_state.stage = "run"
        st.rerun()

elif st.session_state.stage == "run":
    order = st.session_state.question_order
    idx = st.session_state.idx

    if idx >= len(order):
        topic, counts = detect_cluster(st.session_state.answers25)
        st.session_state.cluster_topic = topic
        st.session_state.topic_counts = counts
        st.session_state.stage = "results"
        st.rerun()

    qid = order[idx]
    q = next(x for x in QUESTIONS_25 if x["id"] == qid)

    st.subheader(f"{idx + 1} / 25")
    st.write(q["text"])

    # Auto-save on selection
    def save_current():
        if f"radio_{qid}" in st.session_state:
            st.session_state.answers25[qid] = st.session_state[f"radio_{qid}"]

    current_answer = st.session_state.answers25.get(qid)
    selected_index = OPTIONS.index(current_answer) if current_answer in OPTIONS else 1  # default "sometimes" if unset

    st.radio(
        "How often does this apply?",
        OPTIONS,
        index=selected_index,
        key=f"radio_{qid}",
        on_change=save_current,
    )

    st.progress((idx + 1) / len(order))

    col_back, col_next = st.columns([1, 2])
    with col_back:
        if st.button("← Back", use_container_width=True, disabled=(idx == 0)):
            st.session_state.idx = idx - 1
            st.rerun()
    with col_next:
        if st.button("Next →", type="primary", use_container_width=True):
            save_current()  # safety
            st.session_state.idx = idx + 1
            st.rerun()

elif st.session_state.stage == "results":
    topic = st.session_state.cluster_topic
    counts = st.session_state.topic_counts

    st.subheader("Result")

    if topic is None:
        st.write("No single pattern reached the minimum signal threshold (≥3 truthy responses).")
        st.write("This typically indicates either distributed patterns or predominantly 'rarely/never' responses.")
    else:
        st.markdown(f"### Dominant interference: **{topic_title(topic)}**")
        st.write(synthesize(topic))

    st.divider()
    st.subheader("Signal strength by pattern (truthy responses only)")
    if counts:
        for t, n in counts.most_common():
            strength = "strong" if n >= 5 else "moderate" if n >= 3 else "weak"
            st.write(f"- **{topic_title(t)}** ({n} hits, {strength}): {synthesize(t)}")
    else:
        st.write("No truthy responses recorded.")

    st.divider()
    if st.button("Begin again", type="primary", use_container_width=True):
        reset_all()
        st.rerun()        
        st.write(synthesize(minor))

    st.write("Left unaddressed, these will continue reinforcing each other.")

    st.markdown("**Remove the interference — or keep managing around it?**")
else:
    st.write(
        "Multiple competing interferences are present, preventing a single corrective action from emerging."
    )




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
st.title("Answers (25)")
st.caption("Not a test. No grades. Just signal → correction.")

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
