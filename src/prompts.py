TASKS = {
    "Study notes": "Create structured, exam-friendly study notes with headings, key terms, explanations, examples and a concise recap.",
    "PDF summary": "Summarize the supplied source accurately. Include an executive summary, section-wise summary, key facts and glossary.",
    "Revision sheet": "Create a compact last-minute revision sheet with definitions, formulas where present, important facts and memory cues.",
    "Flashcards": "Create question-and-answer flashcards from the source. Use one concept per card.",
    "Quiz": "Create a quiz from the source with a mix of multiple-choice and short-answer questions. Put the answer key at the end.",
    "Question paper": "Create a balanced question paper from the source. Include sections, marks, difficulty mix and a separate answer key.",
    "Answers": "Answer the supplied questions using only the source where possible. Show concise reasoning and flag anything not supported by the source.",
    "Slide outline": "Turn the source into a slide-by-slide presentation outline with slide titles and concise bullet points.",
    "Flowchart (Mermaid)": "Convert the source process or concepts into a Mermaid flowchart. Output only valid Mermaid code inside a mermaid code fence, followed by a short explanation.",
    "Explain simply": "Explain the source in beginner-friendly language, using analogies and examples without changing its meaning.",
}

def build_prompt(task: str, source: str, extra: str = "") -> str:
    instruction = TASKS[task]
    return f"""{instruction}

User preferences: {extra or "No additional preferences."}

SOURCE MATERIAL:
{source[:45000]}

Important: Do not invent facts. If the source is incomplete or unclear, say so.
"""
