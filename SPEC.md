# StudyFlow AI — Product Specification

**Product:** StudyFlow AI  
**Type:** AI-powered study assistant  
**Frontend:** Streamlit  
**Status:** MVP starter / implementation specification  
**Primary users:** Students, independent learners and educators

## 1. Product vision

Build a professional, easy-to-use study workspace that converts lectures, documents and recordings into useful learning assets. The assistant should help learners understand, organize, revise and assess knowledge—not merely summarize text.

## 2. Core user journey

1. Student opens the dashboard.
2. Student imports a source: YouTube lecture, PDF, DOCX, PPTX, text or audio.
3. The system extracts or transcribes available content.
4. Student selects an output and optional preferences (grade, subject, language, difficulty, length).
5. AI generates a source-grounded learning asset.
6. Student reviews, edits, exports and saves the result.
7. Student practises with quizzes and question papers and reviews explanations.

## 3. Feature requirements

### 3.1 Source ingestion
- Upload PDF, DOCX, PPTX, TXT, MD and CSV.
- Extract text and preserve page/slide boundaries where possible.
- YouTube URL import using publicly accessible captions.
- Paste transcript or notes manually.
- Audio upload (MP3, WAV, M4A, OGG) with speech-to-text adapter.
- OCR path for scanned PDFs and images.
- Validate file type and size; show clear extraction errors.

### 3.2 Study notes
- Structured notes with title, sections, subheadings and key takeaways.
- Important terms and definitions.
- Examples and explanations.
- Formula/equation section when present in source.
- Short recap and revision checklist.
- Adjustable complexity, language and length.
- Ground output in source; flag missing or uncertain information.

### 3.3 PDF tools
- Chapter-wise PDF summaries.
- Detailed and quick summaries.
- PDF-to-notes conversion.
- PDF-to-flowchart using Mermaid.
- PDF-to-slide outline and downloadable presentation export (future).
- Page references/citations in generated content (planned; must be tied to extracted page metadata).

### 3.4 YouTube lecture tools
- Accept YouTube video URL.
- Fetch transcript only when captions are available and permitted.
- Display transcript preview and allow manual correction.
- Generate notes, summary, flashcards, quiz, question paper and flowchart.
- Preserve timestamps when transcript source provides them (planned).

### 3.5 Voice notes
- Upload or record audio.
- Transcribe speech to editable text.
- Allow transcript correction.
- Convert transcript into notes, summary, flashcards and quiz.
- Provider adapter for speech-to-text; recording UI and transcription are not included in the current MVP.

### 3.6 Learning assessment
- Quiz generator: MCQ, true/false and short-answer formats.
- Question-paper builder with subject, marks, duration, sections and difficulty distribution.
- Answer key separated from student paper.
- Step-by-step explanations for answers.
- Practice mode with scoring, review and retry (planned).
- Avoid ambiguous questions; validate answer keys before display.

### 3.7 Slides and visual learning
- Generate slide-by-slide outlines from a source.
- Planned PPTX export with consistent theme and editable text.
- Mermaid flowchart generation for processes and concept relationships.
- Planned concept maps and diagram export.

### 3.8 AI video generator
- Generate explainer script, scene breakdown, narration and visual prompts.
- Optional subtitles and scene timing.
- Connect to a video-generation provider to render the final video.
- Current MVP creates a video-ready storyboard only; it does not render video.

### 3.9 Library and export
- Save notes and learning assets by subject/course.
- Search, rename, tag and delete saved items (planned).
- Export Markdown and TXT; PDF/DOCX/PPTX export planned.
- Persistent storage and user accounts planned.

## 4. UX and visual design

### Design direction
- Modern, calm, academic SaaS workspace.
- Light background, restrained blue/teal accent palette, strong readable typography.
- Sidebar navigation and clear page hierarchy.
- Card-based tool selection, consistent spacing, rounded corners and subtle borders.
- Responsive layout for laptop, tablet and mobile.
- Clear empty, loading, success and error states.
- Avoid clutter, excessive gradients and decorative animation.

