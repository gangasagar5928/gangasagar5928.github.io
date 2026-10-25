import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os
import docx2pdf

def set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_p_border_bottom(p, color_hex="1A3A5C", size="6"):
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(size))
    bottom.set(qn('w:space'), '2')
    bottom.set(qn('w:color'), color_hex)
    pBdr.append(bottom)
    pPr.append(pBdr)

def build_resume():
    doc = docx.Document()
    
    # Page setup - Letter, 0.45" margins
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.42)
    section.bottom_margin = Inches(0.42)
    section.left_margin = Inches(0.48)
    section.right_margin = Inches(0.48)
    
    # Styles
    navy = RGBColor(0x1A, 0x3A, 0x5C)
    black = RGBColor(0x00, 0x00, 0x00)
    gray = RGBColor(0x33, 0x33, 0x33)
    
    # Header - Name
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(2)
    p_name.paragraph_format.line_spacing = 1.0
    r_name = p_name.add_run("AMAN KUMAR SINGH")
    r_name.font.name = "Arial"
    r_name.font.size = Pt(17)
    r_name.font.bold = True
    r_name.font.color.rgb = navy
    
    # Header - Line 1
    p_c1 = doc.add_paragraph()
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.space_before = Pt(0)
    p_c1.paragraph_format.space_after = Pt(1.5)
    p_c1.paragraph_format.line_spacing = 1.0
    r_c1 = p_c1.add_run("Greater Noida, UP 201310  |  +91-9460075023  |  singhamankumar.5928@gmail.com")
    r_c1.font.name = "Arial"
    r_c1.font.size = Pt(8.5)
    r_c1.font.color.rgb = black
    
    # Header - Line 2
    p_c2 = doc.add_paragraph()
    p_c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c2.paragraph_format.space_before = Pt(0)
    p_c2.paragraph_format.space_after = Pt(6)
    p_c2.paragraph_format.line_spacing = 1.0
    r_c2 = p_c2.add_run("linkedin.com/in/gangasagar5928  |  github.com/gangasagar5928  |  faujiniwas.web.app")
    r_c2.font.name = "Arial"
    r_c2.font.size = Pt(8.5)
    r_c2.font.color.rgb = black
    
    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(title)
        r.font.name = "Arial"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = navy
        add_p_border_bottom(p, "1A3A5C", "6")
        return p

    # --- SUMMARY ---
    add_section_header("SUMMARY")
    p_sum = doc.add_paragraph()
    p_sum.paragraph_format.space_before = Pt(2)
    p_sum.paragraph_format.space_after = Pt(4)
    p_sum.paragraph_format.line_spacing = 1.08
    r_sum = p_sum.add_run(
        "Electrical & Electronics Engineering student specializing in embedded cybersecurity and hardware-enforced fail-closed "
        "architectures. Inventor of four drafted patent applications spanning battery security, medical-device anti-spoofing, earthen "
        "primary energy, and spacecraft radiation fault-tolerance. 2,150+ GitHub commits and a 217-day streak across defense-tech DSP, "
        "on-device AI, and deployed commercial platforms."
    )
    r_sum.font.name = "Arial"
    r_sum.font.size = Pt(9.0)
    r_sum.font.color.rgb = black
    
    # --- PATENT APPLICATIONS (DRAFTED — FILING IN PROGRESS) ---
    add_section_header("PATENT APPLICATIONS (DRAFTED — FILING IN PROGRESS)")
    
    patents = [
        (
            "BioTrustPulse — Fail-Closed Hardware-Interlocked Biometric Diagnostic Apparatus",
            "A fail-closed medical-diagnostic apparatus that verifies device integrity before any measurement, preventing sensor spoofing and tampering."
        ),
        (
            "Sentry BMS — Cyber-Physical Battery Management & Trust-Gated Access Control System",
            "A cyber-physical battery-management and access-control system that fuses battery-health integrity with user authentication: tampering with the battery automatically cuts power and denies physical access."
        ),
        (
            "Agastya — Earthen Primary Galvanic Power Generation System",
            "A battery-free, earth-abundant primary power system delivering a stable regulated supply for off-grid loads and on-demand hydrogen generation."
        ),
        (
            "RadZero Space AI — Spacecraft Attitude Control & Radiation Fault-Mitigation Apparatus",
            "A spacecraft attitude-control apparatus that detects and repairs radiation-induced memory faults in on-board AI in real time, maintaining stable control without a system reboot."
        )
    ]
    
    for i, (title, desc) in enumerate(patents):
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(3 if i > 0 else 2)
        p_t.paragraph_format.space_after = Pt(1)
        p_t.paragraph_format.line_spacing = 1.0
        r_t = p_t.add_run(title)
        r_t.font.name = "Arial"
        r_t.font.size = Pt(9.2)
        r_t.font.bold = True
        r_t.font.color.rgb = black
        
        p_d = doc.add_paragraph()
        p_d.paragraph_format.space_before = Pt(0)
        p_d.paragraph_format.space_after = Pt(2.5)
        p_d.paragraph_format.line_spacing = 1.05
        r_d = p_d.add_run(desc)
        r_d.font.name = "Arial"
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = black

    # --- EXPERIENCE ---
    add_section_header("EXPERIENCE")
    p_exp_t = doc.add_paragraph()
    p_exp_t.paragraph_format.space_before = Pt(2)
    p_exp_t.paragraph_format.space_after = Pt(1.5)
    p_exp_t.paragraph_format.line_spacing = 1.0
    r_exp_title = p_exp_t.add_run("Founder — Fauji Niwas & ScrapMandi")
    r_exp_title.font.name = "Arial"
    r_exp_title.font.size = Pt(9.5)
    r_exp_title.font.bold = True
    r_exp_title.font.color.rgb = black
    r_exp_meta = p_exp_t.add_run("  |  React, Flutter, Firebase, Razorpay  |  Feb 2026 – Present")
    r_exp_meta.font.name = "Arial"
    r_exp_meta.font.size = Pt(8.0)
    r_exp_meta.font.color.rgb = gray
    
    p_exp_d = doc.add_paragraph(style='List Bullet')
    p_exp_d.paragraph_format.space_before = Pt(0)
    p_exp_d.paragraph_format.space_after = Pt(3)
    p_exp_d.paragraph_format.line_spacing = 1.05
    r_exp_d = p_exp_d.add_run(
        "Built and deployed two production platforms: a privacy-first defense relocation PWA for military personnel (AES-256-GCM + "
        "RSA-OAEP, zero-PII server exposure) and a B2B scrap-exchange marketplace (React 18 + Firebase, 7,000+ lines, server-side "
        "Razorpay escrow verification)."
    )
    r_exp_d.font.name = "Arial"
    r_exp_d.font.size = Pt(8.8)
    r_exp_d.font.color.rgb = black

    # --- PROJECTS ---
    add_section_header("PROJECTS")
    projects = [
        (
            "NIRDHVANI — Tactical Throat-Acoustic ANC System (SIH)",
            "  |  ESP32, TinyML, DSP  |  Aug 2026",
            "Throat-contact piezo ANC for 120 dB+ battlefield noise; NLMS adaptive filter + TinyML step-size tuning, <4 ms latency, prototype BOM under Rs 780."
        ),
        (
            "VARUNA-SDS — Subsea Software-Defined Sonar Payload (SIH)",
            "  |  STM32, DMA/DAC  |  Aug 2026",
            "10–100 kHz LFM chirp synthesis with 7.6 cm range resolution (50x over fixed-frequency sonar); Tukey/Hann windowing for multipath environments."
        ),
        (
            "Eloqui — 100% Offline AI Speaking Coach",
            "  |  Flutter, C++ FFI, llama.cpp  |  Jul 2026",
            "On-device LLM inference + Whisper STT + Piper TTS; solved the multi-model RAM cliff via deterministic lifecycle management (peak RAM < 1.2 GB)."
        )
    ]
    for i, (title, meta, desc) in enumerate(projects):
        p_p = doc.add_paragraph()
        p_p.paragraph_format.space_before = Pt(2.5 if i > 0 else 2)
        p_p.paragraph_format.space_after = Pt(1)
        p_p.paragraph_format.line_spacing = 1.0
        r_pt = p_p.add_run(title)
        r_pt.font.name = "Arial"
        r_pt.font.size = Pt(9.5)
        r_pt.font.bold = True
        r_pt.font.color.rgb = black
        r_pm = p_p.add_run(meta)
        r_pm.font.name = "Arial"
        r_pm.font.size = Pt(8.0)
        r_pm.font.color.rgb = gray
        
        p_pd = doc.add_paragraph(style='List Bullet')
        p_pd.paragraph_format.space_before = Pt(0)
        p_pd.paragraph_format.space_after = Pt(2.5)
        p_pd.paragraph_format.line_spacing = 1.05
        r_pd = p_pd.add_run(desc)
        r_pd.font.name = "Arial"
        r_pd.font.size = Pt(8.8)
        r_pd.font.color.rgb = black

    # --- TECHNICAL SKILLS ---
    add_section_header("TECHNICAL SKILLS")
    skills = [
        ("Hardware: ", "C/C++, FreeRTOS, ESP32, STM32, DSP (NLMS/LFM), TinyML, DMA/ADC/DAC/PWM, PCB & SMD soldering"),
        ("Security: ", "AES-256-GCM, RSA-OAEP, ECDSA/ECDH P-256, ATECC608A secure element, Secure Boot v2, STRIDE, fail-closed interlocks"),
        ("Software: ", "Python, React 18, TypeScript, Flutter/Dart, Firebase, Razorpay API, Git, Linux")
    ]
    for lbl, vals in skills:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.space_before = Pt(1)
        p_s.paragraph_format.space_after = Pt(1.5)
        p_s.paragraph_format.line_spacing = 1.05
        r_l = p_s.add_run(lbl)
        r_l.font.name = "Arial"
        r_l.font.size = Pt(8.8)
        r_l.font.bold = True
        r_l.font.color.rgb = black
        r_v = p_s.add_run(vals)
        r_v.font.name = "Arial"
        r_v.font.size = Pt(8.8)
        r_v.font.color.rgb = black

    # --- EDUCATION ---
    add_section_header("EDUCATION")
    edu = [
        ("Galgotias College of Engineering & Technology (AKTU)", "  |  B.Tech, Electrical & Electronics Engineering  |  3rd Semester  |  Expected 2029"),
        ("LBS Convent School, Kota (CBSE Class XII, PCM)", "  |  72.4%  |  JEE Main Mathematics: 90+ percentile")
    ]
    for inst, det in edu:
        p_e = doc.add_paragraph()
        p_e.paragraph_format.space_before = Pt(1.5)
        p_e.paragraph_format.space_after = Pt(1.5)
        p_e.paragraph_format.line_spacing = 1.05
        r_i = p_e.add_run(inst)
        r_i.font.name = "Arial"
        r_i.font.size = Pt(9.0)
        r_i.font.bold = True
        r_i.font.color.rgb = black
        r_d = p_e.add_run(det)
        r_d.font.name = "Arial"
        r_d.font.size = Pt(8.2)
        r_d.font.color.rgb = gray

    # --- CERTIFICATIONS & ACHIEVEMENTS ---
    add_section_header("CERTIFICATIONS & ACHIEVEMENTS")
    certs = [
        "NCC Air Wing 'A' Certificate (Ministry of Defence)  |  Duolingo English Test 130/160 (CEFR C1)",
        "Cisco: Introduction to Cybersecurity  |  Deloitte Cyber Job Simulation (Forage)  |  The Future of Chiplets (EE Times / Goldcast)",
        "GeeksforGeeks: Computer Fundamentals  |  MathWorks: MATLAB Onramp & Core MATLAB Skills  |  ULSA Academic Honor"
    ]
    for c in certs:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(1)
        p_c.paragraph_format.space_after = Pt(1.5)
        p_c.paragraph_format.line_spacing = 1.05
        r_c = p_c.add_run(c)
        r_c.font.name = "Arial"
        r_c.font.size = Pt(8.5)
        r_c.font.color.rgb = black

    out_docx = "Aman_Kumar_Singh_Resume.docx"
    doc.save(out_docx)
    print(f"Saved {out_docx}")

if __name__ == "__main__":
    build_resume()
