<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Llama_3-AI_Powered-667eea?style=for-the-badge&logo=meta&logoColor=white" alt="Llama 3"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Last_Updated-January_2026-orange?style=for-the-badge" alt="Last Updated"/>
</p>

<h1 align="center">🎯 SmartMatch AI</h1>

<p align="center">
  <strong>Portfolio-Grade ATS Resume Analyzer powered by Llama 3 AI</strong>
</p>

<p align="center">
  <em>Unlike keyword matchers, our AI understands context and synonyms. <br/>
  "ML" = "Machine Learning", "JS" = "JavaScript", and more!</em>
</p>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Analysis** | Uses Llama 3 (70B) via Groq for deep semantic resume matching |
| 📊 **Interactive Dashboard** | Beautiful Streamlit interface with glassmorphism design |
| 🎯 **Match Scoring** | Get a precise 0-100% compatibility score with detailed breakdown |
| 🔍 **Missing Skills Detection** | Identifies critical skills gaps between your resume and job description |
| 📝 **AI Assessment** | Receive professional recruiter-style feedback on your candidacy |
| ✅ **Resume Quality Check** | Validates email, phone, sections, and optimal word count |
| 📈 **Visual Analytics** | Interactive Plotly gauge charts for instant visual feedback |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Groq API key ([Get one free here](https://console.groq.com/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/JD-fitter.git
   cd JD-fitter
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   
   Open `app.py` and replace the placeholder with your Groq API key:
   ```python
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

---

## 🎮 How to Use

<table>
<tr>
<td width="33%" align="center">
<h3>Step 1</h3>
<p>📋 Paste the job description in the sidebar</p>
</td>
<td width="33%" align="center">
<h3>Step 2</h3>
<p>📄 Upload your PDF resume</p>
</td>
<td width="33%" align="center">
<h3>Step 3</h3>
<p>🚀 Click "Analyze Resume" and get instant AI feedback!</p>
</td>
</tr>
</table>

---

## 🏗️ Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     SmartMatch AI                           │
├─────────────────────────────────────────────────────────────┤
│  Frontend          │  Streamlit (Interactive Web Dashboard) │
│  Visualization     │  Plotly (Interactive Charts)           │
│  AI Engine         │  Llama 3 (70B) via Groq API           │
│  PDF Processing    │  PyPDF2                                │
│  Language          │  Python 3.8+                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Scoring System

The AI evaluates resumes using a weighted scoring system:

| Category | Weight | Description |
|----------|--------|-------------|
| **Hard Skills** | 60% | Programming languages, frameworks, tools, certifications |
| **Experience** | 25% | Years of relevant experience, seniority level, industry alignment |
| **Soft Skills & Education** | 15% | Leadership, communication, certifications, degrees |

### Score Interpretation

| Score Range | Rating | Recommendation |
|-------------|--------|----------------|
| 85-100 | 🌟 Excellent | Interview immediately |
| 70-84 | ✅ Good | Worth interviewing |
| 50-69 | ⚠️ Partial | Some gaps, could be considered |
| 30-49 | ⚡ Weak | Significant skill gaps |
| 0-29 | ❌ Poor | Not suitable for this role |

---

## 🎨 UI Preview

The application features a stunning dark theme with:
- **Glassmorphism cards** with frosted glass effect
- **Gradient backgrounds** (Purple to Blue theme)
- **Interactive gauge charts** for score visualization
- **Color-coded badges** for matched/missing skills
- **Responsive design** that works on all screen sizes

---

## 📁 Project Structure

```
JD-fitter/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore rules
```

---

## 🔧 Configuration

### Environment Variables (Optional)

Instead of hardcoding the API key, you can use environment variables:

```bash
export GROQ_API_KEY="your_api_key_here"
```

Then modify `app.py`:
```python
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔀 Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a ⭐ on GitHub!

---

<p align="center">
  <strong>Built with ❤️ using Streamlit, Plotly, and Llama 3 via Groq</strong>
</p>

<p align="center">
  <a href="https://github.com/YOUR_USERNAME/JD-fitter/issues">Report Bug</a>
  ·
  <a href="https://github.com/YOUR_USERNAME/JD-fitter/issues">Request Feature</a>
</p>
