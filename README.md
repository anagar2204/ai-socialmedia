# 🚀 AI Social Media Content Studio

> An AI-powered social media marketing toolkit built with **Python**, **Streamlit**, and **OpenAI GPT**. Generate captions, image prompts, content calendars, and optimized hashtags — all from a single professional dashboard.

![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-ff4b4b?style=flat-square&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

---

## ✨ Features

| Module | Description |
|--------|-------------|
| **✍️ Caption Generator** | 3 caption variations + short caption + storytelling caption + 10 hashtags |
| **🎨 Image Prompt Generator** | 3 DALL-E / Midjourney-ready image prompts |
| **📅 Content Calendar** | 7-day social media plan with post ideas, themes & hashtags |
| **#️⃣ Hashtag Engine** | 15 optimized hashtags blending AI + curated trending data |

### UX Highlights
- 🎯 Modern SaaS-grade dashboard with card-style layout
- 📋 One-click copy to clipboard
- ⬇️ Download results as text / CSV
- 🔢 Live character counter for captions
- 🔄 Regenerate & clear buttons
- 🕐 Session history (last 3 outputs per module)
- ⚠️ Graceful error handling for missing API keys

---

## 📁 Project Structure

```
project-folder/
├── app.py                 # Streamlit dashboard (main entry point)
├── ai_engine.py           # Core LLM integration layer
├── content_modules.py     # High-level orchestration for all modules
├── hashtag_dataset.py     # Curated trending hashtag dataset
├── utils.py               # Formatting, clipboard, download helpers
├── requirements.txt       # Python dependencies
├── .env                   # API key (not committed to Git)
└── README.md              # This file
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-content-studio.git
cd ai-content-studio
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI API key

Open `.env` and replace the placeholder:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS (gradient header, card layout, Google Fonts)
- **Backend**: Python with modular architecture
- **AI**: OpenAI GPT-4o-mini via the `openai` Python SDK
- **Data**: pandas for calendar tables, curated hashtag dataset
- **Config**: python-dotenv for environment variable management

---

## 📸 Screenshots

> *Add screenshots here after running the app locally.*

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-module`)
3. Commit your changes (`git commit -m 'Add new module'`)
4. Push to the branch (`git push origin feature/new-module`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
  <strong>Built with ❤️ using Streamlit & OpenAI</strong>
</p>
