def build_base_context(room_name: str, merged_transcript: str) -> str:
    return f"""
You are an AI meeting intelligence assistant.

Meeting ID: {room_name}

Below is a full transcript of a meeting.
The transcript is accurate and ordered by time.

Transcript:
{merged_transcript}
"""


def build_summary_prompt(context: str) -> str:
    return context + """
TASK:
Generate a concise professional summary of this meeting.
Focus on:
- Purpose
- Key discussion points
- Outcomes
"""


def build_mom_prompt(context: str) -> str:
    return context + """
TASK:
Generate detailed Minutes of Meeting (MoM) with:
- Attendees (infer from speakers)
- Agenda
- Key decisions
- Action items (with owner & priority)
- Open questions
"""


def build_ppt_prompt(context: str) -> str:
    return context + """
TASK:
Create a PowerPoint outline with:
- Slide titles
- Bullet points per slide
- Logical flow from problem → solution → execution
"""


def build_flowchart_prompt(context: str) -> str:
    return context + """
TASK:
Create a flowchart structure.
Return the flow in text form like:

Start → Step A → Decision? → Yes → Step B → End

Keep it clear and structured.
"""
