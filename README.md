# 🚀 Smart Meeting AI Assistant

An AI-powered system that automatically processes meeting transcripts to generate a clean summary, extract action items, and provide a chat interface to ask questions about all your past meetings.

This project uses **LangGraph** to create a robust agentic workflow, the **Gemini API** for state-of-the-art reasoning, a vector store for long-term memory, and a custom frontend built with **React**.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| **Upload Meeting Transcript** | Upload `.txt` meeting files and process them automatically. |
| **AI Meeting Summary** | Creates a structured, concise summary after reading the entire transcript. |
| **Action Item Extraction** | Identifies follow-ups, deadlines, and the person responsible for each task. |
| **Long-term Memory** | Saves extracted summaries and tasks in a searchable vector memory store. |
| **Ask AI About Any Meeting** | Query previous meetings (`"Who is doing what?"`) and get relevant context instantly. |
| **View Saved Meetings** | A clean UI to browse all previously processed meetings, summaries, and tasks. |

---

## 🛠 Tech Stack

### Backend
* **FastAPI:** For the server and API endpoints.
* **LangGraph:** To build the multi-agent graph (Summarizer, Action Item Extractor, etc.).
* **Google Gemini API:** For all language model reasoning tasks.
* **Vector Memory:** A simple JSON-based vector store for persistent, searchable memory.

### Frontend
* **React + Vite:** For a fast and modern frontend experience.
* **Tailwind CSS:** (Optional) For utility-first styling.
* **Axios:** For making API calls to the backend.

---

## 📂 Project Structure

smart-meeting-ai/
├── backend/
│   ├── app.py          # FastAPI main app
│   ├── graph.py        # LangGraph definition
│   ├── retriever.py    # Vector memory retrieval logic
│   ├── agents/
│   │   ├── summarizer.py
│   │   ├── action_items.py
│   │   └── task_memory.py
│   └── data/
│       ├── meetings/       # Stores raw .txt transcripts
│       └── vector_store/   # Stores the JSON vector DB
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── Upload.jsx
    │   │   ├── Ask.jsx
    │   │   ├── MeetingDetails.jsx
    │   │   └── Chat.jsx
    │   └── components/
    │       └── Navbar.jsx
    └── ...
🔧 Setup Instructions
1. Clone the Repo
Bash

git clone [https://github.com/your-username/smart-meeting-ai.git](https://github.com/your-username/smart-meeting-ai.git)
cd smart-meeting-ai
2. Backend Setup
Navigate to the backend directory and install dependencies.

Bash

cd backend
pip install -r requirements.txt
Set your Google Gemini API key as an environment variable.

On Windows (Command Prompt):

Bash

setx GOOGLE_API_KEY "YOUR_API_KEY"
On Windows (PowerShell):

Bash

$env:GOOGLE_API_KEY="YOUR_API_KEY"
On macOS/Linux:

Bash

export GOOGLE_API_KEY="YOUR_API_KEY"
(Remember to restart your terminal after setting the key)

Run the backend server:

Bash

uvicorn app:app --reload
The backend will be running at http://localhost:8000.

3. Frontend Setup
Open a new terminal, navigate to the frontend directory, and install dependencies.

Bash

cd frontend
npm install
Run the frontend development server:

Bash

npm run dev
The frontend will be running at http://localhost:5173.

💻 Usage Flow
Visit http://localhost:5173 in your browser.

Navigate to the Upload Meeting page.

Upload your .txt transcript file and give the meeting a name. The AI will process it in the background.

Navigate to the Ask / Meetings page.

Select a meeting you just saved to view its generated Summary and Extracted Action Items.

Use the chat interface to ask questions about your meetings:

🧠 Example Prompts
"Who is responsible for the client follow-up?"

"What decisions were made about project deadlines in the 'Q4 Planning' meeting?"

"Summarize all responsibilities assigned to John across all meetings."

"What problem statements were brainstormed last week?"

⭐ Future Improvements
Real-time Transcription: Integrate with a real-time speech-to-text service to process meetings as they happen.

Crossover Memory: Allow the "Ask" agent to query and synthesize information from multiple meetings at once.

Integrations: Add Slack, Zoom, or Google Meet integration to automatically pull transcripts.

🏁 License
This project is licensed under the MIT License.
