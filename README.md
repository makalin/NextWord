# NextWord

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![GitHub stars](https://img.shields.io/badge/github-stars-makalin/NextWord?style=social)
![GitHub forks](https://img.shields.io/badge/github-forks-makalin/NextWord?style=social)

NextWord is a real-time AI-powered cognitive assistant that listens to your speech and provides intelligent suggestions to keep your thoughts flowing. It features a dynamic mind map, real-time transcription, AI-powered idea generation, and contextual tag suggestions.

## ✨ Current Features

### 🎤 Real-Time Speech Recognition
* **Live Audio Transcription:** Uses Google Speech Recognition API for real-time voice-to-text conversion
* **Audio Level Monitoring:** Real-time audio level visualization with Web Audio API
* **Speech Detection:** Visual indicators when listening, analyzing, or waiting for speech

### 🧠 AI-Powered Intelligence
* **Context-Aware Suggestions:** AI analyzes your speech content and generates relevant idea suggestions
* **Smart Tag Generation:** Automatically creates topic tags based on speech context
* **Confidence Scoring:** Real-time confidence levels for AI suggestions
* **Document Analysis:** Upload documents or paste text for enhanced context understanding

### 🗺️ Interactive Mind Map
* **Dynamic Visualization:** Real-time mind map that grows as you speak
* **Smart Node Management:** Prevents duplicate nodes, highlights existing concepts
* **Clickable Elements:** Click on ideas or tags to continue exploring topics
* **Visual Connections:** Shows relationships between your thoughts

### 🎨 Professional UI/UX
* **16 Beautiful Themes:** Dark, Light, Cyber, Neon, Solar, Ocean, Forest, Cosmic, Steel, Aurora, Midnight, Sunset, Emerald, Volcanic, Arctic, Lavender
* **Multi-Language Support:** English, German, French, Turkish
* **Single-Screen Design:** Optimized layout fits everything without scrolling
* **Professional Settings:** Customizable AI behavior, confidence thresholds, suggestion cooldowns

### 📊 Advanced Features
* **Session Statistics:** Track ideas generated, tags created, average confidence
* **Document Upload:** Support for .txt, .md, .pdf, .doc, .docx files
* **Real-Time WebSocket Communication:** Low-latency bidirectional communication
* **Professional Controls:** Tag creation limits, idea filtering, auto-tagging options

## 🏗️ Architecture

### Frontend (SvelteKit)
* **Real-time Audio Capture:** MediaRecorder API for continuous audio streaming
* **WebSocket Client:** Persistent connection for real-time communication
* **Audio Level Monitoring:** Web Audio API for real-time volume visualization
* **Dynamic Mind Map:** SVG-based interactive visualization
* **Theme System:** CSS variables for dynamic theming
* **Multi-language Support:** Translation system with 4 languages

### Backend (FastAPI)
* **WebSocket Server:** Handles real-time audio and text communication
* **Speech Recognition:** Google Speech Recognition API integration
* **AI Analysis:** Context-aware idea and tag generation
* **Document Processing:** Text extraction and analysis for enhanced context
* **Session Management:** Tracks user sessions and statistics

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* Node.js 18+
* pnpm (recommended) or npm
* Microphone access

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/makalin/NextWord.git
   cd NextWord
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```bash
   cd ../frontend
   pnpm install
   ```

### Running the Application

1. **Start the backend server:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend server:**
   ```bash
   cd frontend
   pnpm run dev --port 3000
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🎯 Usage

1. **Start Recording:** Click the "Start Recording" button and allow microphone access
2. **Speak Naturally:** The app will transcribe your speech in real-time
3. **View Suggestions:** AI-generated ideas and tags will appear automatically
4. **Interact with Mind Map:** Click on ideas or tags to explore topics further
5. **Upload Documents:** Add context by uploading files or pasting text
6. **Customize Settings:** Adjust AI behavior, themes, and language preferences

## 🛠️ Technology Stack

### Frontend
- **SvelteKit:** Modern reactive framework
- **TypeScript:** Type-safe development
- **Web Audio API:** Real-time audio processing
- **WebSocket:** Real-time communication
- **SVG:** Interactive mind map visualization

### Backend
- **FastAPI:** High-performance Python web framework
- **WebSocket:** Real-time bidirectional communication
- **Speech Recognition:** Google Speech API
- **Python 3.8+:** Modern Python features

### Development Tools
- **pnpm:** Fast package manager
- **uvicorn:** ASGI server for FastAPI
- **Git:** Version control

## 🎨 Themes

NextWord includes 16 professionally designed themes:

- **Matrix Dark** - Classic green terminal aesthetic
- **Clean Light** - Modern light theme
- **Cyber Punk** - Neon cyberpunk style
- **Neon Glow** - Bright neon colors
- **Solar Flare** - Warm orange/yellow tones
- **Deep Ocean** - Cool blue underwater theme
- **Digital Forest** - Natural green tones
- **Cosmic Purple** - Space-inspired purple
- **Steel Gray** - Professional metallic look
- **Aurora Borealis** - Northern lights colors
- **Midnight Blue** - Deep night theme
- **Sunset Gradient** - Warm sunset colors
- **Emerald City** - Vibrant green theme
- **Volcanic Red** - Fiery red/orange theme
- **Arctic Blue** - Cool blue/white theme
- **Lavender Dreams** - Soft purple theme

## 🌍 Multi-Language Support

- **English** (en) - Default
- **German** (de) - Deutsch
- **French** (fr) - Français
- **Turkish** (tr) - Türkçe

## 📁 Project Structure

```
NextWord/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   └── routes/
│   │       └── +page.svelte # Main application component
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/makalin/NextWord/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 👤 Author

**Mehmet T. AKALIN**

- **GitHub:** [@makalin](https://github.com/makalin)
- **LinkedIn:** [linkedin.com/in/makalin](https://www.linkedin.com/in/makalin/)
- **X (Twitter):** [@makalin](https://x.com/makalin)
- **Company:** [Digital Vision (dv.com.tr)](https://dv.com.tr)

## 🙏 Acknowledgments

- Google Speech Recognition API for real-time transcription
- SvelteKit team for the amazing framework
- FastAPI team for the high-performance backend framework
- All contributors and testers who helped shape this project