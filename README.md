# 🕰️ ChronoBot – AI Time Travel Chat

Ever wondered what it would be like to talk to a **robotic nurse from Delhi, 2125** or a **street vendor in Madurai, 1700**?

**ChronoBot** is a Python-based command-line chatbot powered by **Google Gemini**. It allows you to interact with fictional characters from different timelines — both historical and futuristic.

---

## 🌟 Features

- ✨ Chat with AI-generated characters from any year or place
- 🔮 Enter a timeline, location, and profession — get a fully roleplayed character
- 🧠 Powered by Google Gemini via the `google-generativeai` Python SDK
- 🎓 Great for learning, creativity, and storytelling

---

## 🛠 Tech Stack

- **Python 3**
- **Google Generative AI Python SDK** (`google-generativeai`)
- **Gradio**

---

## 🚀 How It Works

1. User enters:
   - `Timeline` (e.g., 1857, 2070)
   - `Location` (e.g., Coimbatore, Tokyo)
   - `Character Type` (e.g., king, soldier, vendor, activist)

2. Gemini API is prompted with a roleplay instruction using the details.

3. The bot responds **as if it were that character**, with appropriate tone, context, and attitude.

---
## 🖥️ Demo

Here’s a preview of the chatbot in action:

![ChronoBot Terminal Demo](./assets/demo1.png)
![ChronoBot Terminal Demo](./assets/demo2.png)


## 📦 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/S-Dhilipkumar/ai-time-travel-chat.git
   cd ai-time-travel-chat
