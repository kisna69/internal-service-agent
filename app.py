"""
app.py - Veridian Corp Internal IT Support Agent
Assignment 2: Internal Service Agent (IT Support)
A simple, rule-based Streamlit application for processing employee IT requests
according to Veridian Corp knowledge base policies and historical ticket records.
"""

import re
import streamlit as st
from data import POLICIES, EMPLOYEE_REQUESTS, TICKET_QUEUE


# ---------------------------------------------------------------------------
# Rule-Based Classification & Decision Engine
# ---------------------------------------------------------------------------
def analyze_request(query: str) -> dict:
    """
    Analyzes an employee IT request string and matches it to the appropriate
    Veridian Corp policy, decision type, recommended action, and historical precedent.
    """
    text = query.strip()
    lower = text.lower()

    # Rule 1: Check for extremely vague or empty requests (e.g., REQ-15)
    if not text or len(text.split()) < 3 or lower in [
        "help", "its not working", "it's not working", "not working",
        "hey can you help, its not working", "need help", "broken"
    ]:
        return {
            "category": "Unspecified / General Inquiry",
            "policy_id": "N/A",
            "policy_title": "General IT Intake",
            "decision": "Ask for More Information",
            "action": "Request employee to specify the device, application, error message, and steps taken.",
            "reason": (
                "The request is too vague to determine the issue. Employees must provide details "
                "such as device type, software name, or error codes before IT can take action."
            ),
            "precedent": "None — requires clarification."
        }

    # Rule 2: Phishing / Malware / Security Incidents (KB-09)
    if any(k in lower for k in ["phish", "malware", "unauthorized", "suspicious email", "asking for my login"]):
        forwarding_warning = ""
        if "forward" in lower:
            forwarding_warning = "CRITICAL: Employee must immediately STOP forwarding the email to colleagues. "
        return {
            "category": "Security Incident",
            "policy_id": "KB-09",
            "policy_title": POLICIES["KB-09"]["title"],
            "decision": "Route to Security",
            "action": f"{forwarding_warning}Report immediately to security@veridian-corp.example and flag for investigation.",
            "reason": (
                "Under KB-09, any suspected phishing or unauthorized access attempt must be reported "
                "to security@veridian-corp.example immediately and must NOT be forwarded to other employees."
            ),
            "precedent": "TK-1048: Phishing email reported — Escalated to Security — under investigation (active)."
        }

    # Rule 3: Password Reset & Account Lockout (KB-01)
    if any(k in lower for k in ["password", "locked out", "lock out", "failed attempt"]):
        # Extract number of failed attempts if mentioned
        attempts_match = re.search(r"(\d+)\s*(?:times|failed|attempts)", lower)
        failed_count = int(attempts_match.group(1)) if attempts_match else None

        if (failed_count and failed_count >= 5) or "locked out" in lower or "6 times" in lower:
            return {
                "category": "Password Reset",
                "policy_id": "KB-01",
                "policy_title": POLICIES["KB-01"]["title"],
                "decision": "Route to IT",
                "action": "IT technician must unlock the account manually. No approval required.",
                "reason": (
                    "Under KB-01, employees can self-reset passwords, but if locked out after 5 or more "
                    "failed attempts, IT must unlock the account manually. No approval is required."
                ),
                "precedent": "TK-1049: Password reset — Resolved (closed)."
            }
        else:
            return {
                "category": "Password Reset",
                "policy_id": "KB-01",
                "policy_title": POLICIES["KB-01"]["title"],
                "decision": "Resolve / Self-Service",
                "action": "Guide employee to reset their password via the self-service portal.",
                "reason": (
                    "Under KB-01, employees can reset their own password via the self-service portal at any time."
                ),
                "precedent": "TK-1049: Password reset — Resolved (closed)."
            }

    # Rule 4: VPN Access & Credentials (KB-02)
    if "vpn" in lower:
        if any(k in lower for k in ["contractor", "temp", "vendor", "new contractor"]):
            return {
                "category": "VPN Access",
                "policy_id": "KB-02",
                "policy_title": POLICIES["KB-02"]["title"],
                "decision": "Manager Approval Required",
                "action": "Submit contractor access request form with manager approval.",
                "reason": (
                    "Under KB-02, VPN access is automatic only for full-time employees. "
                    "Contractors require manager approval submitted via the access request form."
                ),
                "precedent": "Active contractor onboarding policy under KB-02."
            }
        elif any(k in lower for k in ["expired", "credentials", "renew", "stopped working"]):
            return {
                "category": "VPN Access",
                "policy_id": "KB-02",
                "policy_title": POLICIES["KB-02"]["title"],
                "decision": "Resolve / Self-Service",
                "action": "Employee should renew VPN credentials via the self-service access portal.",
                "reason": (
                    "Under KB-02, VPN credentials expire every 90 days and must be renewed by the employee."
                ),
                "precedent": "TK-1042: VPN credential expired — Resolved (closed)."
            }
        else:
            return {
                "category": "VPN Access",
                "policy_id": "KB-02",
                "policy_title": POLICIES["KB-02"]["title"],
                "decision": "Resolve / Self-Service",
                "action": "Full-time employees have automatic VPN access. If credentials expired, renew them.",
                "reason": "VPN access is granted automatically to full-time staff; credentials expire every 90 days.",
                "precedent": "TK-1042: VPN credential expired — Resolved (closed)."
            }

    # Rule 5: Guest Wi-Fi Access (KB-07)
    if any(k in lower for k in ["guest wi-fi", "guest wifi", "wi-fi for visitor", "wifi for visitor", "guest visiting"]):
        return {
            "category": "Guest Wi-Fi",
            "policy_id": "KB-07",
            "policy_title": POLICIES["KB-07"]["title"],
            "decision": "Resolve / Self-Service",
            "action": "Direct employee to the front-desk kiosk to generate 24-hour guest credentials. No ticket needed.",
            "reason": (
                "Under KB-07, guest Wi-Fi credentials are valid for 24 hours and can be generated by "
                "any employee from the front-desk kiosk. No IT ticket is required."
            ),
            "precedent": "TK-1051: Guest Wi-Fi issued — Resolved (closed)."
        }

    # Rule 6: Hardware & Laptop Replacement / Troubleshooting (KB-03 & Asset Policy)
    if any(k in lower for k in ["laptop", "screen", "flicker", "refresh cycle", "hardware failure", "dead", "won't turn on"]):
        # Check years
        years_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years|yrs)", lower)
        years = float(years_match.group(1)) if years_match else None

        if "flicker" in lower or "fix not a replacement" in lower or (years and years < 3 and "dead" not in lower):
            return {
                "category": "Laptop Troubleshooting",
                "policy_id": "KB-03 & Asset Management",
                "policy_title": "KB-03 & Asset Management Policy",
                "decision": "Troubleshooting Required",
                "action": "Assign an IT hardware technician to inspect and repair the hardware issue.",
                "reason": (
                    f"Laptop is {'about ' + str(years) + ' years old' if years else 'under 3 years old'} "
                    "and not eligible for scheduled replacement (standard refresh is 4 years per Asset Policy; "
                    "replacement eligibility starts at 3 years per KB-03). Physical hardware diagnostics/repair needed."
                ),
                "precedent": "TK-1043 is an approved 3.2-year-old replacement; 2-year devices receive repair first."
            }
        else:
            return {
                "category": "Laptop Replacement",
                "policy_id": "KB-03 & Asset Management",
                "policy_title": "KB-03 & Asset Management Policy",
                "decision": "Route to IT",
                "action": "Log laptop replacement request for IT approval and route to Finance for sign-off.",
                "reason": (
                    "Under KB-03, laptops are eligible for replacement after 3 years or earlier for verified hardware failure. "
                    "Under the Asset Management Policy, hardware follows a 4-year cycle, so early replacement outside 4 years "
                    "requires Finance sign-off in addition to IT approval."
                ),
                "precedent": "TK-1043: Laptop replacement (3.2 yrs old) — Approved — pending fulfillment (active)."
            }

    # Rule 7: Software Installation & Extensions (KB-04)
    if any(k in lower for k in ["software", "install", "extension", "catalog", "tool that's not", "browser extension"]):
        if any(k in lower for k in ["not in", "non-catalog", "extension", "not in the software catalog", "approval to install"]):
            return {
                "category": "Software Installation",
                "policy_id": "KB-04",
                "policy_title": POLICIES["KB-04"]["title"],
                "decision": "Security Review Required",
                "action": "Submit software details for IT Security review. Review takes 3–5 business days.",
                "reason": (
                    "Under KB-04, non-catalog software and browser extensions require IT Security review, "
                    "which takes 3–5 business days."
                ),
                "precedent": "TK-1044: Non-catalog software request — Pending Security review (active)."
            }
        else:
            return {
                "category": "Software Installation",
                "policy_id": "KB-04",
                "policy_title": POLICIES["KB-04"]["title"],
                "decision": "Resolve / Self-Service",
                "action": "Direct employee to install standard software directly from the approved software catalog.",
                "reason": "Standard software listed in the approved catalog can be self-installed by the employee.",
                "precedent": "Catalog self-installations do not require IT tickets."
            }

    # Rule 8: Printer Troubleshooting (KB-05)
    if any(k in lower for k in ["printer", "print", "spooler", "paper jam"]):
        return {
            "category": "Printer Troubleshooting",
            "policy_id": "KB-05",
            "policy_title": POLICIES["KB-05"]["title"],
            "decision": "Troubleshooting Required",
            "action": "Check printer queue and restart print spooler. If issue persists, log ticket with printer asset tag.",
            "reason": (
                "Under KB-05, users must first check the printer queue and restart the print spooler. "
                "If the issue persists, a ticket must be logged with the printer's asset tag."
            ),
            "precedent": "TK-1046: Printer paper jam, floor 2 — Resolved (closed)."
        }

    # Rule 9: Email Mailbox Quota (KB-06)
    if any(k in lower for k in ["mailbox", "quota", "can't send email", "cannot send email", "mailbox is full"]):
        if any(k in lower for k in ["increase", "more space", "higher quota", "beyond 25gb"]):
            return {
                "category": "Email Mailbox Quota",
                "policy_id": "KB-06",
                "policy_title": POLICIES["KB-06"]["title"],
                "decision": "Manager Approval Required",
                "action": "Obtain manager approval for quota increase. Note: quota increases are strictly capped at 50GB.",
                "reason": (
                    "Under KB-06, default quota is 25GB. Quota increases beyond 25GB require manager approval "
                    "and are capped at 50GB."
                ),
                "precedent": "TK-1045: Mailbox quota increase — Approved at 35GB (closed)."
            }
        else:
            return {
                "category": "Email Mailbox Quota",
                "policy_id": "KB-06",
                "policy_title": POLICIES["KB-06"]["title"],
                "decision": "Resolve / Self-Service",
                "action": "Instruct employee to archive old emails. If an increase beyond 25GB is needed, request manager approval.",
                "reason": (
                    "Under KB-06, default mailbox quota is 25GB. Employees nearing quota should archive old mail. "
                    "Increases beyond 25GB require manager approval (capped at 50GB)."
                ),
                "precedent": "TK-1045: Mailbox quota increase — Approved at 35GB (closed)."
            }

    # Rule 10: Expense Software Access (KB-08)
    if any(k in lower for k in ["expense", "expense tool", "expense management"]):
        return {
            "category": "Expense Software Access",
            "policy_id": "KB-08",
            "policy_title": POLICIES["KB-08"]["title"],
            "decision": "Route to Finance",
            "action": "Verify with Finance whether an account exists. IT can only assist with technical login once an account is created by Finance.",
            "reason": (
                "Under KB-08, access to the expense management tool is granted by Finance, not IT. "
                "IT can only assist with login/technical issues once an account already exists."
            ),
            "precedent": "REQ-12: Awaiting screenshot/Finance account verification."
        }

    # Rule 11: Work-From-Home Equipment (KB-10)
    if any(k in lower for k in ["work from home", "working from home", "remote", "wfh", "monitor", "chair", "home office"]):
        return {
            "category": "Work-From-Home Equipment",
            "policy_id": "KB-10",
            "policy_title": POLICIES["KB-10"]["title"],
            "decision": "Route to Finance",
            "action": "Employee must obtain manager sign-off and submit to Finance for allowance processing. IT ships after approval.",
            "reason": (
                "Under KB-10, employees working remotely >3 days/week are eligible for a one-time home office allowance. "
                "Requires manager sign-off and Finance processing. IT only handles equipment shipping once approved."
            ),
            "precedent": "TK-1047: Home office equipment request — Pending Finance (active)."
        }

    # Rule 12: Admin Access / Server Privileges
    if any(k in lower for k in ["admin access", "server access", "admin rights", "root access"]):
        return {
            "category": "Admin Access",
            "policy_id": "IT Security & Access Control",
            "policy_title": "Access Control & Business Justification",
            "decision": "Manager Approval Required",
            "action": "Require formal access request with documented business justification and manager approval.",
            "reason": (
                "Administrative and privileged server access requires formal business justification and manager sign-off. "
                "Urgent verbal or unapproved requests are rejected per corporate security standards."
            ),
            "precedent": "TK-1050: Admin access request — Rejected — no business justification provided (closed)."
        }

    # Fallback / Default
    return {
        "category": "General IT Inquiry",
        "policy_id": "N/A",
        "policy_title": "General IT Support",
        "decision": "Route to IT",
        "action": "Assign to Tier-1 IT Support for preliminary assessment and policy matching.",
        "reason": "Request does not match a specific self-service policy keyword. IT technician review required.",
        "precedent": "General IT ticketing queue."
    }


