"""
================================================================================
SmartMatch AI - Portfolio-Grade ATS Resume Analyzer
================================================================================

A visually impressive Application Tracking System (ATS) Resume Analyzer that uses
Generative AI (Llama 3 via Groq) for semantic resume matching.

Tech Stack:
- Frontend: Streamlit (interactive web dashboard)
- Visualization: Plotly (interactive charts)
- AI: Llama 3 via Groq API (semantic analysis)
- File Handling: PyPDF2 (PDF parsing)

Author: Built with AI Assistance
Version: 2.0.0 (LLM-Powered)
================================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================
import streamlit as st
import plotly.graph_objects as go
import PyPDF2
import re
import io
import os
import json
from typing import Tuple, List, Dict, Optional

# Groq API for Llama 3 access
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="SmartMatch AI | ATS Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS STYLING
# =============================================================================
st.markdown("""
<style>
    /* ===== Global Styles ===== */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
    }
    
    /* ===== Main Header Styling ===== */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #a0a0c0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* ===== Glassmorphism Cards ===== */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .card-title {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* ===== Keyword Badges ===== */
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .badge-missing {
        background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(238, 90, 90, 0.4);
    }
    
    .badge-matched {
        background: linear-gradient(135deg, #51cf66, #40c057);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(64, 192, 87, 0.4);
    }
    
    /* ===== Profile Summary Box ===== */
    .summary-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
        border-left: 4px solid #667eea;
        padding: 1.2rem;
        margin: 0.5rem 0;
        border-radius: 0 12px 12px 0;
        color: #e0e0e0;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* ===== Quality Check Indicators ===== */
    .quality-pass {
        color: #51cf66;
        font-weight: 600;
    }
    
    .quality-fail {
        color: #ff6b6b;
        font-weight: 600;
    }
    
    .quality-warning {
        color: #fcc419;
        font-weight: 600;
    }
    
    /* ===== Sidebar Styling ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a3e 0%, #0f0f23 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] .stTextArea textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
    }
    
    /* ===== Metric Styling ===== */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stMetricValue"] {
        color: #667eea;
    }
    
    /* ===== Button Styling ===== */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* ===== Divider ===== */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* ===== AI Badge ===== */
    .ai-badge {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# LLM SYSTEM PROMPT
# =============================================================================
SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) and a strict technical recruiter with 15+ years of experience.
Your task is to evaluate how well a candidate's resume matches a specific job description.

EVALUATION CRITERIA (in order of importance):

1. HARD SKILLS (60% weight):
   - Penalize heavily for missing required technical skills (programming languages, frameworks, tools, certifications)
   - Each missing critical skill: -8 to -12 points
   - Recognize synonyms and abbreviations: "ML" = "Machine Learning", "JS" = "JavaScript", "K8s" = "Kubernetes"
   
2. EXPERIENCE (25% weight):
   - Years of relevant experience in the field
   - Seniority level match (Junior/Mid/Senior)
   - Industry alignment (e.g., fintech for fintech role)
   
3. SOFT SKILLS & EDUCATION (15% weight):
   - Leadership, communication, teamwork evidence
   - Relevant certifications or degrees

SCORING GUIDELINES:
- 85-100: Excellent match - Strong candidate, interview immediately
- 70-84: Good match - Solid candidate, worth interviewing  
- 50-69: Partial match - Some gaps but could be considered
- 30-49: Weak match - Significant skill gaps
- 0-29: Poor match - Not suitable for this role

