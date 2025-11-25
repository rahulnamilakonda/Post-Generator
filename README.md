# 🚀 Social Media Post Generator using LangChain

An AI-powered **social media post generator** built using **LangChain**, designed to help users create high-quality posts tailored for different social media platforms.

Generate professional, engaging, and platform-optimized posts for:
- **LinkedIn**
- **Instagram**
- **X (Twitter)**

---

## 🌟 Features

- ✨ Generate posts using just a topic or idea
- 🧠 LangChain-powered prompt templating and LLM orchestration
- 🎯 Platform-specific formatting, tone & structure
- 🔁 Supports iterative feedback & refinement
- 🔌 Easily extendable to new platforms
- 🔐 Works with **Gemini** and any other LangChain-supported LLM
- 🔄 Switch between LLMs easily via `chat_model.py`

---

## 🧰 Tech Stack

- **Python 3.10+**
- **LangChain / LangChain Core**
- **Gemini API**
- Optional: **OpenAI API**, **Claude**, etc.

---

## 📦 Installation

```bash
git clone https://github.com/rahulnamilakonda/Post-Generator
cd Post-Generator
pip install -r requirements.txt
```

---

## 🔐 Environment Variables Setup

Create a `.env` file in the project root and add:

```ini
GOOGLE_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key    # optional if you want to use OpenAI
```

These keys are required depending on which LLM you choose.

---

## 🔄 Select Your LLM Provider

All model configurations are inside:

```
chat_model.py
```

You can:
- Change between Gemini, OpenAI, or any supported model
- Update model names
- Adjust temperature and generation settings

This makes the project fully modular and easy to adapt.

---

## 🚀 Usage

### Interactive Mode

```bash
python main.py
```

Follow the prompts to:
1. Enter your post topic or idea
2. Select target platform (LinkedIn/Instagram/Twitter)
3. Get your AI-generated post
4. Optionally refine with feedback

### Command Line Mode

You can also generate posts directly via command line arguments:

```bash
python main.py <platform> <post_title>
```

**Examples:**
```bash
python main.py linkedin "MCP vs API"
python main.py linkedin MCP vs API
python main.py instagram "Top 10 Travel Destinations"
python main.py twitter "Breaking News in AI"
```

This will generate a post for the specified platform and topic, then save it directly.

### 📂 Output

Generated posts are automatically saved in the `output/` folder with the post title as the filename for easy access and organization.

---

## 📝 License

MIT License - feel free to use and modify!

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 👤 Author

**Rahul Namilakonda**

- GitHub: [@rahulnamilakonda](https://github.com/rahulnamilakonda)

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!