# ---------------------------------------------------------------------------
# Streamlit Interface
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Veridian Corp - IT Support Agent",
    page_icon="🖥️",
    layout="wide"
)

# Custom header
st.title("🖥️ Veridian Corp — Internal IT Support Agent")
st.caption("Assignment 2: Internal Service Agent (IT Support) | Academic Prototype")

# Top overview cards
col_summary1, col_summary2, col_summary3 = st.columns(3)
with col_summary1:
    st.metric(label="Knowledge Base Policies", value=len(POLICIES))
with col_summary2:
    st.metric(label="Assignment Requests", value=len(EMPLOYEE_REQUESTS))
with col_summary3:
    active_count = sum(1 for t in TICKET_QUEUE if t["is_active"])
    st.metric(label="Active Queue Tickets", value=active_count, delta=f"{len(TICKET_QUEUE) - active_count} Closed")

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🤖 IT Support Agent", "📋 Employee Requests (15)", "🎫 Ticket Queue (Historical Context)"])


# ---------------------------------------------------------------------------
# TAB 1: IT Support Agent
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Interactive Request Analyzer")
    st.write(
        "Enter an employee IT problem or select a pre-set sample below to classify the request, "
        "match it with the relevant Veridian Corp policy, and determine the recommended action."
    )

    # Sample selector for easy demonstration
    sample_options = ["-- Select a sample query (optional) --"] + [
        f"{r['request_id']} ({r['employee']}): {r['request_text']}" for r in EMPLOYEE_REQUESTS
    ] + [
        "Custom Sample: My VPN credentials expired",
        "Custom Sample: I need to install a standard text editor from catalog",
        "Custom Sample: Can someone give me guest Wi-Fi for 2 days?"
    ]

    selected_sample = st.selectbox("Quick-test sample requests:", sample_options)

    # Pre-fill text area based on sample selection
    default_text = "My VPN credentials expired"
    if selected_sample != "-- Select a sample query (optional) --":
        if ":" in selected_sample:
            default_text = selected_sample.split(":", 1)[1].strip()
        else:
            default_text = selected_sample

    user_input = st.text_area("Employee IT Request:", value=default_text, height=90)

    if st.button("Analyze Request", type="primary"):
        if not user_input.strip():
            st.warning("Please enter a request before analyzing.")
        else:
            result = analyze_request(user_input)

            st.markdown("### Analysis Result")

            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.markdown(f"**Category:** `{result['category']}`")
                st.markdown(f"**Relevant Policy:** `{result['policy_id']}` — {result['policy_title']}")
                
                # Decision badge
                dec = result['decision']
                if dec == "Resolve / Self-Service":
                    st.success(f"**Decision:** {dec}")
                elif "Security" in dec:
                    st.error(f"**Decision:** {dec}")
                elif "Finance" in dec or "Approval" in dec:
                    st.warning(f"**Decision:** {dec}")
                elif dec == "Ask for More Information":
                    st.info(f"**Decision:** {dec}")
                else:
                    st.info(f"**Decision:** {dec}")

            with col_res2:
                st.markdown(f"**Recommended Action:**\n{result['action']}")
                st.markdown(f"**Short Reason:**\n{result['reason']}")
                st.markdown(f"**Historical Precedent:**\n_{result['precedent']}_")

    # Knowledge Base Policy Reference Expander
    with st.expander("📖 View Veridian Corp Knowledge Base Policies (Reference)"):
        for pid, pdata in POLICIES.items():
            st.markdown(f"**{pid}: {pdata['title']}** ({pdata['category']})")
            st.write(pdata['content'])
            st.markdown("---")


