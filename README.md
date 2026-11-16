# StudyFlow AI — Streamlit Study Helper

A clean, modular Streamlit starter app that turns learning material into study resources.

## Included in this MVP
- PDF, DOCX, PPTX, TXT, Markdown and CSV text extraction
- YouTube caption/transcript import when captions are available
- AI study notes, summaries, revision sheets, flashcards and simple explanations
- Quiz, question-paper and answer-key generation
- Slide outline and Mermaid flowchart generation
- Download generated resources as Markdown
- Voice-notes and rendered AI-video provider integration placeholders
- Session-based study library

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your AI API key.
5. Start the app:

   ```bash
   streamlit run app.py
   ```

## Configuration

- `AI_API_KEY`: required for AI generation.
- `AI_MODEL`: model name supported by your provider.
- `AI_BASE_URL`: optional base URL for an OpenAI-compatible API.

Never commit `.env` or expose your API key in client-side code.

## Important limitations
- PDF extraction reads selectable text. Scanned/image-only PDFs need OCR integration.
- YouTube import reads accessible captions only; some videos have no available transcript.
- Voice-note transcription needs a speech-to-text provider adapter.
- AI video generation needs a video-generation provider and is not rendered by this MVP.
- Generated outputs are held in Streamlit session state; persistent accounts, database storage and cloud deployment are future work.

See `SPEC.md` for the full product specification and roadmap.
