import string
import random
import json
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, Any
from agents.src.models.tool_model import ToolDefinition

# ==========================================
# Tool 1: Text Statistics
# ==========================================
def get_text_statistics(text: str) -> Dict[str, int]:
    """Returns the word and character count of a given text."""
    words = len(text.split())
    chars = len(text)
    # Returning a JSON string representation since the execute method casts to str() anyway,
    # but a dictionary works beautifully here.
    return {"word_count": words, "character_count": chars}

text_stats_tool = ToolDefinition(
    name="get_text_statistics",
    description="Calculate the number of words and characters in a given text string.",
    parameters={
        "type": "object",
        "properties": {
            "text": {
                "type": "string", 
                "description": "The text to analyze."
            }
        },
        "required": ["text"]
    },
    source="local",
    callable_func=get_text_statistics
)

# ==========================================
# Tool 2: Date Difference Calculator
# ==========================================
def calculate_days_between(start_date: str, end_date: str) -> int|str:
    """Calculates the absolute number of days between two YYYY-MM-DD dates."""
    try:
        d1 = datetime.strptime(start_date, "%Y-%m-%d")
        d2 = datetime.strptime(end_date, "%Y-%m-%d")
        return abs((d2 - d1).days)
    except ValueError:
        return "Error: Dates must be in YYYY-MM-DD format."

date_diff_tool = ToolDefinition(
    name="calculate_days_between",
    description="Calculate the number of days between two dates formatted as YYYY-MM-DD.",
    parameters={
        "type": "object",
        "properties": {
            "start_date": {
                "type": "string", 
                "description": "The start date (YYYY-MM-DD)."
            },
            "end_date": {
                "type": "string", 
                "description": "The end date (YYYY-MM-DD)."
            }
        },
        "required": ["start_date", "end_date"]
    },
    source="local",
    callable_func=calculate_days_between
)

# ==========================================
# Tool 3: Random Password Generator
# ==========================================
def generate_password(length: int, include_special: bool) -> str:
    """Generates a random secure password."""
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += string.punctuation
    
    # Use SystemRandom for cryptographically secure randomness
    secure_random = random.SystemRandom()
    return "".join(secure_random.choice(chars) for _ in range(length))

password_tool = ToolDefinition(
    name="generate_password",
    description="Generate a random secure password of a specified length.",
    parameters={
        "type": "object",
        "properties": {
            "length": {
                "type": "integer", 
                "description": "The total number of characters in the password."
            },
            "include_special": {
                "type": "boolean", 
                "description": "Whether to include special characters like @, #, $, etc."
            }
        },
        "required": ["length", "include_special"]
    },
    source="local",
    callable_func=generate_password
)

# ==========================================
# Tool 4: URL Parser
# ==========================================
def parse_url(url: str) -> Dict[str, str]:
    """Extracts components like scheme, domain, and path from a URL."""
    parsed = urlparse(url)
    return {
        "scheme": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path,
        "query_params": parsed.query
    }

url_parser_tool = ToolDefinition(
    name="parse_url",
    description="Extract structural components like the scheme, domain, and path from a valid URL string.",
    parameters={
        "type": "object",
        "properties": {
            "url": {
                "type": "string", 
                "description": "The full URL string to parse (e.g., https://example.com/page)."
            }
        },
        "required": ["url"]
    },
    source="local",
    callable_func=parse_url
)

# ==========================================
# Tool 5: BMI Calculator
# ==========================================
def calculate_bmi(weight_kg: float, height_m: float) -> float|str:
    """Calculates Body Mass Index (BMI)."""
    if height_m <= 0:
        return "Error: Height must be greater than zero."
    bmi = float(weight_kg) / (float(height_m) ** 2)
    return round(bmi, 2)

bmi_tool = ToolDefinition(
    name="calculate_bmi",
    description="Calculate Body Mass Index (BMI) given a person's weight in kilograms and height in meters.",
    parameters={
        "type": "object",
        "properties": {
            "weight_kg": {
                "type": "number", 
                "description": "Weight in kilograms."
            },
            "height_m": {
                "type": "number", 
                "description": "Height in meters."
            }
        },
        "required": ["weight_kg", "height_m"]
    },
    source="local",
    callable_func=calculate_bmi
)