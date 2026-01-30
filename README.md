# 🎙️ Talk2Task

**Talk2Task** is a real-time **AI-powered meeting intelligence platform** that transforms conversations into **clear actions, insights, and presentations**.

It enables smart meetings with:
- 🎧 Live speech-to-text captions
- 🧠 AI-generated summaries, MoM, flowcharts, and PPT outlines
- 📊 One-click presentation generation (PDF / PPTX)
- 💬 AI assistant for participants
- 🎥 Live video conferencing via LiveKit

Built for **teams, remote collaboration, and AI-first productivity**.

---

## 🚀 Features

### 🔊 Real-time Meetings
- Live video & audio using **LiveKit**
- Role-based access: **Host** & **Participants**
- Secure token-based room joining

### 🎤 Live Captions (Speech-to-Text)
- Real-time STT via WebSockets
- Supported languages:
  - English
  - Hindi
  - Hinglish
- Host-controlled recording
- Participants see live captions & recording indicator

### 🧠 AI Meeting Intelligence
Powered by **OpenAI / Gemini**:
- ✅ Meeting Summary
- ✅ Minutes of Meeting (MoM)
- ✅ Flowchart generation
- ✅ PPT outline generation

### 📊 AI Presentation Generator
- Converts meeting transcripts into structured slides
- Uses **Presenton.ai API**
- Download formats:
  - PPTX
  - PDF
- Preview before download

### 💬 AI Assistant (Participants)
- Ask questions about the meeting
- Uses full meeting context
- Conversational Q&A experience

### 📎 File Uploads (Host)
- Upload PDFs & images
- Extracted text is added to AI context
- Improves accuracy of summaries & presentations

---

## 🏗️ Tech Stack

### Frontend
- **Next.js 14 (App Router)**
- TypeScript
- Tailwind CSS
- LiveKit React SDK
- Axios

### Backend
- **FastAPI**
- WebSockets (Speech-to-Text)
- LiveKit Server SDK
- OpenAI / Gemini
- Presenton.ai API
- Python 3.10+

---

## 📁 Project Structure

### Backend (`/backend`)
