import sys
from pathlib import Path

import streamlit as st


# =========================================================
# PROJECT PATH
# =========================================================

ROOT_DIR = Path(__file__).resolve().parents[1]

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# =========================================================
# HINDSIGHT / AGENT
# =========================================================

from agent.support_agent import (
    get_customer_memory,
    generate_support_response,
    save_customer_interaction,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SupportMemory AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DASHBOARD STYLE
# =========================================================

st.markdown(
    """
    <style>

        /* Main application */

        .stApp {
            background: linear-gradient(
                135deg,
                #0f0f1a 0%,
                #17152b 50%,
                #0d1224 100%
            );

            color: #f5f5f7;
        }


        /* Sidebar */

        [data-testid="stSidebar"] {
            background: #0b0b14;
            border-right: 1px solid #29233f;
        }

        [data-testid="stSidebar"] * {
            color: #f5f5f7;
        }


        /* Headings */

        h1,
        h2,
        h3 {
            color: #ffffff;
        }


        /* Buttons */

        .stButton > button {
            border-radius: 10px;
            border: 1px solid #3b3260;
            background: #17152b;
            color: white;
            font-weight: 600;
        }

        .stButton > button:hover {
            border-color: #8B5CF6;
            color: white;
        }


        /* Text area */

        .stTextArea textarea {
            background: #11111d;
            color: white;
            border: 1px solid #383052;
            border-radius: 10px;
        }


        /* Select box */

        [data-baseweb="select"] > div {
            background: #11111d;
            border-color: #383052;
        }


        /* Metrics */

        [data-testid="stMetric"] {
            background: #151425;
            border: 1px solid #2d2745;
            border-radius: 12px;
            padding: 12px;
        }


        /* Containers */

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #151425;
            border: 1px solid #2d2745;
            border-radius: 14px;
        }


        /* Divider */

        hr {
            border-color: #2d2745;
        }


        /* Tabs */

        [data-baseweb="tab-list"] {
            gap: 8px;
        }

        [data-baseweb="tab"] {
            border-radius: 8px;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# CUSTOMER DATA
# =========================================================

CUSTOMERS = {

    "Priya": {
        "initials": "P",
        "status": "VIP Customer",
        "type": "Payment Support",
        "description": "Returning customer with payment history",
    },

    "Rahul": {
        "initials": "R",
        "status": "Returning Customer",
        "type": "UPI Support",
        "description": "Returning customer with UPI history",
    },

    "Arjun": {
        "initials": "A",
        "status": "Enterprise User",
        "type": "Account Support",
        "description": "Customer with account support history",
    },

    "Sneha": {
        "initials": "S",
        "status": "Regular Customer",
        "type": "Delivery Support",
        "description": "Customer with delivery history",
    },

}


# =========================================================
# SESSION STATE
# =========================================================

defaults = {

    "selected_customer": "Priya",

    "memories": [],

    "profile_memories": [],

    "last_query_memories": [],

    "last_response": "",

    "chat_history": [],

    "recall_count": 0,

    "retain_count": 0,

    "last_action": "System Ready",

    "last_customer": "Priya",

    "customer_message": "",

    "active_filter": "All",

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def unique_memories(memories):

    result = []

    for memory in memories:

        clean = str(memory).strip()

        if clean and clean not in result:

            result.append(clean)

    return result


def classify_memory(memory):

    text = memory.lower()


    # -----------------------------------------------------
    # PREFERENCES
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "prefer",
            "preference",
            "likes",
            "wants",
            "direct",
            "short",
            "step-by-step",
            "one step",
            "one troubleshooting step",
            "troubleshooting step",
        ]
    ):

        return "Preference", "💡"


    # -----------------------------------------------------
    # SUCCESSFUL SOLUTIONS
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "resolved",
            "solution",
            "fixed",
            "worked",
            "successfully",
        ]
    ):

        return "Successful Solution", "🛠️"


    # -----------------------------------------------------
    # PREVIOUS PROBLEMS
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "failed",
            "failure",
            "problem",
            "issue",
            "error",
            "declined",
            "trouble",
        ]
    ):

        return "Previous Problem", "⚠️"


    # -----------------------------------------------------
    # CUSTOMER CONTEXT
    # -----------------------------------------------------

    if any(
        word in text
        for word in [
            "currently",
            "uses",
            "using",
            "account",
            "mobile",
            "app",
        ]
    ):

        return "Customer Context", "👤"


    return "Customer Memory", "🧠"


def memory_reason(category):

    reasons = {

        "Preference":
            "This helps the AI adapt how it communicates with the customer.",

        "Successful Solution":
            "This gives the AI a previously successful solution to consider.",

        "Previous Problem":
            "This helps the AI recognize recurring or similar customer issues.",

        "Customer Context":
            "This gives the AI additional customer-specific context.",

        "Customer Memory":
            "This provides historical context for future support requests.",
    }

    return reasons.get(
        category,
        "Provides historical context for future support.",
    )


def show_memory(memory, number=None):

    category, icon = classify_memory(memory)

    title = f"{icon} {category}"

    if number is not None:

        title = f"{title}  •  Memory #{number}"

    with st.container(border=True):

        st.markdown(f"**{title}**")

        st.write(memory)

        st.caption(
            f"💡 Why it matters: {memory_reason(category)}"
        )


def get_memory_counts(memories):

    counts = {

        "Preference": 0,

        "Successful Solution": 0,

        "Previous Problem": 0,

        "Customer Context": 0,

        "Customer Memory": 0,

    }

    for memory in memories:

        category, _ = classify_memory(memory)

        if category in counts:

            counts[category] += 1

    return counts


def reset_current_session():

    st.session_state.memories = []

    st.session_state.profile_memories = []

    st.session_state.last_query_memories = []

    st.session_state.last_response = ""

    st.session_state.customer_message = ""

    st.session_state.active_filter = "All"

    st.session_state.last_action = "Session Reset"


def load_customer_memory():

    customer = st.session_state.selected_customer

    try:

        memories = get_customer_memory(

            customer,

            (
                f"Give me the important previous history, "
                f"preferences, successful solutions, problems, "
                f"and customer context for {customer}."
            ),

        )

        memories = unique_memories(memories)

        st.session_state.profile_memories = memories

        st.session_state.memories = memories

        st.session_state.last_query_memories = memories

        st.session_state.last_action = (
            f"Loaded {len(memories)} memories for {customer}"
        )

        return True

    except Exception as e:

        st.error(
            f"Unable to load customer memory: {e}"
        )

        return False


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🧠 SupportMemory AI")

    st.caption(
        "Persistent AI customer-support intelligence"
    )

    st.divider()


    # -----------------------------------------------------
    # CUSTOMER
    # -----------------------------------------------------

    st.subheader("👤 Active Customer")

    customer_names = list(CUSTOMERS.keys())

    selected_customer = st.selectbox(

        "Select customer",

        customer_names,

        index=customer_names.index(
            st.session_state.selected_customer
        ),

    )


    if selected_customer != st.session_state.last_customer:

        reset_current_session()

        st.session_state.last_customer = selected_customer


    st.session_state.selected_customer = selected_customer

    customer = CUSTOMERS[selected_customer]


    # -----------------------------------------------------
    # CUSTOMER BADGE
    # -----------------------------------------------------

    st.info(

        f"**{customer['initials']}  {selected_customer}**\n\n"
        f"{customer['status']}"

    )

    st.caption(
        customer["type"]
    )


    st.divider()


    # -----------------------------------------------------
    # MEMORY ENGINE
    # -----------------------------------------------------

    st.subheader("📊 Memory Engine")

    metric1, metric2 = st.columns(2)

    with metric1:

        st.metric(
            "Recalls",
            st.session_state.recall_count,
        )

    with metric2:

        st.metric(
            "Learned",
            st.session_state.retain_count,
        )


    st.divider()


    st.success(
        "🟢 Hindsight Connected"
    )

    st.caption(
        "Long-term customer memory is active."
    )


    st.divider()


    # -----------------------------------------------------
    # QUICK ACTIONS
    # -----------------------------------------------------

    st.subheader("⚡ Quick Actions")


    if st.button(
        "🧠 Load Customer Memory",
        use_container_width=True,
    ):

        with st.spinner(
            f"Loading {selected_customer}'s memory..."
        ):

            if load_customer_memory():

                st.toast(
                    f"🧠 Loaded {selected_customer}'s memory"
                )

                st.rerun()


    if st.button(
        "🔄 Reset Session",
        use_container_width=True,
    ):

        reset_current_session()

        st.toast(
            "Session reset successfully."
        )

        st.rerun()


    st.divider()


    st.caption(
        "Choose a customer, explore their memory, "
        "and demonstrate how the AI becomes more personalized."
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.title(
    "🧠 SupportMemory AI"
)

st.caption(
    "AI customer support that remembers previous problems, "
    "successful solutions, preferences, and context."
)


header1, header2, header3 = st.columns(3)

with header1:

    st.info(
        "👤 Customer-aware"
    )

with header2:

    st.info(
        "🧠 Persistent memory"
    )

with header3:

    st.success(
        "⚡ Hindsight powered"
    )


# =========================================================
# CUSTOMER PROFILE
# =========================================================

st.divider()

profile_left, profile_right = st.columns(
    [3, 1]
)


with profile_left:

    st.subheader(
        f"👤 {selected_customer}"
    )

    st.write(
        customer["description"]
    )

    badge1, badge2, badge3 = st.columns(3)


    with badge1:

        st.info(
            f"**Status**\n\n{customer['status']}"
        )


    with badge2:

        st.info(
            f"**Support Type**\n\n{customer['type']}"
        )


    with badge3:

        st.success(
            "**Memory**\n\nActive"
        )


with profile_right:

    known_memories = unique_memories(
        st.session_state.profile_memories
    )

    st.metric(
        "Known Memories",
        len(known_memories),
    )

    st.caption(
        "Powered by Hindsight"
    )


# =========================================================
# WHAT HINDSIGHT KNOWS
# =========================================================

st.divider()

st.subheader(
    f"🧠 What Hindsight Remembers About {selected_customer}"
)

st.caption(
    "These memories help the support agent understand "
    "the customer's history before responding."
)


profile_memories = unique_memories(
    st.session_state.profile_memories
)


if profile_memories:

    counts = get_memory_counts(
        profile_memories
    )


    # -----------------------------------------------------
    # MEMORY SUMMARY
    # -----------------------------------------------------

    m1, m2, m3, m4 = st.columns(4)


    with m1:

        st.metric(
            "💡 Preferences",
            counts["Preference"],
        )


    with m2:

        st.metric(
            "🛠️ Solutions",
            counts["Successful Solution"],
        )


    with m3:

        st.metric(
            "⚠️ Problems",
            counts["Previous Problem"],
        )


    with m4:

        st.metric(
            "👤 Context",
            counts["Customer Context"],
        )


    st.divider()


    # -----------------------------------------------------
    # PROFILE MEMORY FILTER
    # -----------------------------------------------------

    profile_filter_options = [

        "All",

        "Preference",

        "Successful Solution",

        "Previous Problem",

        "Customer Context",

    ]


    profile_filter = st.segmented_control(

        "Memory Type",

        profile_filter_options,

        default="All",

        key="profile_memory_filter",

    )


    if profile_filter is None:

        profile_filter = "All"


    if profile_filter == "All":

        filtered_profile = profile_memories

    else:

        filtered_profile = [

            memory

            for memory in profile_memories

            if classify_memory(memory)[0]
            == profile_filter

        ]


    if filtered_profile:

        left_col, right_col = st.columns(2)


        for index, memory in enumerate(
            filtered_profile
        ):

            with (
                left_col
                if index % 2 == 0
                else right_col
            ):

                show_memory(
                    memory,
                    index + 1,
                )


    else:

        st.info(
            "No memories match this category."
        )


else:

    st.info(
        f"No {selected_customer} memory is currently displayed."
    )

    st.caption(
        "Click **Load Customer Memory** in the sidebar "
        "or run a support request to retrieve relevant history."
    )


# =========================================================
# SUPPORT WORKSPACE
# =========================================================

st.divider()

st.subheader(
    "💬 Live Support Workspace"
)

st.caption(
    "Enter a customer issue and let SupportMemory AI "
    "recall history before generating a response."
)


# =========================================================
# QUICK DEMO SCENARIOS
# =========================================================

st.markdown(
    "**⚡ Quick Demo Scenarios**"
)


q1, q2, q3, q4 = st.columns(4)


with q1:

    if st.button(
        "💳 Payment Failure",
        use_container_width=True,
    ):

        st.session_state.customer_message = (
            "My payment is failing again. What should I do?"
        )

        st.rerun()


with q2:

    if st.button(
        "📱 Mobile App",
        use_container_width=True,
    ):

        st.session_state.customer_message = (
            "I am having trouble with the mobile app again."
        )

        st.rerun()


with q3:

    if st.button(
        "🔄 Previous Fix",
        use_container_width=True,
    ):

        st.session_state.customer_message = (
            "What worked for me the last time?"
        )

        st.rerun()


with q4:

    if st.button(
        "💡 My Preference",
        use_container_width=True,
    ):

        st.session_state.customer_message = (
            "How should you guide me when I have a payment problem?"
        )

        st.rerun()


# =========================================================
# CUSTOMER MESSAGE
# =========================================================

message = st.text_area(

    "Customer message",

    key="customer_message",

    height=120,

    placeholder=(
        "Example: My payment is failing again. "
        "What should I do?"
    ),

)


ask_button = st.button(

    "✨ Recall Memory & Generate Personalized Response",

    type="primary",

    use_container_width=True,

)


# =========================================================
# REQUEST PROCESSING
# =========================================================

if ask_button:

    if not message.strip():

        st.warning(
            "Please enter a customer message first."
        )

    else:

        try:


            # =================================================
            # STEP 1 — RECALL
            # =================================================

            with st.status(

                "🔎 Step 1 of 3 — Searching Hindsight memory...",

                expanded=True,

            ):

                retrieved_memories = get_customer_memory(

                    selected_customer,

                    message,

                )


                memories = unique_memories(

                    retrieved_memories

                )


                st.session_state.memories = memories

                st.session_state.profile_memories = memories

                st.session_state.last_query_memories = memories

                st.session_state.recall_count += 1


                st.write(

                    f"Retrieved {len(memories)} relevant memories."

                )


            # =================================================
            # STEP 2 — GENERATE RESPONSE
            # =================================================

            with st.status(

                "🤖 Step 2 of 3 — Personalizing support response...",

                expanded=True,

            ):

                response = generate_support_response(

                    selected_customer,

                    message,

                )


                st.session_state.last_response = response


                st.write(
                    "Response generated using customer history."
                )


            # =================================================
            # STEP 3 — RETAIN
            # =================================================

            with st.status(

                "💾 Step 3 of 3 — Learning from interaction...",

                expanded=True,

            ):

                save_customer_interaction(

                    selected_customer,

                    message,

                    response,

                )


                st.session_state.retain_count += 1


                st.write(
                    "Interaction retained in Hindsight."
                )


            # =================================================
            # SAVE CHAT
            # =================================================

            st.session_state.last_action = (

                "Memory recalled → response personalized → "
                "interaction retained"

            )


            st.session_state.chat_history.append(

                {

                    "customer": selected_customer,

                    "message": message,

                    "response": response,

                }

            )


            st.toast(
                "🧠 Hindsight recalled and learned from the interaction!"
            )


            st.rerun()


        except Exception as e:

            st.error(
                f"Execution Error: {e}"
            )


# =========================================================
# CURRENT HINDSIGHT RECALL
# =========================================================

memories = unique_memories(
    st.session_state.memories
)


st.divider()

st.subheader(
    "🔎 Hindsight Recall"
)


if memories:

    st.caption(
        f"{len(memories)} relevant memories retrieved "
        f"for {selected_customer}."
    )


    # -----------------------------------------------------
    # MEMORY COUNTS
    # -----------------------------------------------------

    counts = get_memory_counts(
        memories
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.metric(
            "All",
            len(memories),
        )


    with c2:

        st.metric(
            "💡 Preferences",
            counts["Preference"],
        )


    with c3:

        st.metric(
            "🛠️ Solutions",
            counts["Successful Solution"],
        )


    with c4:

        st.metric(
            "⚠️ Problems",
            counts["Previous Problem"],
        )


    with c5:

        st.metric(
            "👤 Context",
            counts["Customer Context"],
        )


    st.divider()


    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    filter_options = [

        "All",

        "Preference",

        "Successful Solution",

        "Previous Problem",

        "Customer Context",

    ]


    selected_filter = st.segmented_control(

        "Filter recalled memories",

        filter_options,

        default=st.session_state.active_filter,

        key="memory_filter",

    )


    if selected_filter is None:

        selected_filter = "All"


    st.session_state.active_filter = selected_filter


    # -----------------------------------------------------
    # FILTERED MEMORIES
    # -----------------------------------------------------

    filtered_memories = [

        memory

        for memory in memories

        if (

            selected_filter == "All"

            or classify_memory(memory)[0]
            == selected_filter

        )

    ]


    if filtered_memories:

        left_col, right_col = st.columns(2)


        for index, memory in enumerate(
            filtered_memories
        ):

            with (

                left_col

                if index % 2 == 0

                else right_col

            ):

                show_memory(

                    memory,

                    index + 1,

                )


    else:

        st.info(
            "No memories match the selected filter."
        )


else:

    st.info(
        "No Hindsight memories have been retrieved "
        "for the current request yet."
    )


# =========================================================
# RESPONSE SECTION
# =========================================================

st.divider()

response_col, impact_col = st.columns(
    [2.3, 1]
)


# =========================================================
# AI RESPONSE
# =========================================================

with response_col:

    st.subheader(
        "🤖 Personalized AI Response"
    )


    if st.session_state.last_response:

        st.success(
            "Response generated using customer history."
        )


        with st.container(border=True):

            st.write(
                st.session_state.last_response
            )


        st.caption(
            "📋 Use the copy button inside the code box to copy the response."
        )


        st.code(
            st.session_state.last_response,
            language="text",
        )


    else:

        st.info(
            "The personalized AI response will appear here "
            "after you run a support request."
        )


# =========================================================
# MEMORY IMPACT
# =========================================================

with impact_col:

    st.subheader(
        "🎯 Memory Impact"
    )


    st.metric(
        "Memories Recalled",
        len(memories),
    )


    st.metric(
        "Interactions Learned",
        st.session_state.retain_count,
    )


    if st.session_state.last_response:

        st.success(
            "🧠 Personalization Active"
        )

        st.caption(
            "The response was generated with "
            "customer history available to the agent."
        )

    else:

        st.info(
            "Waiting for request"
        )


# =========================================================
# TABS
# =========================================================

st.divider()


tab_chat, tab_learning, tab_analytics = st.tabs(

    [

        "💬 Conversation History",

        "🔄 Learning Loop",

        "📊 Engine Analytics",

    ]

)


# =========================================================
# CONVERSATION HISTORY
# =========================================================

with tab_chat:

    st.subheader(
        f"💬 Conversation History — {selected_customer}"
    )


    current_chats = [

        chat

        for chat in st.session_state.chat_history

        if chat["customer"] == selected_customer

    ]


    if current_chats:

        st.caption(

            f"{len(current_chats)} interaction(s) "
            "recorded in this session."

        )


        for number, chat in enumerate(

            reversed(current_chats),

            start=1,

        ):

            with st.container(border=True):

                st.caption(
                    f"Interaction {number}"
                )


                st.chat_message(
                    "user"
                ).write(
                    chat["message"]
                )


                st.chat_message(
                    "assistant"
                ).write(
                    chat["response"]
                )


    else:

        st.info(

            "No conversation has been recorded for "

            f"{selected_customer} in this session."

        )


# =========================================================
# LEARNING LOOP
# =========================================================

with tab_learning:

    st.subheader(
        "🔄 How SupportMemory Gets Smarter"
    )

    st.caption(
        "Every interaction follows the Hindsight memory loop."
    )


    loop1, loop2 = st.columns(2)


    with loop1:

        with st.container(border=True):

            st.subheader(
                "1️⃣ Recall"
            )

            st.write(

                "Hindsight searches the customer's historical "
                "memories for information relevant to the new request."

            )

            st.info(

                "Example: previous payment problems and solutions."

            )


    with loop2:

        with st.container(border=True):

            st.subheader(
                "2️⃣ Personalize"
            )

            st.write(

                "The agent uses relevant preferences, problems, "
                "solutions, and customer context."

            )

            st.info(

                "Example: use the customer's preferred response style."

            )


    loop3, loop4 = st.columns(2)


    with loop3:

        with st.container(border=True):

            st.subheader(
                "3️⃣ Respond"
            )

            st.write(

                "The AI generates a support response based on "
                "the customer's current issue and history."

            )

            st.info(

                "Example: reuse a previously successful solution."

            )


    with loop4:

        with st.container(border=True):

            st.subheader(
                "4️⃣ Retain"
            )

            st.write(

                "The new interaction is stored in Hindsight "
                "so future conversations can use it."

            )

            st.success(

                "This is how the agent learns over time."

            )


    # -----------------------------------------------------
    # CURRENT LEARNING STATE
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "🧠 Current Learning State"
    )


    l1, l2, l3 = st.columns(3)


    with l1:

        st.metric(
            "Recalls",
            st.session_state.recall_count,
        )


    with l2:

        st.metric(
            "Interactions Retained",
            st.session_state.retain_count,
        )


    with l3:

        st.metric(
            "Current Memories",
            len(memories),
        )


    st.caption(
        f"Last action: {st.session_state.last_action}"
    )


# =========================================================
# ENGINE ANALYTICS
# =========================================================

with tab_analytics:

    st.subheader(
        "📊 Hindsight Engine Analytics"
    )


    a1, a2, a3, a4 = st.columns(4)


    with a1:

        st.metric(
            "Hindsight Recalls",
            st.session_state.recall_count,
        )


    with a2:

        st.metric(
            "Interactions Retained",
            st.session_state.retain_count,
        )


    with a3:

        st.metric(
            "Current Memories",
            len(memories),
        )


    with a4:

        st.metric(
            "Active Customer",
            selected_customer,
        )


    st.divider()


    st.subheader(
        "🧠 Memory Distribution"
    )


    if memories:

        analytics_counts = get_memory_counts(
            memories
        )


        d1, d2 = st.columns(2)


        with d1:

            st.metric(
                "💡 Preferences",
                analytics_counts["Preference"],
            )

            st.metric(
                "🛠️ Successful Solutions",
                analytics_counts["Successful Solution"],
            )

            st.metric(
                "⚠️ Previous Problems",
                analytics_counts["Previous Problem"],
            )


        with d2:

            st.metric(
                "👤 Customer Context",
                analytics_counts["Customer Context"],
            )

            st.metric(
                "🧠 Other Memories",
                analytics_counts["Customer Memory"],
            )


    else:

        st.info(
            "Run a support request to populate memory analytics."
        )


    st.divider()


    st.subheader(
        "⚙️ Current System State"
    )


    state1, state2 = st.columns(2)


    with state1:

        st.info(

            f"**Customer:** {selected_customer}\n\n"

            f"**Type:** {customer['type']}\n\n"

            f"**Status:** {customer['status']}"

        )


    with state2:

        st.success(

            "**Hindsight:** Connected\n\n"

            "**Memory:** Active\n\n"

            f"**Last Action:** {st.session_state.last_action}"

        )


    st.divider()


    st.subheader(
        "🔧 Architecture"
    )


    st.write(

        "Customer Message → Hindsight Recall → "
        "AI Personalization → Support Response → "
        "Hindsight Retain"

    )


# =========================================================
# HACKATHON DEMO STORY
# =========================================================

st.divider()

st.subheader(
    "🎬 Hackathon Demo Story"
)


demo1, demo2, demo3 = st.columns(3)


with demo1:

    with st.container(border=True):

        st.subheader(
            "① First Interaction"
        )

        st.write(
            "Customer reports a problem."
        )

        st.caption(
            "The agent retrieves relevant history "
            "and responds."
        )


with demo2:

    with st.container(border=True):

        st.subheader(
            "② Hindsight Learns"
        )

        st.write(
            "The interaction is retained."
        )

        st.caption(
            "The new information becomes part of "
            "the customer's long-term memory."
        )


with demo3:

    with st.container(border=True):

        st.subheader(
            "③ Future Interaction"
        )

        st.write(
            "Customer returns with a similar problem."
        )

        st.caption(
            "The agent recalls previous context "
            "and provides a more personalized response."
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(

    "🧠 SupportMemory AI • Persistent AI Customer Support "
    "• Powered by Hindsight + Streamlit"

)