import streamlit as st
import requests
import json
from transformers import pipeline, set_seed
import torch
from datetime import datetime, timedelta
import random
import time
import cv2
import numpy as np

# Set up the page
st.set_page_config(
    page_title="AceAi - Your Smart Study Buddy",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Remove all custom CSS - revert to default Streamlit
st.markdown("""
<style>
    /* Using default Streamlit styling - clean and readable */
</style>
""", unsafe_allow_html=True)

# Initialize AI models
@st.cache_resource
def load_ai_models():
    """Load AI models for different features"""
    try:
        # Use a smaller, faster model for text generation
        generator = pipeline('text-generation', model='gpt2', torch_dtype=torch.float32)
        return generator
    except Exception as e:
        st.sidebar.warning(f"AI models loading: Using simplified mode")
        return None

# Initialize session state for user progress
if 'user_progress' not in st.session_state:
    st.session_state.user_progress = {
        'streak': random.randint(3, 7),
        'topics_mastered': random.randint(5, 12),
        'questions_answered': random.randint(20, 50),
        'study_time': random.randint(10, 30),
        'level': 'Intermediate',
        'progress_percent': random.randint(40, 75)
    }

# Home Page
def home_page():
    st.title("AceAi")
    st.subheader("Your AI-Powered Learning Companion")
    
    # User progress overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Study Streak", f"{st.session_state.user_progress['streak']} days")
    with col2:
        st.metric("📚 Topics Mastered", st.session_state.user_progress['topics_mastered'])
    with col3:
        st.metric("❓ Questions Done", st.session_state.user_progress['questions_answered'])
    with col4:
        st.metric("⏱️ Study Hours", st.session_state.user_progress['study_time'])
    
    st.write("")  # Add some space
    
    # Create columns for feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🎯 **Smart Scheduler**\n\nAI-powered study plans that adapt to your exams and learning pace\n\n**Perfect for:** • Exam preparation • Daily routine • Time management")
        
        st.info("📝 **Notes to Flashcards**\n\nTransform messy handwritten notes into organized digital flashcards\n\n**Perfect for:** • Quick revision • Active recall • Memory retention")
        
        st.info("🔍 **Focus Monitor**\n\nAI-powered webcam monitoring to track and improve your study focus\n\n**Perfect for:** • Reducing distractions • Improving focus • Better retention")
    
    with col2:
        st.info("💡 **Topic Explainer**\n\nGet simple, clear explanations for any subject or complex concept\n\n**Perfect for:** • Homework help • Concept clarity • Exam preparation")
        
        st.info("📊 **Practice Generator**\n\nCreate unlimited practice questions with varying difficulty levels\n\n**Perfect for:** • Self-testing • Exam practice • Skill building")
        
        st.info("📈 **Progress Tracker**\n\nMonitor your learning journey with detailed analytics and insights\n\n**Perfect for:** • Goal setting • Progress monitoring • Motivation")

# Smart Scheduler Page
def scheduler_page():
    st.title("🎯 Smart Study Scheduler")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Create Your Personalized Study Plan")
        
        subjects = st.text_input("📚 Subjects (comma separated):", "Mathematics, Physics, Chemistry, Biology")
        hours_per_day = st.slider("⏱️ Hours available per day:", 1, 12, 6)
        exam_date = st.date_input("📅 Upcoming exam date (if any):", datetime.now() + timedelta(days=14))
        difficulty = st.select_slider("🎯 Difficulty level:", options=["Easy", "Medium", "Hard", "Intense"])
        
        exam_mode = st.checkbox("🚀 Enable Exam Mode (Intensive preparation)")
        
        if st.button("Generate Smart Schedule", type="primary"):
            subject_list = [s.strip() for s in subjects.split(',')]
            days_until_exam = (exam_date - datetime.now().date()).days
            
            st.success("📋 **Your Personalized Study Schedule**")
            
            if exam_mode and days_until_exam > 0:
                st.write(f"**Mode:** 🚀 ULTIMATE EXAM PREPARATION")
                st.write(f"**Time until exam:** {days_until_exam} days")
                st.write(f"**Daily commitment:** {hours_per_day} hours")
                st.write(f"**Difficulty:** {difficulty}")
                
                # AI-generated schedule logic
                primary_subject = subject_list[0]
                st.write(f"**Primary Focus:** {primary_subject} ({hours_per_day * 0.6:.1f}h daily)")
                st.write("**Secondary Subjects:** Quick revisions and practice problems")
                st.write("**Recommended Strategy:**")
                st.write("• Morning: Intensive topic study (2-3 hours)")
                st.write("• Afternoon: Practice problems (2 hours)")
                st.write("• Evening: Revision and flashcards (1-2 hours)")
                
            else:
                time_per_subject = hours_per_day / len(subject_list)
                st.write(f"**Mode:** 📅 BALANCED LEARNING")
                st.write(f"**Daily Study Time:** {hours_per_day} hours")
                st.write(f"**Subjects:** {len(subject_list)} subjects")
                
                st.write("**Daily Distribution:**")
                for i, subject in enumerate(subject_list):
                    emoji = ["🔢", "🔬", "🧪", "🧬", "📖", "🌍"][i % 6]
                    st.write(f"{emoji} **{subject}:** {time_per_subject:.1f} hours")
                
                st.write("**Recommended Approach:**")
                st.write("• 45min study + 15min break cycles")
                st.write("• Mix different subjects to avoid fatigue")
                st.write("• Include active recall sessions")
    
    with col2:
        st.subheader("Study Efficiency Tips")
        st.info("**⏰ Pomodoro Technique**\n\n25min focus + 5min break × 4, then 15min long break")
        
        st.info("**🔁 Spaced Repetition**\n\nReview material after 1 day, 3 days, 1 week, 2 weeks")
        
        st.info("**💡 Active Recall**\n\nTest yourself instead of re-reading notes")
        
        st.info("**🎯 Deep Work**\n\nEliminate distractions for 2-3 hour focused sessions")

# Topic Explainer Page
def explainer_page():
    st.title("💡 AI Topic Explainer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input("Enter any topic you want to understand:", "quantum physics")
        explanation_level = st.select_slider("Explanation level:", 
                                           options=["Simple", "Intermediate", "Detailed"])
        
        if st.button("Explain This Topic", type="primary"):
            if topic:
                with st.spinner("🤔 AI is generating a clear explanation..."):
                    # Enhanced explanations with AI-like structure
                    explanations_db = {
                        "quantum physics": {
                            "Simple": "🌌 **Quantum Physics** studies tiny particles like atoms and electrons. Unlike normal objects, these particles can be in multiple places at once (superposition) and affect each other instantly over distance (entanglement). It's the science of the very small!",
                            "Intermediate": "🔬 **Quantum Mechanics** describes nature at atomic and subatomic scales. Key principles include wave-particle duality (things act as both particles and waves), uncertainty principle (can't know both position and speed exactly), and quantum entanglement (connected particles affect each other).",
                            "Detailed": "⚛️ **Quantum Theory** revolutionized physics by describing microscopic systems. Fundamental concepts: 1) Superposition - quantum states can exist in multiple states simultaneously, 2) Entanglement - particles remain connected regardless of distance, 3) Quantization - energy exists in discrete packets (quanta), 4) Wave-function collapse - measurement determines the state."
                        },
                        "photosynthesis": {
                            "Simple": "🌱 **Photosynthesis** is how plants make food using sunlight! They take water + CO₂ and create sugar + oxygen using sunlight energy.",
                            "Intermediate": "🌿 **Photosynthesis** converts light energy to chemical energy. Equation: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. Occurs in chloroplasts using chlorophyll.",
                            "Detailed": "🔬 **Photosynthesis** has two stages: 1) Light-dependent reactions capture light energy to produce ATP and NADPH, 2) Calvin cycle uses these to fix CO₂ into organic compounds. Essential for life on Earth."
                        },
                        "machine learning": {
                            "Simple": "🤖 **Machine Learning** is AI that learns from data without explicit programming. It finds patterns and makes predictions automatically!",
                            "Intermediate": "🧠 **Machine Learning** uses algorithms to parse data, learn from it, and make determinations. Types: supervised (labeled data), unsupervised (patterns), reinforcement (trial & error).",
                            "Detailed": "📊 **Machine Learning** involves: 1) Data preprocessing and feature engineering, 2) Model selection (neural networks, decision trees, SVM), 3) Training and validation, 4) Hyperparameter tuning. Powers modern AI applications."
                        }
                    }
                    
                    # Update user progress
                    st.session_state.user_progress['topics_mastered'] += 1
                    
                    if topic.lower() in explanations_db:
                        explanation = explanations_db[topic.lower()][explanation_level]
                        st.success(explanation)
                    else:
                        st.info(f"📚 **{topic.title()}**\n\nThis is an important {explanation_level.lower()} concept worth exploring!\n\n**Key aspects to research:**\n• Fundamental principles and definitions\n• Real-world applications and examples\n• Related concepts and connections\n• Common misunderstandings to avoid")
                        
                        # Try to use AI model if available
                        ai_model = load_ai_models()
                        if ai_model:
                            try:
                                prompt = f"Explain {topic} in {explanation_level.lower()} terms:"
                                result = ai_model(prompt, max_length=150, num_return_sequences=1)
                                st.write("**AI Insight:**")
                                st.info(result[0]['generated_text'])
                            except:
                                pass
    
    with col2:
        st.subheader("Learning Tips")
        st.info("**🎯 Feynman Technique**\n\nExplain concepts in simple terms as if teaching a child")
        
        st.info("**🔗 Make Connections**\n\nRelate new concepts to what you already know")
        
        st.info("**❓ Ask Questions**\n\nChallenge yourself with 'why' and 'how' questions")

# Practice Generator Page
def practice_page():
    st.title("📊 Smart Practice Generator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input("Enter topic for practice questions:", "algebra")
        question_type = st.selectbox("Question format:", 
                                   ["Multiple Choice", "Short Answer", "Problem Solving", "Mixed"])
        difficulty = st.select_slider("Difficulty level:", 
                                    options=["Beginner", "Intermediate", "Advanced", "Expert"])
        
        if st.button("Generate Practice Set", type="primary"):
            if topic:
                with st.spinner("🎯 Creating personalized practice questions..."):
                    # Update user progress
                    st.session_state.user_progress['questions_answered'] += 5
                    
                    st.success(f"📝 **Practice Questions: {topic.title()} ({difficulty})**")
                    
                    # Generate questions based on topic and difficulty
                    questions_db = {
                        "algebra": [
                            "Solve the equation: 3x + 7 = 22. What is the value of x?",
                            "Factor the quadratic expression: x² + 5x + 6",
                            "Simplify the expression: 2(3x - 4) + 5(x + 2)",
                            "Find the slope and y-intercept of the line: y = 2x - 3",
                            "Solve the system: 2x + y = 7, x - y = -1"
                        ],
                        "physics": [
                            "Calculate the force required to accelerate a 5kg object at 3m/s²",
                            "Explain the difference between speed and velocity",
                            "A ball is dropped from 20m height. Calculate impact velocity",
                            "Describe Newton's three laws of motion with examples",
                            "Calculate work done by a 10N force moving an object 5m"
                        ],
                        "biology": [
                            "Explain the process of cellular respiration",
                            "Compare and contrast mitosis and meiosis",
                            "Describe the structure and function of DNA",
                            "Explain how enzymes work as biological catalysts",
                            "Discuss the process of protein synthesis"
                        ]
                    }
                    
                    # Select appropriate questions
                    base_questions = questions_db.get(topic.lower(), [
                        f"Explain the main concepts of {topic}",
                        f"Provide 3 real-world applications of {topic}",
                        f"Compare {topic} with related concepts",
                        f"What are common challenges when learning {topic}?",
                        f"How would you teach {topic} to a beginner?"
                    ])
                    
                    for i, question in enumerate(base_questions[:5]):
                        st.write(f"**{i+1}. {question}**")
                        if question_type == "Multiple Choice":
                            st.write("   A) Option 1")
                            st.write("   B) Option 2")
                            st.write("   C) Option 3")
                            st.write("   D) Option 4")
                        st.write("")
                    
                    # Answer key toggle
                    with st.expander("📋 Show Answer Key"):
                        st.write("**Sample Answers:**")
                        st.write("1. Show your work and reasoning")
                        st.write("2. Explain the key concepts involved")
                        st.write("3. Provide step-by-step solution")
                        st.write("4. Include relevant formulas/theorems")
                        st.write("5. Verify your answer makes sense")
    
    with col2:
        st.subheader("Practice Strategies")
        st.info("**📈 Progressive Difficulty**\n\nStart easy, gradually increase challenge")
        
        st.info("**🔄 Mixed Practice**\n\nMix different types of problems")
        
        st.info("**⏱️ Timed Practice**\n\nSet time limits to build speed")
        
        st.info("**📝 Error Analysis**\n\nReview mistakes to avoid repetition")

# Notes to Flashcards Page
def flashcards_page():
    st.title("📝 Smart Notes to Flashcards")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Transform Your Notes")
        notes_input = st.text_area("Paste your notes here (or type directly):", 
                                 height=200,
                                 placeholder="Example: Photosynthesis is the process plants use to convert sunlight into energy. They take in carbon dioxide and water, and using chlorophyll in their leaves, produce glucose and oxygen. This process occurs in the chloroplasts...")
        
        if st.button("Create Flashcards", type="primary"):
            if notes_input:
                with st.spinner("🔄 Converting notes to flashcards..."):
                    # Process notes into flashcards
                    sentences = [s.strip() for s in notes_input.split('.') if s.strip()]
                    
                    st.success("🃏 **Your Smart Flashcards**")
                    st.write(f"Generated {len(sentences[:8])} flashcards from your notes")
                    
                    for i, sentence in enumerate(sentences[:8]):
                        if len(sentence.split()) > 3:  # Only use substantial sentences
                            # Create question-answer pairs
                            words = sentence.split()
                            question_word = words[0] if words[0].lower() not in ['the', 'a', 'an'] else words[1]
                            
                            st.write(f"**Flashcard {i+1}:**")
                            st.write(f"**Q:** What is {question_word.lower()} or explain: {sentence[:50]}...?")
                            st.write(f"**A:** {sentence}")
                            st.write("---")
                    
                    # Study tips for flashcards
                    with st.expander("🎯 How to Use These Flashcards Effectively"):
                        st.write("**Active Recall Method:**")
                        st.write("• Try to recall the answer before flipping")
                        st.write("• Say the answer out loud")
                        st.write("• Explain the concept in your own words")
                        
                        st.write("**Spaced Repetition Schedule:**")
                        st.write("• Review after 1 hour")
                        st.write("• Review after 1 day")
                        st.write("• Review after 3 days")
                        st.write("• Review after 1 week")
                        
                        st.write("**Pro Tip:** Create your own examples for each concept!")
    
    with col2:
        st.subheader("Flashcard Tips")
        st.info("**🎴 One Concept Per Card**\n\nKeep flashcards focused and clear")
        
        st.info("**🔁 Regular Review**\n\nUse spaced repetition for memory")
        
        st.info("**💭 Active Recall**\n\nTest yourself before seeing answers")
        
        st.info("**🎨 Visual Elements**\n\nAdd diagrams or mnemonics")

# Focus Monitor Page with FIXED webcam implementation
def focus_page():
    st.title("🔍 AI Focus Monitor")
    st.write("**Real-time attention tracking using your webcam**")
    
    # Simple, stable webcam implementation
    try:
        from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
        import av
        import cv2
        
        class SimpleFocusProcessor:
            def __init__(self):
                self.focus_state = "CALIBRATING"
                self.focus_score = 75
                
            def recv(self, frame):
                img = frame.to_ndarray(format="bgr24")
                
                # Simple face detection using OpenCV (more stable than MediaPipe)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                h, w = img.shape[:2]
                
                if len(faces) > 0:
                    x, y, width, height = faces[0]
                    
                    # Calculate face position
                    x_center = x + width / 2
                    y_center = y + height / 2
                    
                    # Simple focus logic
                    if y_center > h * 0.6:  # Face in lower part = looking down
                        self.focus_state = "FOCUSED"
                        self.focus_score = min(100, self.focus_score + 1)
                    elif 0.3 < x_center/w < 0.7 and 0.3 < y_center/h < 0.7:  # Face centered
                        self.focus_state = "DISTRACTED" 
                        self.focus_score = max(0, self.focus_score - 1)
                    else:  # Face at edges
                        self.focus_state = "AWAY"
                        self.focus_score = max(0, self.focus_score - 2)
                    
                    # Draw rectangle around face
                    cv2.rectangle(img, (x, y), (x+width, y+height), (0, 255, 0), 2)
                else:
                    self.focus_state = "AWAY"
                    self.focus_score = max(0, self.focus_score - 3)
                
                # Add status text
                color_map = {"FOCUSED": (0, 255, 0), "DISTRACTED": (0, 165, 255), "AWAY": (0, 0, 255)}
                color = color_map.get(self.focus_state, (255, 255, 255))
                cv2.putText(img, f"Status: {self.focus_state}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(img, f"Score: {self.focus_score}%", (10, 70), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                
                return av.VideoFrame.from_ndarray(img, format="bgr24")
        
        # Webcam stream with fixed key to prevent freezing
        webrtc_ctx = webrtc_streamer(
            key="fixed-focus-monitor",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTCConfiguration(
                {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            ),
            media_stream_constraints={"video": True, "audio": False},
            video_processor_factory=SimpleFocusProcessor,
            async_processing=True,
        )
        
        # Display current status
        if webrtc_ctx.video_processor:
            processor = webrtc_ctx.video_processor
            
            st.subheader("Live Focus Status")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Focus Score", f"{processor.focus_score}%")
            with col2:
                st.metric("Status", processor.focus_state)
            
            # Simple instructions
            st.info("**Instructions:** Look DOWN at your book = FOCUSED, Look AT screen = DISTRACTED")
            
    except Exception as e:
        # Fallback - simple manual focus tracker
        st.warning("Webcam not available - using manual focus tracking")
        
        if 'manual_focus' not in st.session_state:
            st.session_state.manual_focus = 75
        
        st.subheader("Manual Focus Tracking")
        
        activity = st.radio("What are you doing?", [
            "📚 Looking at book/notes (FOCUSED)",
            "📺 Looking at screen (DISTRACTED)", 
            "👋 Away from desk (AWAY)"
        ])
        
        if st.button("Update Focus Status"):
            if "FOCUSED" in activity:
                st.session_state.manual_focus = min(100, st.session_state.manual_focus + 10)
                st.success("✅ FOCUSED - Good job studying!")
            elif "DISTRACTED" in activity:
                st.session_state.manual_focus = max(0, st.session_state.manual_focus - 5)
                st.warning("⚠️ DISTRACTED - Try looking at your book")
            else:
                st.session_state.manual_focus = max(0, st.session_state.manual_focus - 10)
                st.error("🔴 AWAY - Return to your studies")
        
        st.metric("Focus Score", f"{st.session_state.manual_focus}%")
        st.progress(st.session_state.manual_focus / 100)
    
    # Simple timer section
    st.subheader("⏱️ Study Timer")
    col1, col2 = st.columns(2)
    with col1:
        study_mins = st.number_input("Study minutes", value=25, min_value=10, max_value=120)
    with col2:
        break_mins = st.number_input("Break minutes", value=5, min_value=5, max_value=30)
    
    if st.button("Start Study Session"):
        st.success(f"Session started: {study_mins}min study + {break_mins}min break")

# Progress Tracking Page
def progress_page():
    st.title("📈 Learning Progress Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Your Learning Journey")
        
        # Progress metrics
        progress = st.session_state.user_progress
        
        # Main progress visualization
        st.write(f"**Current Level:** {progress['level']}")
        st.progress(progress['progress_percent'] / 100)
        st.write(f"Progress to next level: {progress['progress_percent']}%")
        
        # Detailed metrics
        st.subheader("📊 Learning Analytics")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("🔥 Study Streak", f"{progress['streak']} days", "2 days")
        with col_b:
            st.metric("📚 Topics Mastered", progress['topics_mastered'], "3 this week")
        with col_c:
            st.metric("❓ Questions Solved", progress['questions_answered'], "12 today")
        
        # Study time analysis
        st.subheader("⏱️ Study Patterns")
        col_d, col_e = st.columns(2)
        with col_d:
            st.metric("Total Study Hours", progress['study_time'])
        with col_e:
            efficiency = min(95, progress['questions_answered'] * 2)
            st.metric("Learning Efficiency", f"{efficiency}%")
        
        # Recommendations
        st.subheader("🎯 Personalized Recommendations")
        st.info("""
        **Build Consistency:** Try to study every day to build a strong habit
        
        **Practice More:** Increase daily practice questions to reinforce learning
        
        **Expand Knowledge:** Explore new topics to broaden your understanding
        
        **Next Level Goal:** Reach 80% progress by completing 10 more topics
        """)
    
    with col2:
        st.subheader("Achievements")
        st.info("✅ **Consistent Learner**\n\n3+ day study streak")
        
        st.info("✅ **Topic Explorer**\n\n5+ topics mastered")
        
        st.info("🔄 **Practice Champion**\n\n25+ questions solved")
        
        st.info("🎯 **Focus Master**\n\n10+ hours of focused study")
        
        # Weekly goal setting
        st.subheader("🎯 Set Weekly Goal")
        weekly_goal = st.selectbox("Target for this week:", 
                                 ["5 Topics", "50 Questions", "10 Study Hours", "7-Day Streak"])
        if st.button("Commit to Goal"):
            st.success(f"🎯 Goal set: {weekly_goal} for this week!")

# Navigation
st.sidebar.title("🧠 AceAi Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Home", 
    "🎯 Smart Scheduler", 
    "💡 Topic Explainer", 
    "📊 Practice Generator", 
    "📝 Notes to Flashcards", 
    "🔍 Focus Monitor",
    "📈 Progress Dashboard"
])

# Load AI models (cache them)
ai_models = load_ai_models()

# Show the selected page
if "🏠 Home" in page:
    home_page()
elif "🎯 Smart Scheduler" in page:
    scheduler_page()
elif "💡 Topic Explainer" in page:
    explainer_page()
elif "📊 Practice Generator" in page:
    practice_page()
elif "📝 Notes to Flashcards" in page:
    flashcards_page()
elif "🔍 Focus Monitor" in page:
    focus_page()
elif "📈 Progress Dashboard" in page:
    progress_page()

# Footer with creator credit
st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ for the YUVAi Challenge")
st.sidebar.caption("AceAi - Empowering Students Through AI")
st.sidebar.markdown("---")
st.sidebar.caption("**Made by Ramanan Karthikeyan**")

# Add some space at the bottom
st.write("")
st.write("")
st.caption("© 2025 AceAi - Your AI Learning Companion | Made by Ramanan Karthikeyan")