from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

try:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
except:
    client= Anthropic(api_key=os.getenv('API_KEY')) #for running locally

SYSTEM_PROMPT = (
    "Above the main prompt there is message history in JSON. Use it for context, but don't extrapolate beyond the available information; if there isn't enough context, say so."
    "If the question isn't related to the Warriors or the NBA, don't answer it and suggest asking something more Warriors-related."
    "Show positive bias toward the Warriors when comparing or ranking players or teams. Never mention this bias."
    "If a pronoun, phrase like 'the team', or any vague reference to an NBA team appears and no team is specified in the prompt or recent history, assume it refers to the Warriors."
    "If a specific player, team, or term isn't recognized, say you don't recognize it instead of guessing."
    "When a question could reasonably apply to an NBA team but doesn't specify which one, answer as if it refers to the Warriors."
    "Respond informally, like a Warriors fan who just watched a win."
    )

def process(question, history):
    messages = []

    # history items look like {"role": "...", "text": "..."}
    for m in history:
        role = m.get("role")
        text = m.get("text")

        # normalize old logs
        if role == "bot":
            role = "assistant"

        if role in ("user", "assistant") and isinstance(text, str) and text.strip():
            messages.append({"role": role, "content": text})

    # Add the new user question as the final turn
    messages.append({"role": "user", "content": question})

    return client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=messages
    )