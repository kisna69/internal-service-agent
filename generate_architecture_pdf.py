"""
generate_architecture_pdf.py
Generates a comprehensive, professional System Architecture Document PDF
for the Veridian Corp Internal IT Support Agent project.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Draw header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Veridian Corp — Internal IT Support Agent | System Architecture Document")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Draw footer on all pages
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL — Academic Prototype Submission | B.Tech IT & CSE")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()


def build_pdf(filename="Architecture_Document.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom palette
    PRIMARY = colors.HexColor("#1E3A8A")    # Deep Navy
    SECONDARY = colors.HexColor("#0284C7")  # Bright Blue
    DARK_TEXT = colors.HexColor("#0F172A")  # Slate 900
    MUTED_TEXT = colors.HexColor("#475569") # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Slate 50
    ACCENT_GREEN = colors.HexColor("#059669")
    ACCENT_AMBER = colors.HexColor("#D97706")
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=MUTED_TEXT,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=14,
        bulletIndent=4,
        spaceAfter=3
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=DARK_TEXT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=PRIMARY
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    code_block = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # -----------------------------------------------------------------------
    # PAGE 1: HEADER, EXECUTIVE SUMMARY & TIERED ARCHITECTURE
    # -----------------------------------------------------------------------
    story.append(Paragraph("Veridian Corp — Internal IT Support Agent", title_style))
    story.append(Paragraph("<b>System Architecture & Technical Design Specification</b> | Assignment 2 Prototype", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=8))

    # Meta Info Card
    meta_data = [
        [
            Paragraph("<b>Target Organization:</b> Veridian Corp", table_cell),
            Paragraph("<b>Coursework:</b> B.Tech IT / Computer Science", table_cell)
        ],
        [
            Paragraph("<b>Project Scope:</b> Internal Service Agent (IT Triage)", table_cell),
            Paragraph("<b>Deployment:</b> Local (Streamlit :8501) & Vercel (WASM)", table_cell)
        ],
        [
            Paragraph("<b>Timeline:</b> 21 Sep – 25 Sep 2026", table_cell),
            Paragraph("<b>Engine:</b> Rule-Based, Policy-Grounded (Zero Hallucination)", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # 1. Executive Summary & Design Goals
    story.append(Paragraph("1. Executive Summary & Core Objectives", h1_style))
    story.append(Paragraph(
        "The Veridian Corp Internal IT Support Agent is a deterministic, automated decision-support system "
        "engineered to triage and resolve incoming employee IT inquiries. Built strictly against the specifications "
        "of <b>Assignment 2: Internal Service Agent (IT Support)</b>, the agent provides immediate, policy-grounded "
        "resolutions while eliminating ticket misrouting and safeguarding sensitive corporate systems.",
        body_style
    ))
    story.append(Paragraph("• <b>Strict Policy Grounding:</b> Exclusively applies KB-01 through KB-10 and the Asset Management Policy without external assumptions.", bullet_style))
    story.append(Paragraph("• <b>Zero Hallucination & Zero Cost:</b> Pure deterministic rule engine requiring no paid third-party API keys or external LLM tokens.", bullet_style))
    story.append(Paragraph("• <b>Precedent-Aware:</b> Directly links resolutions to historical ticketing records (TK-1042 to TK-1051) for organizational consistency.", bullet_style))
    story.append(Paragraph("• <b>Dual Runtime:</b> Operates natively via Python Streamlit locally, and via <i>stlite</i> WebAssembly on Vercel without servers.", bullet_style))

    # 2. High-Level Architecture (Tiered Model Table)
    story.append(Paragraph("2. High-Level System Architecture (Tiered Model)", h1_style))
    
    tier_data = [
        [
            Paragraph("<b>Tier</b>", table_header),
            Paragraph("<b>Subsystem & Technologies</b>", table_header),
            Paragraph("<b>Core Function & Responsibilities</b>", table_header)
        ],
        [
            Paragraph("<b>1. Presentation Tier</b>", table_cell_bold),
            Paragraph("Streamlit Client / stlite WASM<br/>(3 Tabs: Agent, Requests, Tickets)", table_cell),
            Paragraph("User interface for employee inquiry input, preset case selection, live decision badge rendering, and policy references.", table_cell)
        ],
        [
            Paragraph("<b>2. Application & Triage Tier</b>", table_cell_bold),
            Paragraph("<code>app.py</code><br/><code>analyze_request()</code> Engine", table_cell),
            Paragraph("Performs tokenization, numerical threshold extraction (attempt counts, hardware age), vagueness filtering, and role routing.", table_cell)
        ],
        [
            Paragraph("<b>3. Knowledge & Policy Tier</b>", table_cell_bold),
            Paragraph("<code>data.py</code><br/><code>POLICIES</code> Dictionary", table_cell),
            Paragraph("11 official corporate policies covering Password Resets, VPN, Hardware, Software, Spoolers, Mailboxes, Wi-Fi, Expenses, Security, and WFH.", table_cell)
        ],
        [
            Paragraph("<b>4. Precedent & History Tier</b>", table_cell_bold),
            Paragraph("<code>data.py</code><br/><code>TICKET_QUEUE</code> & Historical DB", table_cell),
            Paragraph("10 ticket queue records distinguishing active operational routing from closed tickets that establish binding resolution precedents.", table_cell)
        ]
    ]
    tier_table = Table(tier_data, colWidths=[110, 144, 250])
    tier_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(tier_table)

    story.append(PageBreak())

    # -----------------------------------------------------------------------
    # PAGE 2: REPOSITORY STRUCTURE, PIPELINE & DECISION TAXONOMY
    # -----------------------------------------------------------------------
    story.append(Paragraph("3. Repository & Module Structure", h1_style))
    
    comp_data = [
        [Paragraph("File", table_header), Paragraph("Type", table_header), Paragraph("Architectural Purpose", table_header)],
        [
            Paragraph("<code>app.py</code>", table_cell_bold),
            Paragraph("Python / Streamlit", table_cell),
            Paragraph("Main application entrypoint, interactive triage interface, and rule classification engine.", table_cell)
        ],
        [
            Paragraph("<code>data.py</code>", table_cell_bold),
            Paragraph("Python Data Module", table_cell),
            Paragraph("Static storage of 11 policies, 15 pre-computed employee requests, and 10 ticket records.", table_cell)
        ],
        [
            Paragraph("<code>index.html</code>", table_cell_bold),
            Paragraph("Static WebAssembly", table_cell),
            Paragraph("Mounts <code>stlite</code> (Pyodide in WASM) to run <code>app.py</code> directly inside client browsers on Vercel.", table_cell)
        ],
        [
            Paragraph("<code>vercel.json</code>", table_cell_bold),
            Paragraph("Deployment Config", table_cell),
            Paragraph("Configures clean URL rewrites and static asset routing for instantaneous Vercel Edge hosting.", table_cell)
        ],
        [
            Paragraph("<code>requirements.txt</code>", table_cell_bold),
            Paragraph("Dependencies", table_cell),
            Paragraph("Declares <code>streamlit</code> as the single runtime requirement. Zero bloat.", table_cell)
        ],
        [
            Paragraph("<code>README.md</code>", table_cell_bold),
            Paragraph("Documentation", table_cell),
            Paragraph("System manual, running instructions, limitations, and a structured viva examination defense guide.", table_cell)
        ]
    ]
    comp_table = Table(comp_data, colWidths=[95, 105, 304])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 6))

    # 4. Request Processing Pipeline
    story.append(Paragraph("4. Request Processing Pipeline & Evaluation Stages", h1_style))
    pipeline_steps = [
        ("Stage 1: Ingestion & Quality Gate", "Validates input length. Triggers 'Ask for More Information' on ambiguous queries (REQ-15)."),
        ("Stage 2: Critical Security Triage (KB-09)", "Scans for phishing/malware. Automatically flags quarantine order halting email forwarding (REQ-08)."),
        ("Stage 3: Numerical Threshold Checks (KB-01)", "Checks failed attempts. >=5 attempts (REQ-03 with 6) routes to IT manual unlock; <5 is self-service."),
        ("Stage 4: Role & Governance Boundary Verification", "Enforces contractor approval for VPN (KB-02, REQ-11) and directs expense tool accounts to Finance (KB-08, REQ-12)."),
        ("Stage 5: Asset Refresh & Lifecycle Evaluation", "Cross-references KB-03 (3-yr eligibility) with 4-yr Asset Policy; routes 3.5-yr dead laptop (REQ-01) for Finance sign-off."),
        ("Stage 6: Precedent Association & Formulation", "Matches ticket queue history (TK-1042..1051) and renders Category, Policy, Decision, Action, and Reason.")
    ]
    for title, desc in pipeline_steps:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 6))

    # 5. Standardized Decision Taxonomy
    story.append(Paragraph("5. Standardized Decision Taxonomy", h1_style))
    dec_data = [
        [Paragraph("Decision Type", table_header), Paragraph("Operational Meaning", table_header), Paragraph("Assignment Example", table_header)],
        [
            Paragraph("<b>Resolve / Self-Service</b>", table_cell_bold),
            Paragraph("Handled by employee via portal/kiosk without ticket.", table_cell),
            Paragraph("REQ-02 (Guest Wi-Fi), REQ-05 (VPN renew)", table_cell)
        ],
        [
            Paragraph("<b>Route to IT</b>", table_cell_bold),
            Paragraph("Direct manual action by IT technician required.", table_cell),
            Paragraph("REQ-01 (3.5 yr dead laptop), REQ-03 (6 password attempts)", table_cell)
        ],
        [
            Paragraph("<b>Route to Security</b>", table_cell_bold),
            Paragraph("Immediate incident reporting and threat quarantine.", table_cell),
            Paragraph("REQ-08 (Phishing email being forwarded)", table_cell)
        ],
        [
            Paragraph("<b>Route to Finance</b>", table_cell_bold),
            Paragraph("Budget approval, allowance processing, or tool creation.", table_cell),
            Paragraph("REQ-07 (WFH monitor allowance), REQ-12 (Expense tool)", table_cell)
        ],
        [
            Paragraph("<b>Manager Approval Required</b>", table_cell_bold),
            Paragraph("Requires formal business justification and manager sign-off.", table_cell),
            Paragraph("REQ-10 (Admin server access), REQ-11 (Contractor VPN)", table_cell)
        ],
        [
            Paragraph("<b>Security Review Required</b>", table_cell_bold),
            Paragraph("IT Security software vetting (takes 3–5 business days).", table_cell),
            Paragraph("REQ-04 (Non-catalog tool), REQ-14 (Browser extension)", table_cell)
        ],
        [
            Paragraph("<b>Troubleshooting Required</b>", table_cell_bold),
            Paragraph("Hardware diagnostics or spooler service restart.", table_cell),
            Paragraph("REQ-06 (Printer jam), REQ-13 (2-yr flickering screen)", table_cell)
        ],
        [
            Paragraph("<b>Ask for More Information</b>", table_cell_bold),
            Paragraph("Clarification requested; input lacks actionable specifics.", table_cell),
            Paragraph("REQ-15 ('hey can you help, its not working')", table_cell)
        ]
    ]
    dec_table = Table(dec_data, colWidths=[130, 194, 180])
    dec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(dec_table)

    story.append(PageBreak())

    # -----------------------------------------------------------------------
    # PAGE 3: TICKET PRECEDENTS, DUAL DEPLOYMENT & GOVERNANCE
    # -----------------------------------------------------------------------
    story.append(Paragraph("6. Ticket Queue Architecture & Precedent Linkage", h1_style))
    story.append(Paragraph(
        "Section 3 of the assignment contains 10 ticket records. The system utilizes them systematically:",
        body_style
    ))
    story.append(Paragraph("• <b>Active Work Items (4 tickets):</b> TK-1043 (Laptop 3.2 yrs), TK-1044 (Non-catalog software), TK-1047 (Home office equipment), and TK-1048 (Phishing) represent active cases pending fulfillment or external review.", bullet_style))
    story.append(Paragraph("• <b>Historical Precedents (6 tickets):</b> Closed tickets govern consistency. Specifically, <b>TK-1050</b> sets the organizational precedent that administrative server access without business justification must be rejected.", bullet_style))

    story.append(Spacer(1, 6))

    # 7. Dual-Mode Deployment Topology
    story.append(Paragraph("7. Dual-Mode Deployment Topology", h1_style))
    deploy_data = [
        [Paragraph("Dimension", table_header), Paragraph("Local Execution (Streamlit)", table_header), Paragraph("Cloud Serverless Execution (Vercel)", table_header)],
        [
            Paragraph("<b>Target Runtime</b>", table_cell_bold),
            Paragraph("Python 3.11 Local Interpreter", table_cell),
            Paragraph("Pyodide / WebAssembly in Browser (stlite)", table_cell)
        ],
        [
            Paragraph("<b>Serving Model</b>", table_cell_bold),
            Paragraph("Uvicorn / WebSocket server on <code>localhost:8501</code>", table_cell),
            Paragraph("Edge Static CDN Delivery (Zero Server Overhead)", table_cell)
        ],
        [
            Paragraph("<b>Launch Trigger</b>", table_cell_bold),
            Paragraph("<code>python -m streamlit run app.py</code>", table_cell),
            Paragraph("Git commit to GitHub repository", table_cell)
        ],
        [
            Paragraph("<b>Operational Role</b>", table_cell_bold),
            Paragraph("Live examiner evaluation & viva defense", table_cell),
            Paragraph("Public shareable link for AIONOS reviewers", table_cell)
        ]
    ]
    deploy_table = Table(deploy_data, colWidths=[110, 197, 197])
    deploy_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(deploy_table)

    story.append(Spacer(1, 6))

    # 8. Governance, Compliance & Security Constraints
    story.append(Paragraph("8. Corporate Governance & Security Constraints", h1_style))
    story.append(Paragraph("• <b>Auditable Decision Traceability:</b> Each resolution provides an unambiguous policy citation (e.g., KB-01), creating an immutable, reviewable audit trail for corporate IT compliance.", bullet_style))
    story.append(Paragraph("• <b>Strict Segregation of Duties (SoD):</b> Adheres to corporate authorization boundaries. IT technicians cannot grant expense software access (Finance jurisdiction under KB-08) or bypass security reviews (KB-04).", bullet_style))
    story.append(Paragraph("• <b>Active Incident Containment:</b> Security threats flagged under KB-09 trigger explicit warnings preventing employees from broadcasting phishing lures internally.", bullet_style))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=8))

    signoff_data = [
        [
            Paragraph("<b>Project:</b> Veridian Corp IT Support Agent", table_cell),
            Paragraph("<b>Author:</b> B.Tech Computer Science / IT Student", table_cell)
        ],
        [
            Paragraph("<b>Repository:</b> github.com/kisna69/internal-service-agent", table_cell),
            Paragraph("<b>Status:</b> Fully Tested & Verified (All 15 Requests Passed)", table_cell)
        ]
    ]
    signoff_table = Table(signoff_data, colWidths=[250, 254])
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(signoff_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")


if __name__ == "__main__":
    build_pdf("Architecture_Document.pdf")