You MUST respond with ONLY a valid JSON object, no markdown, no explanation, no code blocks:
{
  "match_percentage": <integer 0-100>,
  "missing_keywords": [<list of 3-8 critical missing skills/technologies>],
  "profile_summary": "<2-3 sentence professional assessment of the candidate's fit for this specific role>"
}"""


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def get_groq_client(api_key: str) -> Optional[Groq]:
    """
    Initialize and return Groq client with provided API key.
    
    Args:
        api_key: The Groq API key
    
    Returns:
        Groq client or None if not available
    """
    if not GROQ_AVAILABLE:
        return None
    
    if not api_key or not api_key.strip():
        return None
    
    try:
        return Groq(api_key=api_key.strip())
    except Exception:
        return None


def extract_text_from_pdf(pdf_file) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract text content from an uploaded PDF file.
    
    Args:
        pdf_file: Streamlit UploadedFile object containing the PDF
        
    Returns:
        Tuple of (extracted_text, error_message)
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        
        if pdf_reader.is_encrypted:
            return None, "❌ This PDF is password-protected. Please upload an unencrypted resume."
        
        text_content = []
        for page in pdf_reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
            except Exception:
                continue
        
        if not text_content:
            return None, "❌ Could not extract text from this PDF. It might be a scanned image."
        
        return " ".join(text_content), None
        
    except PyPDF2.errors.PdfReadError:
        return None, "❌ Invalid or corrupted PDF file. Please check the file and try again."
    except Exception as e:
        return None, f"❌ An unexpected error occurred: {str(e)}"


def analyze_resume_with_llm(resume_text: str, jd_text: str, api_key: str) -> Dict:
    """
    Use Llama 3 via Groq to semantically analyze resume against job description.
    
    This function sends both texts to the LLM which performs deep semantic analysis,
    understanding synonyms, context, and relevance - far superior to keyword matching.
    
    Args:
        resume_text: Extracted text from the candidate's resume
        jd_text: The job description text
        api_key: The Groq API key
        
    Returns:
        dict with keys: match_percentage, missing_keywords, profile_summary, error
    """
    # Default fallback response
    fallback = {
        "match_percentage": 0,
        "missing_keywords": [],
        "profile_summary": "Unable to analyze. Please check your API key and try again.",
        "error": None
    }
    
    # Check for Groq availability
    client = get_groq_client(api_key)
    if not client:
        if not GROQ_AVAILABLE:
            fallback["error"] = "Groq library not installed. Run: pip install groq"
        else:
            fallback["error"] = "Please enter your Groq API key in the sidebar."
        return fallback
    
    # Construct the user prompt
    user_prompt = f"""Analyze this resume against the job description.

=== JOB DESCRIPTION ===
{jd_text[:4000]}

=== RESUME ===
{resume_text[:6000]}

