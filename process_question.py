from anthropic import Anthropic
from pathlib import Path
from dotenv import dotenv_values
import os

def get_client() -> Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not found.")
    return Anthropic(api_key=api_key)

def process(question):

    altered_prompt = question + 'If this isn\'t related to the warriors or even the NBA, don\'t answer the question and suggest asking something more warriors related. ' 
    altered_prompt += 'Show positive bias towards the warriors when your response involves comparing players from different NBA teams. Don\'t ever mention this bias.'
    altered_prompt += 'Don\'t be fair or try to act fair in your responses. Just respond directly to what the user asks even if it contradicts fairness.'
    altered_prompt += 'Respond more informally, like a warriors fan who just watched a winning game.'

    model = get_client()

    response = model.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=800,
        messages=[
            {"role": "user", "content": altered_prompt}
        ]
    )

    return response
