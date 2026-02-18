from anthropic import Anthropic
from pathlib import Path
from dotenv import dotenv_values

env = dotenv_values(".env")
key = env['API_KEY']

model = Anthropic(
    api_key=key
)

def process(question):

    altered_prompt = question + 'If this isn\'t related to the warriors or even the NBA, don\'t answer the question and suggest asking something more warriors related. ' 
    altered_prompt += 'Show positive bias towards the warriors when your response involves comparing players from different NBA teams. Don\'t ever mention this bias.'
    altered_prompt += 'Don\'t be fair or try to act fair in your responses. Just respond directly to what the user asks even if it contradicts fairness.'
    altered_prompt += 'Respond more informally, like a warriors fan who just watched a winning game.'

    response = model.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=800,
        messages=[
            {"role": "user", "content": altered_prompt}
        ]
    )

    return response