# ---------------------------------------------------------------------------
# TAB 2: Employee Requests
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("All 15 Employee Requests from Assignment")
    st.write(
        "The table below shows all 15 employee requests from the assignment, processed strictly "
        "according to the Veridian Corp Knowledge Base and Asset Management policies."
    )

    # Filter option by decision
    all_decisions = ["All"] + sorted(list(set(r["decision"] for r in EMPLOYEE_REQUESTS)))
    selected_filter = st.selectbox("Filter by Decision Type:", all_decisions)

    filtered_requests = [
        r for r in EMPLOYEE_REQUESTS
        if selected_filter == "All" or r["decision"] == selected_filter
    ]

    # Display as a clean, structured table
    table_data = []
    for r in filtered_requests:
        table_data.append({
            "Request ID": r["request_id"],
            "Employee": r["employee"],
            "Category": r["category"],
            "Relevant Policy": r["relevant_policy"],
            "Decision": r["decision"],
            "Reason": r["reason"]
        })

    st.dataframe(table_data, width="stretch", hide_index=True)

    st.markdown("---")
    st.subheader("Inspect Specific Request")
    req_ids = [r["request_id"] for r in EMPLOYEE_REQUESTS]
    selected_req_id = st.selectbox("Choose a Request to view complete details:", req_ids)

    req_detail = next(r for r in EMPLOYEE_REQUESTS if r["request_id"] == selected_req_id)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Request ID:** `{req_detail['request_id']}`")
        st.markdown(f"**Employee:** {req_detail['employee']} ({req_detail['email']})")
        st.markdown(f"**Date Opened:** {req_detail['date_opened']}")
        st.markdown(f"**Original Text:** _{req_detail['request_text']}_")
        st.markdown(f"**Initial Action Taken So Far:** `{req_detail['initial_action']}`")
    with c2:
        st.markdown(f"**Category:** `{req_detail['category']}`")
        st.markdown(f"**Matched Policy:** `{req_detail['relevant_policy']}`")
        st.markdown(f"**Decision:** **{req_detail['decision']}**")
        st.markdown(f"**Recommended Action:** {req_detail['recommended_action']}")
        st.markdown(f"**Detailed Reasoning:** {req_detail['reason']}")