Respond with ONLY the JSON object, nothing else."""

    try:
        # Call Llama 3 via Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,  # Lower temperature for consistent, analytical responses
            max_tokens=500,
            timeout=30.0
        )
        
        # Extract the response
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Clean up potential markdown code blocks
        if response_text.startswith("```"):
            response_text = re.sub(r'^```(?:json)?\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
        
        # Parse JSON response
        result = json.loads(response_text)
        
        # Validate required fields
        if "match_percentage" not in result:
            result["match_percentage"] = 50
        if "missing_keywords" not in result:
            result["missing_keywords"] = []
        if "profile_summary" not in result:
            result["profile_summary"] = "Analysis completed."
        
        # Ensure types are correct
        result["match_percentage"] = int(min(100, max(0, result["match_percentage"])))
        result["missing_keywords"] = list(result["missing_keywords"])[:10]
        result["profile_summary"] = str(result["profile_summary"])[:500]
        result["error"] = None
        
        return result
        
    except json.JSONDecodeError as e:
        fallback["error"] = f"LLM returned invalid JSON. Please try again."
        return fallback
    except Exception as e:
        error_msg = str(e)
        if "rate_limit" in error_msg.lower():
            fallback["error"] = "Rate limit reached. Please wait a moment and try again."
        elif "timeout" in error_msg.lower():
            fallback["error"] = "Request timed out. The service might be busy."
        else:
            fallback["error"] = f"API error: {error_msg[:100]}"
        return fallback


def check_resume_quality(resume_text: str) -> Dict[str, dict]:
    """
    Perform resume hygiene and quality checks.
    
    Args:
        resume_text: The extracted resume text
        
    Returns:
        Dictionary with quality check results
    """
    results = {}
    
    # Word Count Analysis
    word_count = len(resume_text.split())
    if word_count < 150:
        results['word_count'] = {
            'status': 'fail',
            'message': f'Too brief ({word_count} words). Aim for 300-800 words.',
            'value': word_count
        }
    elif word_count > 1500:
        results['word_count'] = {
            'status': 'warning',
            'message': f'Lengthy ({word_count} words). Consider condensing.',
            'value': word_count
        }
    else:
        results['word_count'] = {
            'status': 'pass',
            'message': f'Good length ({word_count} words).',
            'value': word_count
        }
    
    # Email Detection
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails_found = re.findall(email_pattern, resume_text)
    results['email'] = {
        'status': 'pass' if emails_found else 'fail',
        'message': f'Email: {emails_found[0]}' if emails_found else 'No email found.',
        'value': emails_found[0] if emails_found else None
    }
    
    # Phone Detection
    phone_pattern = r'[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{4,6}'
    phones_found = re.findall(phone_pattern, resume_text)
    results['phone'] = {
        'status': 'pass' if phones_found else 'warning',
        'message': 'Phone detected.' if phones_found else 'No phone detected.',
        'value': phones_found[0] if phones_found else None
    }
    
    # Key Sections Detection
    sections = ['experience', 'education', 'skills', 'projects', 'summary']
    found_sections = [s for s in sections if s in resume_text.lower()]
    results['sections'] = {
        'status': 'pass' if len(found_sections) >= 3 else 'warning',
        'message': f'Sections: {", ".join(found_sections).title()}' if found_sections else 'Add clear section headers.',
        'value': found_sections
    }
    
    return results


def create_gauge_chart(score: float) -> go.Figure:
    """
    Create an interactive Plotly gauge chart for the match score.
    
    Args:
        score: Match score percentage (0-100)
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "AI Match Score", 'font': {'size': 24, 'color': '#ffffff'}},
        number={'font': {'size': 56, 'color': '#ffffff'}, 'suffix': '%'},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 2,
                'tickcolor': 'white',
                'tickfont': {'color': 'white'}
            },
            'bar': {'color': "#667eea", 'thickness': 0.75},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(255, 107, 107, 0.3)'},
                {'range': [40, 70], 'color': 'rgba(252, 196, 25, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(81, 207, 102, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "#ffffff", 'width': 4},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=300,
        margin=dict(l=30, r=30, t=50, b=30)
    )
    
    return fig


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point."""
    
    # Header
    st.markdown('<h1 class="main-header">🎯 SmartMatch AI</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Portfolio-Grade ATS Resume Analyzer <span class="ai-badge">Powered by Llama 3</span></p>', 
        unsafe_allow_html=True
    )
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📋 Input Section")
        st.markdown("---")
        
        # API Key Input
        st.markdown("### 🔑 Groq API Key")
        api_key = st.text_input(
            label="Enter your Groq API key",
            type="password",
            placeholder="gsk_...",
            help="Get your free API key at console.groq.com/keys",
            label_visibility="collapsed"
        )
        if api_key:
            st.success("✅ API Key entered")
        else:
            st.info("🔗 [Get free API key](https://console.groq.com/keys)")
        
        st.markdown("---")
        
        # Job Description Input
        st.markdown("### Job Description")
        job_description = st.text_area(
            label="Paste the job description here",
            height=200,
            placeholder="Paste the complete job description including requirements and qualifications...",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Resume Upload
        st.markdown("### Resume Upload")
        uploaded_file = st.file_uploader(
            label="Upload your resume (PDF)",
            type=['pdf'],
            help="Drag and drop your PDF resume here",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Analyze Button
        analyze_clicked = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)
        
        # Info section
        st.markdown("---")
        st.markdown("### ℹ️ How It Works")
        st.markdown("""
        1. **Enter** your Groq API key
        2. **Paste** the job description
        3. **Upload** your PDF resume
        4. **Click** Analyze Resume
        """)
    
    # Main Content Area
    if analyze_clicked:
        # Validate inputs
        if not job_description.strip():
            st.error("⚠️ Please paste a job description in the sidebar.")
            return
        
        if not uploaded_file:
            st.error("⚠️ Please upload your resume (PDF format) in the sidebar.")
            return
        
        # Process
        with st.spinner("🤖 Analyzing with Llama 3 AI... This takes a few seconds."):
            
            # Extract text from PDF
            resume_text, error = extract_text_from_pdf(uploaded_file)
            
            if error:
                st.error(error)
                return
            
            # Analyze with LLM
            llm_result = analyze_resume_with_llm(resume_text, job_description, api_key)
            
            # Check for errors
            if llm_result.get("error"):
                st.error(f"🔴 {llm_result['error']}")
                return
            
            # Quality checks
            quality_results = check_resume_quality(resume_text)
        
        # =================================================================
        # RESULTS DISPLAY
        # =================================================================
        
        st.markdown("---")
        
        # Row 1: Match Score Gauge
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            gauge_chart = create_gauge_chart(llm_result["match_percentage"])
            st.plotly_chart(gauge_chart, use_container_width=True)
            
            # Score interpretation
            score = llm_result["match_percentage"]
            if score >= 70:
                st.success("🌟 Excellent Match! Strong candidate for this position.")
            elif score >= 50:
                st.warning("📊 Partial Match. Some skill gaps to address.")
            else:
                st.error("⚡ Low Match. Significant improvements needed.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Row 2: Profile Summary
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📝 AI Assessment</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-box">{llm_result["profile_summary"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Row 3: Missing Keywords
        if llm_result["missing_keywords"]:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🔴 Missing Skills (High Priority)</div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #a0a0c0; margin-bottom: 1rem;">These skills appear in the job description but are missing from your resume:</p>', unsafe_allow_html=True)
            
            badges_html = '<div class="badge-container">'
            for keyword in llm_result["missing_keywords"]:
                badges_html += f'<span class="badge-missing">{keyword}</span>'
            badges_html += '</div>'
            st.markdown(badges_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">✅ Excellent Skill Coverage</div>', unsafe_allow_html=True)
            st.markdown('<p style="color: #51cf66;">No critical skills are missing from your resume!</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Row 4: Resume Quality Check
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📋 Resume Quality Check</div>', unsafe_allow_html=True)
        
        quality_cols = st.columns(4)
        quality_items = list(quality_results.items())
        
        for i, (check_name, result) in enumerate(quality_items):
            with quality_cols[i]:
                icon = "✅" if result['status'] == 'pass' else "⚠️" if result['status'] == 'warning' else "❌"
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <div style='font-size: 1.5rem;'>{icon}</div>
                        <div style='font-weight: 600; color: #a0a0c0;'>{check_name.replace('_', ' ').title()}</div>
                        <div class='quality-{result["status"]}' style='font-size: 0.85rem;'>{result['status'].upper()}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Expandable quality details
        with st.expander("📖 View Detailed Quality Analysis"):
            for check_name, result in quality_results.items():
                st.markdown(f"**{check_name.replace('_', ' ').title()}:** {result['message']}")
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: #606080;'>Built with ❤️ using Streamlit, Plotly, and Llama 3 via Groq</p>",
            unsafe_allow_html=True
        )
    
    else:
        # Welcome state
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 3rem;">
            <h2 style="color: #667eea;">👋 Welcome to SmartMatch AI</h2>
            <p style="color: #a0a0c0; font-size: 1.1rem;">
                Your intelligent ATS Resume Analyzer powered by <strong>Llama 3 AI</strong>.
            </p>
            <br>
            <p style="color: #808090;">
                Unlike keyword matchers, our AI understands context and synonyms.<br>
                "ML" = "Machine Learning", "JS" = "JavaScript", and more!
            </p>
            <br>
            <p style="color: #808090;">
                Get started by pasting a job description and uploading your resume in the sidebar →
            </p>
            <br>
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 2rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">🤖</div>
                    <div style="color: #a0a0c0;">AI Match Score</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">🔑</div>
                    <div style="color: #a0a0c0;">Missing Skills</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">📝</div>
                    <div style="color: #a0a0c0;">AI Assessment</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2rem;">✅</div>
                    <div style="color: #a0a0c0;">Quality Check</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    main()