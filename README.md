
# 🤖 NEXUS — Virtual Assistant for NRI Group

> An intelligent web-based assistant built with **Streamlit**, designed to answer queries about the **NRI Group of Institutions** using **real-time website data**, **NLP**, and **text-to-speech** capabilities.

---

## 🧠 Overview

**NEXUS** is a smart AI-powered virtual assistant that can:
- Fetch **live data** from NRI Group’s official website.
- Understand **natural language queries** using **spaCy NLP**.
- Read out answers using **Google Text-to-Speech (gTTS)**.
- Maintain **conversation history** and allow quick re-queries.
- Provide a clean and beautiful **Streamlit-based GUI**.

---

## ✨ Features

### 🧩 Core Features
- 🔍 **Smart Search:** Ask questions about NRI Group, courses, faculty, admissions, etc.  
- 🗣️ **Voice Output:** Get responses as audio using gTTS.  
- 🌐 **Live Website Data:** Fetches and processes real-time data from official NRI URLs.  
- 💬 **Conversation History:** Keeps a track of your last few queries.  
- 🧠 **NLP-powered Understanding:** Uses spaCy to understand user intent and extract keywords.  
- 🎨 **Beautiful UI:** Custom CSS styling for a smooth and modern look.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend | Streamlit |
| NLP | spaCy |
| Web Scraping | BeautifulSoup |
| Text-to-Speech | gTTS |
| HTTP Requests | requests |
| Styling | Custom CSS |
| Language | Python 3.9+ |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/nexus-virtual-assistant.git
cd nexus-virtual-assistant
````

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

---

## 🚀 Run the App

Launch the Streamlit web app:

```bash
streamlit run nexus.py
```

Then open your browser at 👉 [http://localhost:8501](http://localhost:8501)

---

## 💬 How It Works

1. 🧍 User enters a natural language query (e.g., “Tell me about the admission process”).
2. 🧠 The app processes the text using **spaCy** and extracts meaningful keywords.
3. 🌐 It fetches real-time data from relevant NRI Group URLs using **requests + BeautifulSoup**.
4. 🔍 The assistant finds relevant sentences matching your query.
5. 🗣️ The response is displayed beautifully and optionally spoken out loud using **gTTS**.
6. 🕓 Your query and response are saved in the **conversation history**.

---

## 🎛️ Sidebar Features

| Option                | Description                                                      |
| --------------------- | ---------------------------------------------------------------- |
| **🎯 Features List**  | Overview of NEXUS features                                       |
| **📚 Topics**         | Shows available query topics (Courses, Faculty, Admission, etc.) |
| **🗑️ Clear History** | Clears the conversation memory                                   |
| **🚀 Quick Actions**  | Ready-made query buttons for instant answers                     |

---

## 🧩 Supported Topics

* 🏫 About NRI Group
* 📘 Courses
* 🧾 Admission Process
* 💻 Computer Science Department
* 👨‍🏫 Faculty
* 🏗️ Facilities
* 🎯 Vision & Mission
* 📞 Contact Information

---

## 📦 Dependencies

```
streamlit
requests
beautifulsoup4
spacy
gTTS
```

---

## 🔊 Example Interaction

**User:** “Tell me about computer science department”
**NEXUS:** “The Computer Science Department at NRI offers B.Tech and M.Tech programs focusing on AI, ML, and software engineering...”
🎧 *(Audio plays automatically)*

---

## 🧠 Smart NLP & Voice Integration

| Function           | Module                                     |
| ------------------ | ------------------------------------------ |
| Text Preprocessing | spaCy                                      |
| Keyword Extraction | Lemmatization + Stopword removal           |
| Speech Generation  | gTTS (Google Text-to-Speech)               |
| Data Fetching      | BeautifulSoup (Scrapes text intelligently) |

---

## 🧑‍💻 Author

**Satvik**
*AI DevSecOps Engineer | Streamlit Developer*


---

## 📜 License

MIT License © 2025 **Satvik**
Feel free to fork, modify, and enhance for educational or institutional use.

---

### 🪄 “NEXUS — Because every institution deserves its own smart assistant.”

