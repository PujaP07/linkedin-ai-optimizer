# 💼 LinkedIn Multi-Agent AI Optimizer

> **AI-powered LinkedIn profile optimization tool using multi-agent system architecture**

Transform your LinkedIn profile into a remote-job magnet with AI-powered multi-agent analysis and optimization specifically designed for **target job roles**.

## 🎯 Project Overview

This application leverages a **4-agent AI system** to analyze, critique, rewrite, and review LinkedIn profiles, helping professionals optimize for:
- 🌍 Remote job opportunities
- 🤖 Mention Job roles
- 📊 ATS (Applicant Tracking System) compatibility
- 🎓 Keyword optimization for better recruiter visibility

---

## ✨ Key Features

### 🤖 Multi-Agent Architecture
- **Agent 1 (Analyzer)**: Evaluates profile remote-readiness, identifies gaps and missing keywords
- **Agent 2 (Re-Analyzer)**: Validates analysis, finds overlooked opportunities, provides market insights
- **Agent 3 (Rewriter)**: Creates optimized headline, about section, experience bullets, and skills list
- **Agent 4 (Reviewer)**: Quality scores profile, checks ATS compatibility, provides final recommendations

### 🔧 Multiple AI Providers
- **OpenAI** (GPT-4o-mini) - Premium quality
- **Anthropic** (Claude 3.5 Sonnet) - Advanced reasoning
- **Hugging Face** (Mistral, Zephyr, FLAN-T5) - Free tier
- **Demo Mode** - Works offline without API keys

### 📥 Flexible Data Input
- 📋 **Copy-Paste** (Easiest method)
- 🔗 **Browser Console Auto-Extract** (JavaScript snippet)
- 📄 **LinkedIn PDF Export** (Official LinkedIn feature)
- 🌐 **URL Scraper** (Limited functionality)

### 💾 Data Privacy
- ✅ 100% Private & Offline
- ✅ All data stays on your computer
- ✅ No external data sharing
- ✅ Local JSON storage

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11 or higher
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/linkedin-ai-optimizer.git
cd linkedin-ai-optimizer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
```
Local URL: http://localhost:8501
```

---

## 📦 Dependencies

```txt
streamlit>=1.28.0
langchain>=0.1.0
langchain-openai>=0.0.2
langchain-anthropic>=0.1.0
langchain-huggingface>=0.0.1
langchain-community>=0.0.10
huggingface-hub>=0.19.0
requests>=2.31.0
beautifulsoup4>=4.12.0
PyPDF2>=3.0.0
```

---

## 🎮 How to Use

### Step 1: Configure AI Provider
1. Open the sidebar
2. Select AI provider (Demo Mode, Hugging Face, OpenAI, or Anthropic)
3. Enter your API key (get free keys from providers)
4. Click "Test API Connection" to verify

### Step 2: Input Your Profile
1. Go to **📝 Input** tab
2. Enter your **Target Remote Role** (e.g., "ServiceNow Developer - Gen AI")
3. Choose input method:
   - **Copy-Paste**: Manually paste each section
   - **Browser Console**: Use JavaScript auto-extractor
   - **PDF Upload**: Upload LinkedIn PDF export
4. Save profile data

### Step 3: Run Analysis
1. Go to **🤖 Analysis** tab
2. Click "▶️ Run Multi-Agent Analysis"
3. Watch the 4 agents work through your profile

### Step 4: Get Results
1. Go to **📊 Results** tab
2. Review optimized profile sections
3. Download or copy optimized content
4. Generate step-by-step modification guide
5. Update your LinkedIn profile!

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit Frontend UI            │
│  (Input → Analysis → Results Tabs)       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Multi-Agent System Controller       │
└──────────────┬──────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
┌──────────┐      ┌──────────┐
│ Agent 1  │      │ Agent 2  │
│ Analyzer │──────│Re-Analyze│
└────┬─────┘      └─────┬────┘
     │                  │
     └────────┬─────────┘
              ▼
        ┌──────────┐
        │ Agent 3  │
        │ Rewriter │
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │ Agent 4  │
        │ Reviewer │
        └────┬─────┘
             │
             ▼
       ┌───────────┐
       │  Results  │
       │  Export   │
       └───────────┘
```

---

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit |
| **Language** | Python 3.11+ |
| **AI/ML** | LangChain, OpenAI, Anthropic, Hugging Face |
| **Web Scraping** | BeautifulSoup4, Requests |
| **PDF Processing** | PyPDF2 |
| **Data Storage** | JSON (Local) |

---

## 📸 Screenshots

### Input Interface
![Input Tab](screenshots/input-tab.png)
*Multiple methods to import your LinkedIn profile*

### Multi-Agent Analysis
![Analysis Tab](screenshots/analysis-tab.png)
*Watch AI agents analyze your profile in real-time*

### Optimized Results
![Results Tab](screenshots/results-tab.png)
*Get ATS-optimized, keyword-rich profile content*

---

## 🎯 Use Cases

### For Job Seekers
- ✅ Optimize profile for remote ServiceNow + Gen AI roles
- ✅ Increase recruiter visibility with keyword optimization
- ✅ Improve ATS compatibility for better job application success
- ✅ Get professional profile rewriting in minutes

### For Career Changers
- ✅ Transition into Gen AI and ServiceNow careers
- ✅ Identify skill gaps for target roles
- ✅ Learn what recruiters look for in profiles

### For Developers
- ✅ Learn multi-agent AI system architecture
- ✅ Understand LangChain integration patterns
- ✅ Practice with multiple LLM providers
- ✅ Build portfolio projects with real-world impact

---

## 🔑 API Keys (Optional)

### Hugging Face (Free) 🆓
1. Visit [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Select "Read" permission
4. Copy token (starts with `hf_`)

### OpenAI 💰
1. Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create new API key
3. Add billing information
4. Copy key (starts with `sk-`)

### Anthropic 💰
1. Visit [https://console.anthropic.com/](https://console.anthropic.com/)
2. Generate API key
3. Copy key

**Or use Demo Mode** - No API key needed! Works offline with professional templates.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **LangChain** for the AI orchestration framework
- **Hugging Face** for free AI model access
- **OpenAI & Anthropic** for powerful language models

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/YOUR_USERNAME/linkedin-ai-optimizer/issues)
- **LinkedIn**: [Connect with me](https://linkedin.com/in/YOUR_PROFILE)
- **Email**: your.email@example.com

---

## 🌟 Star this repo if it helped you!

If this project helped optimize your LinkedIn profile or land a remote job, please ⭐ star this repository and share it with others!

---

## 📊 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/linkedin-ai-optimizer?style=social)
![GitHub Forks](https://img.shields.io/github/forks/YOUR_USERNAME/linkedin-ai-optimizer?style=social)
![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/linkedin-ai-optimizer)

---

**Built with ❤️ for remote job seekers worldwide**
# linkedin-ai-optimizer