# ---------------------------------------------------------------------------
# TAB 3: Ticket Queue
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Ticketing System Records & Historical Precedents")
    st.write(
        "This is the existing ticket queue from the assignment. Closed tickets represent **historical context** "
        "(prior precedents and consistency), while Active tickets represent open cases that require routing or resolution."
    )

    view_mode = st.radio("Display Tickets:", ["All Tickets (10)", "Active Tickets Only (4)", "Closed / Historical Tickets Only (6)"], horizontal=True)

    if "Active" in view_mode:
        displayed_tickets = [t for t in TICKET_QUEUE if t["is_active"]]
    elif "Closed" in view_mode:
        displayed_tickets = [t for t in TICKET_QUEUE if not t["is_active"]]
    else:
        displayed_tickets = TICKET_QUEUE

    ticket_table_data = []
    for t in displayed_tickets:
        ticket_table_data.append({
            "Ticket ID": t["ticket_id"],
            "Employee": t["employee"],
            "Issue Summary": t["issue_summary"],
            "Status": t["status"],
            "Type": "🔴 Active Case" if t["is_active"] else "🟢 Closed (Precedent)",
            "Context / Precedent": t["precedent_note"]
        })

    st.dataframe(ticket_table_data, width="stretch", hide_index=True)

    st.info(
        "💡 **How the Agent uses Ticket History:**\n\n"
        "- **TK-1042 (VPN expired):** Confirms that credential expiration is solved by employee self-renewal.\n"
        "- **TK-1043 (Laptop 3.2 yrs):** Confirms hardware failure over 3 years is approved for replacement.\n"
        "- **TK-1045 (Mailbox 35GB):** Precedent for approving quota increases beyond 25GB (within the 50GB cap) with manager approval.\n"
        "- **TK-1050 (Admin access):** Demonstrates that admin access requests without business justification are rejected.\n"
        "- **TK-1051 (Guest Wi-Fi):** Reaffirms that guest Wi-Fi passes are issued via front-desk kiosk without IT tickets."
    )
