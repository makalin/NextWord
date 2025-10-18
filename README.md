# NextWord

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![GitHub stars](https://img.shields.io/github/stars/makalin/NextWord?style=social)
![GitHub forks](https://img.shields.io/github/forks/makalin/NextWord?style=social)

NextWord is a real-time AI-powered cue suggestion app designed to act as your cognitive partner. It listens as you speak and provides intelligent suggestions to keep your thoughts flowing, helping you articulate ideas, recall missed points, and discover new connections on the fly.

## The Problem

Have you ever been in the middle of a presentation, a brainstorming session, or even just thinking out loud, and you suddenly...
* Lose your train of thought?
* Struggle to find the perfect word?
* Forget a key point you meant to cover?
* Feel you're missing a connection to another topic?

NextWord is being built to solve exactly this.

## Key Features

* **Real-Time Voice Transcription:** Instantly captures your spoken words as you utter them.
* **AI-Powered Cue Suggestions:** Analyzes the live context and provides word/phrase suggestions in milliseconds.
* **Topic Recall & Reminders:** Intelligently identifies related concepts or sub-topics you may have missed, prompting you to explore them.
* **Contextual Word Finder:** Helps you find that specific word that's "on the tip of your tongue."
* **Session Recording:** Save your thought-streams for later review.

## 🚀 Future Vision: The Interactive Mind Map

The ultimate goal for NextWord is to evolve beyond simple cues into a fully interactive **AI-powered mind-mapping tool**.

Imagine this: As you speak, NextWord not only transcribes your voice but also **automatically generates a visual mind map** of your ideas in real-time. This will allow you to:
* **See** the structure of your thoughts as they form.
* **Interact** with nodes on the map to dive deeper.
* **Visually identify** gaps in your logic or areas for expansion.
* **Create** a dynamic, living document of your brainstorming or speech, built entirely from your voice.

## ⚡ Core Architecture (Optimized for Speed)

This app's success depends on low latency. The architecture is designed around a continuous, real-time stream of data.

1.  **Client (Web/Mobile):** Uses the `MediaRecorder` API to capture audio.
2.  **WebSocket (Client -> Backend):** Audio is chunked and streamed to the backend over a persistent WebSocket connection.
3.  **Backend (FastAPI):**
    * Receives the audio chunk.
    * Forwards this chunk to the **Real-time STT API** (e.g., Deepgram) over *its own* WebSocket.
    * Receives *interim* (partial) transcripts back from the STT service.
4.  **AI Suggestion (Backend):**
    * As interim transcripts arrive, the backend sends them to a high-speed **LLM** (e.g., Claude 3 Haiku, Gemini 1.5 Flash).
    * The LLM is prompted to "predict the next word" or "suggest a related topic" based on the partial context.
5.  **WebSocket (Backend -> Client):** The AI-generated suggestion is immediately pushed back down the *original* WebSocket to the client UI.

This entire loop must complete in **sub-second time** to feel "real-time."

## 🛠 Recommended Tech Stack (Optimized for Speed)

This stack is chosen for maximum performance (low latency) and development velocity.

* **Frontend:** **SvelteKit** or **Next.js (React)**
    * *Rationale:* SvelteKit for rapid development and high runtime performance. Next.js for its massive ecosystem, especially for the future mind-mapping feature (e.g., `react-flow`).

* **Backend:** **Python (FastAPI)**
    * *Rationale:* Built for high-performance, async I/O and native WebSocket support. Perfect for managing simultaneous STT and LLM API calls.

* **Real-time STT:** **Deepgram** or **AssemblyAI**
    * *Rationale:* Essential for streaming transcription. These services provide sub-second transcripts from audio streams, which is a hard requirement.

* **AI Suggestions (LLM):** **Anthropic Claude 3 Haiku**, **Google Gemini 1.5 Flash**, or **OpenAI GPT-4o**
    * *Rationale:* Optimized for low-latency, "agent-like" responses. Speed is more important than massive context, and these models are the fastest on the market.

* **Real-time Communication:** **WebSockets**
    * *Rationale:* The only choice for persistent, bi-directional, low-latency communication between the client and server.

* **Databases:**
    * **Redis:** For caching interim transcripts and session data.
    * **PostgreSQL:** For storing user accounts and saved sessions/mind maps.

## 🏁 Getting Started

*(This section will be updated as the project develops.)*

### Prerequisites

* API keys for Deepgram/AssemblyAI and your chosen LLM.
* Redis server
* PostgreSQL server

### Installation

1.  Clone the repo:
    ```sh
    git clone [https://github.com/makalin/NextWord.git](https://github.com/makalin/NextWord.git)
    ```
2.  Navigate to the project directory:
    ```sh
    cd NextWord
    ```
3.  Install backend dependencies:
    ```sh
    # (Example for Python)
    cd backend
    pip install -r requirements.txt
    ```
4.  Install frontend dependencies:
    ```sh
    # (Example for Node.js)
    cd frontend
    npm install
    ```

### Running the App

```sh
# (Add commands to run the backend and frontend servers)
````

## 🤝 Contributing

Contributions, issues, and feature requests are welcome\! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/makalin/NextWord/issues).

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## 👤 Author

**Mehmet T. AKALIN**

  * **GitHub:** [@makalin](https://github.com/makalin)
  * **LinkedIn:** [linkedin.com/in/makalin](https://www.linkedin.com/in/makalin/)
  * **X (Twitter):** [@makalin](https://x.com/makalin)
  * **Company:** [Digital Vision (dv.com.tr)](https://dv.com.tr)
