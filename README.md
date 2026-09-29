# 🤖 MIMI — SupportMemory AI

### Memory-Powered AI Customer Support Agent

MIMI is an AI-powered customer support agent that remembers a customer's previous problems, successful solutions, unresolved issues, and communication preferences.

Instead of making customers repeat their problem every time they contact support, MIMI uses **Hindsight long-term memory** to recall relevant information from previous interactions and provide more personalized support.

---

## 🌟 Overview

Traditional customer-support systems often treat every conversation as a new conversation.

A customer may have already explained:

- What problem they experienced
- Which troubleshooting steps they tried
- What solution worked previously
- Their preferred communication style
- Whether an issue is still unresolved

When the customer contacts support again, they may have to explain everything again.

### MIMI solves this problem by giving the AI agent long-term memory.

MIMI can remember customer-specific information across interactions and use that information when handling future support requests.

```text
Customer
    │
    ▼
┌──────────────────────┐
│      MIMI 🤖         │
│ AI Support Agent     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Hindsight Memory   │
│                      │
│ Problems             │
│ Solutions            │
│ Preferences          │
│ Previous interactions│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Personalized Support │
│ Response             │
└──────────────────────┘
```

---

# 🎯 Problem Statement

Customer-support agents often lose important context between conversations.

A customer may have already explained:

- What problem they experienced
- Which troubleshooting steps they tried
- What solution worked previously
- Their preferred communication style
- Whether an issue is still unresolved

When the customer contacts support again, they may have to explain everything again.

MIMI solves this problem by using **Hindsight long-term memory** to remember relevant customer information and use it in future support conversations.

---

# 💡 Our Solution

MIMI combines:

- Large Language Models
- Hindsight long-term memory
- Customer-specific context retrieval
- Personalized response generation
- Streamlit interface

The important part of the system is that memory is not treated only as simple conversation history.

Hindsight provides the long-term memory layer that allows MIMI to recall useful information from previous customer interactions.

---

# 🧠 Why Hindsight?

Hindsight provides the long-term memory for MIMI.

MIMI can store and recall information such as:

- Previous customer problems
- Successful troubleshooting solutions
- Customer preferences
- Relevant historical context
- Unresolved issues

This allows MIMI to provide support based on previous interactions instead of starting from zero every time.

---

# ✨ Key Features

## 1. 🧠 Long-Term Customer Memory

MIMI remembers useful information from previous support interactions.

Examples:

- Previous problems
- Previous solutions
- Customer preferences
- Unresolved issues

---

## 2. 👤 Customer-Specific Context

MIMI retrieves information relevant to the selected customer.

This helps prevent unrelated customer information from being used when generating a response.

---

## 3. 🔧 Solution Recall

MIMI can remember which troubleshooting solution worked previously.

For example:

```text
Problem:
UPI payment repeatedly failed.

Previous solution:
Clear the payment app cache and retry.

Future interaction:
MIMI can recall this successful troubleshooting step.
```

---

## 4. 💬 Personalized Communication

MIMI remembers how different customers prefer to receive support.

| Customer | Preference |
|----------|------------|
| Rahul | Step-by-step technical instructions |
| Priya | Short and direct responses |
| Arjun | Detailed explanations |
| Sneha | Email-style updates with clear delivery timelines |

MIMI can use these preferences when generating future responses.

---

## 5. 🔄 Continuous Memory

Useful information from support interactions can be stored for future conversations.

This creates a continuous memory cycle:

```text
Conversation
     ↓
Useful Information
     ↓
Hindsight Memory
     ↓
Future Conversation
     ↓
Personalized Support
```

---

# 🏗️ System Architecture

```text
                    ┌───────────────────┐
                    │      Customer     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Streamlit UI    │
                    │                   │
                    │ Customer Support  │
                    │    Interface      │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │       MIMI        │
                    │  AI Support Agent │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
          ┌─────────────────┐   ┌─────────────────┐
          │    Hindsight    │   │     Groq LLM    │
          │ Long-Term       │   │ Response        │
          │ Memory          │   │ Generation      │
          └────────┬────────┘   └────────┬────────┘
                   │                     │
                   └──────────┬──────────┘
                              ▼
                    ┌───────────────────┐
                    │ Personalized      │
                    │ Support Response  │
                    └───────────────────┘
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core application |
| Streamlit | Web interface |
| Groq | AI response generation |
| Hindsight | Long-term AI memory |
| SQLite / JSON | Application data |
| GitHub | Source-code management |
| Streamlit Community Cloud | Deployment |

---

# 📁 Project Structure

```text
SupportMemoryAI/
│
├── app/
│   └── dashboard.py
│
├── agent/
│   └── support_agent.py
│
├── data/
│   └── customer_data.py
│
├── utils/
│   └── hindsight_service.py
│
├── .env
├── .gitignore
├── requirements.txt
├── main.py
└── README.md
```

---

# 🔐 Environment Variables

MIMI requires credentials for Hindsight and the LLM service.

For local development, create a `.env` file:

```env
HINDSIGHT_API_KEY=your_hindsight_api_key
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder values with your actual API credentials.

### ⚠️ Important

Never commit `.env` or API keys to GitHub.

