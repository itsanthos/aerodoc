# AeroDoc

Chatbot that answers aeronautics questions using only the provided documents
(FAA Pilot's Handbook of Aeronautical Knowledge) and cites its sources (file, page).
Answers in French or English. If the answer isn't in the documents, it says so.

## Tech
Python, Gemini API, pypdf, object-oriented design

## Run it
1. `pip install -r requirements.txt`
2. Create a `.env` file with `GEMINI_API_KEY=your-key`
3. Put PDFs in `docs/`
4. `python chat.py`

## Next steps
- Real RAG with embeddings and vector search for large manuals
- Retry with backoff for API errors
- FastAPI + Docker
