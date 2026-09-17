# Veridian Corp — Internal Service Agent (IT Support)

> **Assignment 2: Internal Service Agent (IT Support)**  
> **Course / Academic Prototype:** B.Tech Student Implementation  
> **Target Company:** Veridian Corp (Exercise Timeline: 21 Sep – 25 Sep 2026)

---

## 1. Project Title
**Veridian Corp Internal IT Support Agent** — A rule-based, policy-grounded service agent built with Python and Streamlit.

---

## 2. Objective
To build a lightweight, deterministic internal IT service agent that:
1. Ingests employee IT support requests.
2. Identifies the issue category.
3. Matches the issue strictly with the corresponding Veridian Corp Knowledge Base policy (KB-01 to KB-10 and Asset Management Policy).
4. Determines the correct decision and recommended action.
5. Provides a concise, grounded explanation.
6. Evaluates and displays all 15 employee requests from the assignment dataset.
7. Leverages historical ticket queue records (TK-1042 to TK-1051) for precedent and consistency.

---

## 3. Problem Statement
In enterprise environments like Veridian Corp, IT support teams face a high volume of repetitive queries (e.g., password resets, VPN expiry, guest Wi-Fi) alongside critical items (e.g., phishing alerts, hardware replacement sign-offs). Without an automated triage system, tickets get misrouted, security incidents are delayed, and employees experience long turnaround times. 

The objective is to triage requests immediately based solely on company policies, resolving self-service inquiries directly and accurately escalating complex cases to IT, Security, or Finance.

---

## 4. Technologies Used
- **Language:** Python 3.10+
- **Frontend / Framework:** Streamlit (v1.30+)
- **Architecture:** Pure rule-based & keyword-pattern matching engine
- **Storage:** Static Python dictionaries and lists in `data.py`
- **Dependencies:** Only `streamlit` (No database, no Docker, no external LLM API key required)

---

## 5. How the Agent Works
1. **Input Intake:** An employee inputs an IT inquiry via text or selects a pre-set request.
2. **Pre-processing & Normalization:** Text is cleaned and analyzed for key indicators (e.g., keyword triggers, numerical counts such as password attempts or laptop age).
3. **Policy & Rule Matching:**
   - **Vagueness Detection:** Flags queries lacking actionable details (e.g., REQ-15: *"hey can you help, its not working"*) to request further information.
   - **Security Escalation:** Identifies phishing/malware threats (KB-09) and immediately halts forwarding to peers.
   - **Access & Lockouts:** Evaluates threshold logic for password lockouts (KB-01: self-service for <5 attempts; manual IT unlock for 5+ attempts).
   - **Role & Authorization Checks:** Applies role-specific constraints (KB-02: contractors require manager approval for VPN; KB-10: remote workers >3 days/week require manager sign-off and Finance processing).
   - **Hardware Refresh Cycles:** Cross-checks 3-year replacement eligibility (KB-03) with the 4-year standard refresh cycle requiring Finance sign-off (Asset Management Policy).
4. **Historical Cross-Reference:** Looks up matching past tickets from the Ticket Queue (e.g., closed ticket `TK-1042` for expired VPN or `TK-1050` for admin access without justification) to ensure consistency.
5. **Output Delivery:** Returns Category, Policy ID, Decision Type, Recommended Action, Reason, and Precedent note.

---

## 6. Project Structure
```
sales agent/
├── app.py              # Streamlit user interface and rule-based triage engine
├── data.py             # Knowledge base policies (KB-01..10, Asset Policy), 15 requests, 10 tickets
├── requirements.txt    # Project dependencies (streamlit)
└── README.md           # Documentation and viva presentation guide
```

---

## 7. How to Install
Ensure Python is installed on your computer, then install Streamlit:

```bash
pip install -r requirements.txt
```

---

## 8. How to Run
Run the Streamlit application with:

```bash
streamlit run app.py
```
*(Or on Windows if `streamlit` is not in your system PATH:)*
```bash
python -m streamlit run app.py
```

The web application will automatically open in your default browser at `http://localhost:8501`.

---

## 9. Example Input & Output

### Example 1: Self-Service VPN Renewal
- **Input:** `"My VPN credentials expired"`
- **Category:** `VPN Access`
- **Policy:** `KB-02 (VPN Access)`
- **Decision:** `Resolve / Self-Service`
- **Recommended Action:** `Employee should renew VPN credentials via the self-service access portal.`
- **Reason:** `Under KB-02, VPN credentials expire every 90 days and must be renewed by the employee.`
- **Precedent:** `TK-1042: VPN credential expired — Resolved (closed).`

### Example 2: Security Escalation
- **Input:** `"I got a phishing email asking for login and forwarded it to my team"`
- **Category:** `Security Incident`
- **Policy:** `KB-09 (Security Incident Reporting)`
- **Decision:** `Route to Security`
- **Recommended Action:** `CRITICAL: Employee must immediately STOP forwarding the email to colleagues. Report immediately to security@veridian-corp.example.`
- **Reason:** `Under KB-09, any suspected phishing attempt must be reported to security immediately and must not be forwarded.`
- **Precedent:** `TK-1048: Phishing email reported — Escalated to Security.`

---

## 10. Limitations
1. **Scope Restricted to Provided Policies:** The agent strictly applies Veridian Corp policies provided in the assignment; it does not assume external company norms or third-party tools.
2. **Deterministic Pattern Matching:** Uses keyword and rule heuristics rather than probabilistic LLMs to guarantee 100% policy adherence and zero hallucinations.
3. **In-Memory Storage:** Data resides in `data.py` without a persistent relational database, matching the scope of a lightweight academic prototype.

---

## 11. How to Explain This Project to the Teacher (Viva Guide)

### Problem
*"At Veridian Corp, employees submit varied IT requests ranging from simple self-service tasks to critical security incidents. Triage is often slow, and manual errors can lead to security risks or policy violations."*

### Solution
*"We built an internal IT Support Service Agent using Python and Streamlit. The agent automatically classifies employee inquiries, applies the relevant Veridian Corp policy, checks historical ticket precedents, and produces an actionable decision with clear reasoning."*

### Technology
*"We chose Python and Streamlit because they provide an interactive, browser-based UI with minimal code. We intentionally avoided heavy external frameworks or paid APIs so the project remains deterministic, fast, zero-cost, and 100% reproducible."*

### Workflow
1. *Employee inputs an issue or selects from the assignment's 15 requests.*
2. *The rule engine detects keywords, checks numerical thresholds (such as 6 failed password attempts or laptop age), and matches the issue against Knowledge Base policies (KB-01 to KB-10).*
3. *The system outputs the Category, Relevant Policy, Decision, Action, and Historical Precedent from previous tickets.*

### Example
*"When Sanjay Oberoi states his VPN credentials expired (REQ-05), the agent matches KB-02, notes that VPN credentials expire every 90 days, references historical ticket TK-1042, and marks it as self-service renewal without wasting IT engineering hours."*

### Why it Follows the Assignment
- Strictly uses only KB-01 through KB-10 and the Asset Management Policy extract from the PDF.
- Correctly handles all 15 employee requests (e.g., REQ-03 routes to IT because 6 failed attempts exceeds the 5-attempt limit; REQ-08 immediately halts forwarding phishing emails; REQ-15 asks for clarification).
- Accurately integrates the 10 historical tickets (TK-1042 to TK-1051) to provide context for decisions.
- Contains no invented policies, no commercial bloat, and runs cleanly with a single command.