Your `.gitignore` should include:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/CHINNAPAPOLLAMANASAREDDY/SupportMemoryAI.git
```

Move into the project directory:

```bash
cd SupportMemoryAI
```

---

## 2. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run MIMI Locally

Start the Streamlit application:

```bash
streamlit run app/dashboard.py
```

The application will open in your browser.

The default local address is:

```text
http://localhost:8501
```

---

# ☁️ Deployment

MIMI is deployed using **Streamlit Community Cloud**.

The application uses:

```text
Repository:
CHINNAPAPOLLAMANASAREDDY/SupportMemoryAI

Branch:
master

Main file:
app/dashboard.py
```

For deployment, API credentials should be added through Streamlit Secrets rather than committed to the repository.

Example:

```toml
HINDSIGHT_API_KEY = "your_hindsight_api_key"
HINDSIGHT_BASE_URL = "https://api.hindsight.vectorize.io"
GROQ_API_KEY = "your_groq_api_key"
```

---

# 🧠 Hindsight Memory Implementation

Hindsight provides the long-term memory layer for MIMI.

MIMI uses memory to:

### Retain

Store useful information from customer-support interactions.

### Recall

Retrieve relevant information from previous interactions.

### Reflect

Use relevant memory when generating a personalized support response.

The memory cycle is:

```text
Customer Interaction
        ↓
      Retain
        ↓
Hindsight Memory
        ↓
      Recall
        ↓
Relevant Customer Context
        ↓
      Reflect
        ↓
Personalized Response
```

---

# 🔄 Example of Memory Improvement

### First Conversation

```text
Rahul:
"My UPI payment keeps failing."

MIMI:
"Let's troubleshoot your payment issue."

Solution:
Clear the payment application's cache and retry.
```

The useful information is stored in Hindsight.

### Later Conversation

```text
Rahul:
"I'm having another payment problem."

MIMI:
"Previously, clearing your payment app's cache
helped resolve a UPI issue. Let's try that first..."
```

MIMI can therefore use information learned from the previous interaction instead of starting from zero.

---

# 👥 Customer Examples

## Rahul

**Previous issue:** UPI payment failures

**Successful solution:** Clear the payment app cache and retry

**Preference:** Step-by-step technical instructions

---

## Priya

**Previous issue:** Card payment declined

**Successful solution:** Check the transaction limit and retry

**Preference:** Short and direct responses

---

## Arjun

**Previous issue:** Login problem

**Successful solution:** Password reset

**Preference:** Detailed explanations

---

## Sneha

**Previous issue:** Delayed delivery

**Successful solution:** Updated tracking information

**Preference:** Email-style updates with clear delivery timelines

---

# 🎥 Demo Flow

A simple MIMI demonstration can follow this sequence:

1. Select a customer.
2. Enter a support issue.
3. MIMI retrieves relevant customer memory.
4. MIMI generates a personalized response.
5. Show the previous information that MIMI remembered.
6. Continue the conversation and demonstrate how the remembered context can be used again.

The key idea demonstrated is:

```text
Past Interaction
       ↓
Hindsight Memory
       ↓
Future Interaction
       ↓
Personalized Support
```

---

# 🎯 Project Goals

MIMI is designed to:

- Reduce repetitive customer explanations
- Preserve useful support history
- Recall previously successful solutions
- Personalize communication
- Maintain relevant customer context
- Demonstrate practical long-term AI memory

---

# 🚧 Current Limitations

The current version is a prototype focused on demonstrating memory-powered customer support.

Current limitations include:

- Customer data is based on a controlled demonstration dataset.
- Customer isolation is implemented at the application level.
- The system is not connected to a production CRM or ticket-management platform.
- Production-grade authentication and authorization are not implemented.
- The current application focuses primarily on support conversations.

---

# 🔮 Future Enhancements

Possible future improvements include:

- CRM integration
- Automatic support-ticket history
- Customer sentiment tracking
- Human-agent escalation
- Email and WhatsApp support
- Voice-based support
- Support analytics
- Company knowledge-base integration

---

# 🌐 Project Links

### GitHub Repository

https://github.com/CHINNAPAPOLLAMANASAREDDY/SupportMemoryAI

### Live Demo

Add your Streamlit Community Cloud URL here:

```text
YOUR_STREAMLIT_APP_URL
```

### Demo Video

Add your final demo video URL here:

```text
YOUR_DEMO_VIDEO_URL
```

---

# 🏆 Hackathon Focus

MIMI demonstrates how long-term AI memory can improve customer support.

The core concept is:

```text
Memory
   +
AI Reasoning
   +
Personalization
   +
Customer Support
```

Hindsight provides the long-term memory layer that allows MIMI to use relevant information from previous customer interactions.

---

# 👩‍💻 Project

**SupportMemory AI**

Customer-facing AI agent:

**MIMI 🤖**

Built with:

- Python
- Streamlit
- Groq
- Hindsight

---

# 📄 License

This project is currently intended as a hackathon prototype.

Add an open-source license here if you decide to release the project under a specific license.

---

## ⭐ MIMI in One Sentence

> MIMI is a memory-powered AI customer-support agent that remembers what happened before and uses that context to provide more personalized support.
