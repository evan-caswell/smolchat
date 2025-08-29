import json
from typing import Any
from settings import get_settings

API_BASE_URL = get_settings().API_BASE_URL
MODEL_ID: str = get_settings().MODEL_ID
MODEL_NAME = MODEL_ID.lstrip("ai/").split(":")[0]

DV: dict[str, Any] = {
    "seed": 0,
    "temperature": 0.8,
    "max_tokens": 512,
    "top_p": 0.95,
    "presence_penalty": 0.0,
    "frequency_penalty": 0.0,
    "stop": "",
    "n": 1,
    "stream": False,
    "top_k": 40,
    "min_p": 0.05,
    "typical_p": 1.0,
    "tfs_z": 1.0,
    "repeat_penalty": 1.0,
    "repeat_last_n": 64,
    "mirostat_mode": 0,
    "mirostat_tau": 5.0,
    "mirostat_eta": 0.1,
}

RECIPE_MD = """## Recipe
Generates recipe ingredients in JSON format\n
Prompt: `Give me a recipe for Texas style chili.`\n
Output:
"""

RECIPE_EXAMPLE = json.loads(
    """{
"recipe_name": "Texas Style Chili",
"ingredients": [
"1 can (14.5 oz) diced tomatoes",
"1 medium onion, diced",
"1 can (15 oz) kidney or Spanish beans, drained and rinsed",
"2 tablespoons chili powder",
"2 teaspoons ground cumin",
"1 teaspoon salt",
"2 teaspoons ground black pepper",
"1 cup beef broth",
"1 cup diced green chilies",
"2 cups shredded cheddar cheese"
]
}"""
)

EVENT_MD = """## Event
Extracts an event from a prompt\n
Prompt: `Everyone is excited for John's birthday. Joe and Sally are bringing desserts, and Mary is bringing a casserole. It's hard to believe he was born 18 years ago—September 8th will always be a special day.`\n
Output:
"""

EVENT_EXAMPLE = json.loads(
    """{
"event_name": "John's Birthday",
"event_date": "September 8th",
"participants": [
"Joe",
"Sally",
"Mary"
  ]
}"""
)

TIPS_MD = """### Tips
 - SmolLM2 has a tendency to get stuck in a loop that repeats the same words or phrases. If you get the error 'Invalid structured JSON' try a higher 'frequency penalty'
"""