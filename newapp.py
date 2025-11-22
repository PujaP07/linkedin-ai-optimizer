import streamlit as st
import json
import os
from datetime import datetime
import time
from huggingface_hub import InferenceClient

# Page config
st.set_page_config(
    page_title="LinkedIn Multi-Agent Optimizer",
    page_icon="💼",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.agent-box {
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 5px solid;
}
.agent1 { border-left-color: #3b82f6; background-color: #eff6ff; }
.agent2 { border-left-color: #10b981; background-color: #ecfdf5; }
.agent3 { border-left-color: #8b5cf6; background-color: #f5f3ff; }
.agent4 { border-left-color: #f59e0b; background-color: #fffbeb; }
.success-box {
    padding: 15px;
    background-color: #d1fae5;
    border-radius: 8px;
    border-left: 4px solid #10b981;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = {}
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}
if 'agent_logs' not in st.session_state:
    st.session_state.agent_logs = []

# Data directory
DATA_DIR = "linkedin_data"
os.makedirs(DATA_DIR, exist_ok=True)

def hf_api_call(api_token, model, prompt, max_length=500):
    """Hugging Face API call using InferenceClient"""
    try:
        client = InferenceClient(token=api_token)
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_length,
            temperature=0.7
        )
        response = completion.choices[0].message.content
        return response if response else "⚠️ Model returned empty response. Try again."
    except Exception as e:
        error_msg = str(e).lower()
        if "401" in error_msg or "unauthorized" in error_msg:
            return "❌ Invalid API token. Check your token in the sidebar."
        elif "404" in error_msg or "not found" in error_msg:
            return f"❌ Model not found or unavailable."
        elif "503" in error_msg or "loading" in error_msg:
            return "🔄 Model is loading. Wait 20-30 seconds and try again."
        elif "429" in error_msg or "rate limit" in error_msg:
            return "⏱️ Rate limit exceeded. Wait a minute or upgrade to HF Pro."
        elif "timeout" in error_msg:
            return "⏱️ Request timeout. Try again or use a smaller model."
        else:
            return f"❌ Error: {str(e)[:200]}"

class LinkedInAgent:
    """Base agent class"""
    def __init__(self, name, role, api_token, model):
        self.name = name
        self.role = role
        self.api_token = api_token
        self.model = model
    
    def log_activity(self, message):
        st.session_state.agent_logs.append({
            "agent": self.name,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": message
        })
    
    def generate(self, prompt, max_length=500):
        return hf_api_call(self.api_token, self.model, prompt, max_length)

class Agent1_Analyzer(LinkedInAgent):
    def execute(self, profile_data, context=None):
        self.log_activity("🔍 Starting comprehensive analysis...")
        prompt = f"""You are a LinkedIn Profile Analyzer for remote jobs. Analyze this profile:

TARGET ROLE: {profile_data.get('target_role', 'Remote position')}
HEADLINE: {profile_data.get('headline', 'Not provided')}
ABOUT: {profile_data.get('about', 'Not provided')[:500]}
EXPERIENCE: {profile_data.get('experience', 'Not provided')[:500]}
SKILLS: {profile_data.get('skills', 'Not provided')}

Provide analysis with:
1. Remote-Readiness Score (0-100)
2. Top 3 Strengths
3. Top 3 Critical Gaps
4. 5 Missing Keywords for ATS
5. Top 3 Priority Improvements"""
        
        response = self.generate(prompt, max_length=600)
        self.log_activity("✅ Analysis complete")
        return response

class Agent2_ReAnalyzer(LinkedInAgent):
    def execute(self, profile_data, context=None):
        self.log_activity("🔄 Re-analyzing and validating...")
        agent1_result = context.get('agent1_result', '')[:800]
        prompt = f"""You are a Critical Reviewer. Review this LinkedIn analysis:

ANALYSIS:
{agent1_result}

PROFILE TARGET: {profile_data.get('target_role')}

Provide:
1. Do you agree with the assessment? Why or why not?
2. 2 Overlooked opportunities
3. 2 Alternative improvement approaches
4. Market insight for this role"""
        
        response = self.generate(prompt, max_length=500)
        self.log_activity("✅ Re-analysis complete")
        return response

class Agent3_Rewriter(LinkedInAgent):
    def execute(self, profile_data, context=None):
        self.log_activity("✍️ Rewriting profile for remote roles...")
        prompt = f"""You are a LinkedIn Profile Writer. Create an optimized profile for: {profile_data.get('target_role')}

CURRENT HEADLINE: {profile_data.get('headline', 'Not provided')}
CURRENT ABOUT: {profile_data.get('about', 'Not provided')[:400]}

Create:
1. NEW HEADLINE (120 chars max, keyword-rich, remote-focused)
2. NEW ABOUT SECTION (2-3 short paragraphs, highlight remote skills)
3. 5 OPTIMIZED EXPERIENCE BULLETS (start with action verbs)
4. TOP 15 SKILLS (ATS-optimized, include relevant technologies)"""
        
        response = self.generate(prompt, max_length=800)
        self.log_activity("✅ Profile rewrite complete")
        return response

class Agent4_Reviewer(LinkedInAgent):
    def execute(self, profile_data, context=None):
        self.log_activity("🔎 Final quality review...")
        rewritten = context.get('agent3_result', '')[:800]
        prompt = f"""You are a Quality Reviewer. Review this optimized LinkedIn profile:

{rewritten}

TARGET: {profile_data.get('target_role')}

Provide:
1. Quality Score (0-100)
2. Top 3 Strengths
3. 2 Remaining Issues
4. ATS Compatibility Score (0-100)
5. Final Recommendation"""
        
        response = self.generate(prompt, max_length=500)
        self.log_activity("✅ Review complete")
        return response

def test_hf_connection(api_token, model):
    result = hf_api_call(api_token, model, "Hello! Tell me a very short joke.", max_length=50)
    return result

def run_multi_agent_system(profile_data, api_token, model):
    st.session_state.agent_logs = []
    results = {}
    
    agent1 = Agent1_Analyzer("Agent 1: Analyzer", "Initial Analysis", api_token, model)
    agent2 = Agent2_ReAnalyzer("Agent 2: Re-Analyzer", "Critical Review", api_token, model)
    agent3 = Agent3_Rewriter("Agent 3: Rewriter", "Profile Optimization", api_token, model)
    agent4 = Agent4_Reviewer("Agent 4: Reviewer", "Quality Assurance", api_token, model)
    
    progress = st.progress(0)
    status = st.empty()
    
    try:
        status.markdown("### 🤖 Agent 1: Analyzing profile...")
        progress.progress(25)
        results['agent1'] = agent1.execute(profile_data)
        if "❌" in results['agent1'] or "🔄" in results['agent1']:
            st.warning(results['agent1'])
            return None
        time.sleep(2)
        
        status.markdown("### 🤖 Agent 2: Re-analyzing...")
        progress.progress(50)
        results['agent2'] = agent2.execute(profile_data, {'agent1_result': results['agent1']})
        if "❌" in results['agent2'] or "🔄" in results['agent2']:
            st.warning(results['agent2'])
            return None
        time.sleep(2)
        
        status.markdown("### 🤖 Agent 3: Rewriting profile...")
        progress.progress(75)
        results['agent3'] = agent3.execute(profile_data, {
            'agent1_result': results['agent1'],
            'agent2_result': results['agent2']
        })
        if "❌" in results['agent3'] or "🔄" in results['agent3']:
            st.warning(results['agent3'])
            return None
        time.sleep(2)
        
        status.markdown("### 🤖 Agent 4: Final review...")
        progress.progress(100)
        results['agent4'] = agent4.execute(profile_data, {'agent3_result': results['agent3']})
        if "❌" in results['agent4'] or "🔄" in results['agent4']:
            st.warning(results['agent4'])
            return None
        
        status.markdown("### ✅ Multi-agent analysis complete!")
        return results
    except Exception as e:
        st.error(f"Error in multi-agent system: {e}")
        return None

def save_data(data, filename):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def load_data(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    st.title("💼 LinkedIn Multi-Agent Optimizer")
    st.markdown("### 🤗 Powered by Hugging Face (100% Free)")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Hugging Face Configuration")
        st.success("🆓 100% FREE - No credit card needed!")
        
        api_token = st.text_input(
            "Hugging Face Token",
            type="password",
            help="Get your free token at https://huggingface.co/settings/tokens"
        )
        
        with st.expander("📖 How to get HF Token", expanded=not api_token):
            st.markdown("""
            **Simple steps:**
            
            1. Go to [Hugging Face Tokens](https://huggingface.co/settings/tokens)
            2. Click **"Create new token"**
            3. Select **"Read"** permission
            4. Name it: `linkedin-optimizer`
            5. Click **"Create token"**
            6. **Copy** the token (starts with `hf_...`)
            7. **Paste** it above
            
            ✅ Takes 30 seconds!
            """)
        
        st.subheader("🤖 Select Model")
        model = st.selectbox(
            "Choose Model (100% Free Tier)",
            [
                "Qwen/Qwen2.5-7B-Instruct",
                "google/gemma-2-9b-it",
                "meta-llama/Llama-3.2-3B-Instruct",
                "mistralai/Mistral-7B-Instruct-v0.3"
            ],
            help="All models work on free tier (Nov 2025)"
        )
        
        model_info = {
            "Qwen/Qwen2.5-7B-Instruct": "⭐ Very fast & excellent",
            "google/gemma-2-9b-it": "🎯 Excellent quality",
            "meta-llama/Llama-3.2-3B-Instruct": "⚡ Fast & capable",
            "mistralai/Mistral-7B-Instruct-v0.3": "🚀 Classic & reliable"
        }
        st.caption(model_info.get(model, ""))
        
        st.divider()
        if api_token and st.button("🧪 Test Connection", use_container_width=True):
            with st.spinner("Testing..."):
                result = test_hf_connection(api_token, model)
                if "❌" in result:
                    st.error(result)
                elif "🔄" in result:
                    st.warning(result)
                else:
                    st.success("✅ Connection successful!")
                    st.write(f"Response: {result[:100]}...")
        
        st.divider()
        st.header("💾 Data Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save", use_container_width=True):
                if st.session_state.profile_data:
                    save_data(st.session_state.profile_data, "profile_data.json")
                    st.success("Saved!")
        with col2:
            if st.button("📂 Load", use_container_width=True):
                data = load_data("profile_data.json")
                if data:
                    st.session_state.profile_data = data
                    st.success("Loaded!")
                    st.rerun()
        
        st.caption(f"📁 {os.path.abspath(DATA_DIR)}")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📝 Input Profile", "🤖 Run Analysis", "📊 Results"])
    
    with tab1:
        st.header("Enter Your Profile Information")
        
        st.markdown("### 🎯 Target Position")
        target_role = st.text_input(
            "What remote role are you targeting?",
            value=st.session_state.profile_data.get('target_role', ''),
            placeholder="e.g., ServiceNow Developer - Gen AI, Senior DevOps Engineer",
            help="Be specific! Include technologies"
        )
        
        if target_role:
            st.session_state.profile_data['target_role'] = target_role
        
        if 'servicenow' in target_role.lower() or 'gen ai' in target_role.lower():
            st.success("🎯 ServiceNow + Gen AI is HOT for remote roles!")
            with st.expander("💡 Keywords to Include"):
                st.markdown("""
                **Must-Have Keywords:**
                - ServiceNow (ITSM, ITOM, CSM, HRSD)
                - Gen AI / Generative AI / LLM
                - Virtual Agent, Chatbot
                - Flow Designer, Integration Hub
                - API, REST, JavaScript, Python
                - Remote, Distributed, Async
                - Agile, Scrum, CI/CD
                """)
        
        st.divider()
        
        method = st.radio(
            "Choose input method:",
            ["📋 Copy-Paste (Easiest)", "🔗 Browser Console", "📄 Upload PDF"],
            horizontal=True
        )
        
        if method == "📋 Copy-Paste (Easiest)":
            with st.expander("📖 Instructions", expanded=True):
                st.markdown("""
                1. Open your LinkedIn profile
                2. Copy each section individually:
                   - **Headline**: Text under your name
                   - **About**: Click "Show more" → Copy all
                   - **Experience**: Copy recent jobs
                   - **Skills**: Copy your skills list
                3. Paste below in corresponding fields
                """)
            
            with st.form("profile_form"):
                st.markdown("**Copy each section from your LinkedIn profile:**")
                
                headline = st.text_area(
                    "📌 Headline",
                    value=st.session_state.profile_data.get('headline', ''),
                    placeholder="The text under your name on LinkedIn",
                    height=80
                )
                
                about = st.text_area(
                    "📄 About/Summary",
                    value=st.session_state.profile_data.get('about', ''),
                    placeholder="Your About section (click 'Show more' to see all)",
                    height=200
                )
                
                experience = st.text_area(
                    "💼 Recent Experience",
                    value=st.session_state.profile_data.get('experience', ''),
                    placeholder="Copy 1-2 recent jobs with descriptions",
                    height=150
                )
                
                skills = st.text_area(
                    "🛠️ Skills",
                    value=st.session_state.profile_data.get('skills', ''),
                    placeholder="Comma-separated: Python, ServiceNow, Gen AI, AWS, etc.",
                    height=100
                )
                
                submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
                
                if submitted:
                    st.session_state.profile_data.update({
                        'headline': headline,
                        'about': about,
                        'experience': experience,
                        'skills': skills,
                        'timestamp': datetime.now().isoformat()
                    })
                    st.success("✅ Profile saved! Go to '🤖 Run Analysis' tab")
                    st.balloons()
        
        elif method == "🔗 Browser Console":
            st.markdown("### Auto-Extract from LinkedIn")
            
            with st.expander("📖 Instructions", expanded=True):
                st.markdown("""
                1. Open your LinkedIn profile
                2. Press **F12** (Developer Tools)
                3. Click **Console** tab
                4. Paste this code and press Enter:
                """)
                
                st.code("""
const data = {
    headline: document.querySelector('.text-body-medium')?.innerText || '',
    about: document.querySelector('.pv-about__summary-text')?.innerText || '',
    experience: Array.from(document.querySelectorAll('.pvs-list__item--line-separated')).slice(0,2).map(e => e.innerText).join('\\n\\n'),
    skills: Array.from(document.querySelectorAll('.pvs-skill-category-entity__name')).map(s => s.innerText).join(', ')
};
copy(JSON.stringify(data, null, 2));
alert('✅ Copied! Paste in the app.');
                """, language="javascript")
            
            json_input = st.text_area(
                "Paste the JSON here:",
                height=200,
                placeholder='{"headline": "...", "about": "...", ...}'
            )
            
            if st.button("📥 Import", use_container_width=True, type="primary"):
                try:
                    data = json.loads(json_input)
                    st.session_state.profile_data.update(data)
                    st.success("✅ Imported! Go to '🤖 Run Analysis' tab")
                    st.rerun()
                except:
                    st.error("❌ Invalid JSON")
        
        else:  # PDF Upload
            st.markdown("### Upload LinkedIn PDF")
            
            with st.expander("📖 How to export PDF"):
                st.markdown("""
                1. Go to your LinkedIn profile
                2. Click **"More"** (three dots)
                3. Select **"Save to PDF"**
                4. Upload below
                """)
            
            uploaded = st.file_uploader("Choose PDF", type=['pdf'])
            
            if uploaded and st.button("📄 Extract", type="primary"):
                try:
                    import PyPDF2
                    reader = PyPDF2.PdfReader(uploaded)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                    
                    st.info(f"✅ Extracted {len(text)} characters")
                    st.text_area("Preview:", text[:500], height=200)
                    
                    # Simple parsing
                    st.session_state.profile_data.update({
                        'about': text[:1000],
                        'experience': text[1000:2000],
                        'skills': text[2000:2500]
                    })
                    st.success("✅ Imported! Review and edit if needed.")
                    
                except ImportError:
                    st.error("❌ Install PyPDF2: pip install PyPDF2")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        if st.session_state.profile_data:
            st.divider()
            with st.expander("👀 Preview Your Data"):
                st.write("**Target:**", st.session_state.profile_data.get('target_role', 'Not set'))
                st.write("**Headline:**", st.session_state.profile_data.get('headline', '')[:100])
                st.write("**About:**", st.session_state.profile_data.get('about', '')[:200])
                st.write("**Skills:**", st.session_state.profile_data.get('skills', '')[:100])
    
    with tab2:
        st.header("🤖 Multi-Agent Analysis")
        
        if not api_token:
            st.error("⚠️ Enter your Hugging Face token in the sidebar!")
            st.stop()
        
        if not st.session_state.profile_data:
            st.warning("⚠️ Enter your profile in the 'Input Profile' tab first!")
            st.stop()
        
        if not st.session_state.profile_data.get('target_role'):
            st.error("⚠️ Specify your target role!")
            st.stop()
        
        st.info(f"🎯 Optimizing for: **{st.session_state.profile_data.get('target_role')}**")
        st.caption(f"🤖 Using: {model}")
        
        if st.button("▶️ Run 4-Agent Analysis", type="primary", use_container_width=True):
            with st.spinner("🤖 Agents working... (This may take 1-2 minutes)"):
                results = run_multi_agent_system(st.session_state.profile_data, api_token, model)
                
                if results:
                    st.session_state.analysis_results = results
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    save_data({
                        'profile': st.session_state.profile_data,
                        'results': results,
                        'timestamp': datetime.now().isoformat()
                    }, f'results_{timestamp}.json')
                    st.success("✅ Analysis complete! Check '📊 Results' tab")
                    st.balloons()
                else:
                    st.error("❌ Analysis failed. Check messages above.")
        
        if st.session_state.agent_logs:
            st.divider()
            st.subheader("📋 Agent Activity")
            for log in st.session_state.agent_logs:
                agent_num = log['agent'].split()[1].replace(':', '')
                st.markdown(f"""
                <div class="agent-box agent{agent_num}">
                    <strong>{log['agent']}</strong> <small>[{log['timestamp']}]</small><br>
                    {log['message']}
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.header("📊 Optimization Results")
        
        if not st.session_state.analysis_results:
            st.info("👆 Run the analysis first to see results here")
            st.stop()
        
        results = st.session_state.analysis_results
        
        with st.expander("🔍 Agent 1: Initial Analysis", expanded=True):
            st.markdown(results.get('agent1', 'No results'))
        
        with st.expander("🔄 Agent 2: Critical Review"):
            st.markdown(results.get('agent2', 'No results'))
        
        st.divider()
        st.markdown("## ✨ Your Optimized LinkedIn Profile")
        st.markdown("""
        <div class="success-box">
            📝 <strong>Ready to use!</strong> Copy these sections and paste directly into your LinkedIn profile.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(results.get('agent3', 'No results'))
        
        with st.expander("🔎 Agent 4: Quality Review"):
            st.markdown(results.get('agent4', 'No results'))
        
        st.divider()
        st.subheader("💾 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Save to File", use_container_width=True):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                content = f"""OPTIMIZED LINKEDIN PROFILE
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Role: {st.session_state.profile_data.get('target_role')}

{results.get('agent3', '')}

QUALITY REVIEW:
{results.get('agent4', '')}
"""
                path = os.path.join(DATA_DIR, f'linkedin_optimized_{timestamp}.txt')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                st.success(f"✅ Saved: {path}")
        
        with col2:
            st.download_button(
                "⬇️ Download TXT",
                data=results.get('agent3', ''),
                file_name=f"linkedin_optimized_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )

if __name__ == "__main__":
    main()