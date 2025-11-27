# 🧠 AceAi - AI-Powered Study Companion

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

AceAi is a **free, multimodal AI study platform** that combines smart scheduling, real-time focus monitoring, adaptive practice, and evidence-based learning techniques in one integrated workflow.

## 🚀 Features

- **🎯 Smart Study Scheduler** - AI-powered adaptive planning
- **🔍 Focus Monitor** - Webcam-based attention tracking
- **💡 AI Topic Explainer** - Instant explanations at any level
- **📊 Practice Generator** - Unlimited adaptive questions
- **📝 Notes to Flashcards** - Auto-convert notes to smart flashcards
- **📈 Progress Dashboard** - Comprehensive learning analytics

## 🛠️ Installation
# AceAi One-Click Installer - FIXED
Write-Host "🚀 Setting up AceAi Study Companion..." -ForegroundColor Green

# CORRECT repository URL
$repoUrl = "https://github.com/EncryptedMind-0/AceAi-Your-Study-Companion/archive/refs/heads/main.zip"
$zipFile = "AceAi.zip"

Write-Host "📥 Downloading AceAi files from correct repository..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $repoUrl -OutFile $zipFile

# Extract files
Write-Host "📂 Extracting files..." -ForegroundColor Yellow
Expand-Archive -Path $zipFile -DestinationPath . -Force
Move-Item -Path "AceAi-Your-Study-Companion-main\*" -Destination "." -Force
Remove-Item -Path "AceAi-Your-Study-Companion-main" -Force -Recurse
Remove-Item -Path $zipFile -Force

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install streamlit opencv-python numpy transformers torch streamlit-webrtc av Pillow pandas requests

# Run the application
Write-Host "🎯 Starting AceAi..." -ForegroundColor Green
Write-Host "👉 The app will open at http://localhost:8501" -ForegroundColor Cyan
streamlit run app.py

## 📦 Requirements
See requirements.txt for full list of dependencies.

## 🎯 Quick Start
Install dependencies:

pip install -r requirements.txt

Run: 

streamlit run app.py

Open http://localhost:8501 in your browser

Allow camera access for focus monitoring

Start studying smarter!

## 🔧 Tech Stack
Frontend: Streamlit

Computer Vision: OpenCV, Haarcascades

AI/ML: Transformers (Hugging Face), PyTorch

Real-time Processing: WebRTC, Streamlit-WebRTC

Data Processing: NumPy, Pandas

## 📚 Research Basis
AceAi implements proven learning science principles:

Spaced Repetition (Cepeda et al., 2008)

Active Recall (Karpicke & Roediger, 2008)

Multimedia Learning (Mayer, 2005)

Engagement Detection (D'Mello et al., 2016)

## 🌟 Why AceAi?
Feature	AceAi	Competitors
Price	Free	$8-15/month
Focus Tracking	✅	❌
Integrated Workflow	✅	❌
Research-Based	✅	❌
## 🗺️ Roadmap
Mobile app development

Advanced AI tutors by subject

Institutional/LMS integration

Offline functionality

Multi-language support

## 🤝 Contributing
We welcome contributions! Please see our Contributing Guidelines and Code of Conduct.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author
Ramanan Karthikeyan

GitHub: @EncryptedMind-0

## 🙏 Acknowledgments
Learning science research community

Open-source AI/ML libraries

Streamlit team for amazing framework