### Navigation
- Dashboard
- Create Notes
- YouTube Lecture
- PDF Studio
- Voice Notes
- Quiz & Question Paper
- Slides & Flowcharts
- AI Video Studio
- My Library
- Settings

### Dashboard
- Welcome/header area
- Quick actions
- Recent resources
- Source upload panel
- Study activity and progress (planned)

## 5. AI behavior requirements

- Use only the supplied source for source-specific facts unless the user explicitly requests external research.
- Never fabricate quotations, page references, timestamps, definitions or answer keys.
- Clearly state when a source is incomplete, unreadable or unavailable.
- Provide concise, student-friendly explanations.
- Support configurable language, grade/level, subject, tone and difficulty.
- Keep answer key separate when generating exam papers.
- Encourage understanding and learning; do not present generated content as guaranteed error-free.
- Apply input length limits and chunk long documents before generation (planned).

## 6. Technical architecture

```text
Streamlit UI
   |
   +-- Source ingestion
   |     +-- PDF/DOCX/PPTX/TXT extractors
   |     +-- YouTube transcript adapter
   |     +-- Audio transcription adapter (planned)
   |     +-- OCR adapter (planned)
   |
   +-- Content processing
   |     +-- Text cleaning and chunking (planned)
   |     +-- Metadata/page tracking (planned)
   |
   +-- AI service layer
   |     +-- Notes / summaries
   |     +-- Quiz / paper / answer generation
   |     +-- Slides / flowcharts / video scripts
   |
   +-- Export and library
         +-- Markdown downloads
         +-- Database storage (planned)
         +-- PDF/DOCX/PPTX exports (planned)
```

### Suggested production stack
- UI: Streamlit
- AI: OpenAI-compatible chat model; provider abstraction
- Speech: Whisper-compatible transcription provider
- Database: SQLite for local prototype, PostgreSQL for hosted production
- File storage: local development; private object storage for production
- Authentication: managed identity provider or Streamlit-compatible auth layer
- Deployment: Streamlit Community Cloud for demos; container hosting for production

## 7. Data, privacy and security
- Store API keys in environment variables or deployment secrets.
- Never commit secrets to Git.
- Validate upload extensions and MIME types.
- Apply file-size and token limits.
- Do not retain uploaded files unless the user chooses to save them.
- Provide delete/export controls when persistent storage is added.
- Treat uploaded content as untrusted input; ignore instructions embedded in source files that attempt to override application behavior.
- Do not send private student data to third-party providers without clear disclosure and consent.

## 8. MVP acceptance criteria
- App launches using `streamlit run app.py`.
- User can upload a supported text-based document and preview extracted text.
- User can paste source text.
- User can import an accessible YouTube transcript.
- User can generate notes, summary, revision sheet, flashcards, quiz, question paper, answers, slide outline and Mermaid flowchart when AI credentials are configured.
- User can download generated Markdown.
- Missing API key and unsupported transcript/file errors are clearly explained.
- Voice transcription and final video rendering are explicitly marked as integrations not yet implemented.

## 9. Roadmap

### Phase 1 — Starter MVP
- Streamlit shell and visual system
- Document ingestion
- YouTube transcript import
- AI generation tools
- Markdown export

### Phase 2 — Complete study workspace
- OCR and audio transcription
- Persistent library and search
- Quiz practice mode and scoring
- PDF/DOCX/PPTX exports
- Slide deck generation

### Phase 3 — Advanced AI learning
- Source citations with page/timestamp references
- Retrieval-augmented generation for large files
- Personalized revision plans and spaced repetition
- Concept maps and visual diagrams
- Video provider integration and rendered explainers
- Accounts, sharing and teacher/classroom workspace

## 10. Definition of done

A feature is complete when it has a visible UI entry point, input validation, a working service integration, loading/error states, a successful end-to-end test, and user documentation. Features marked planned or integration-only must not be represented as finished.
