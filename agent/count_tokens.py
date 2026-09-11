"""Count tokens in the system prompt, waking message, and tool schema."""
import json
import inspect
from pathlib import Path
from tokenizers import Tokenizer

# Load the tokenizer (using tiktoken or a simple space tokenization for estimation)
def count_tokens(text: str) -> int:
    """Estimate token count using a simple space-splitting heuristic (rough but works)."""
    return len(text.split())

# Read the system prompt
prompt_path = Path("agent/prompt.md")
system_prompt = prompt_path.read_text(encoding="utf-8")

# Read the waking message
from agent import context
from datetime import datetime

root = Path.cwd()
waking_message = context.waking(
    root, run=95, days=1, last="out_of_turns",
    now=datetime.now(), turns=40
)

# Get the tool schema
from agent import tools
tool_schema = tools.schema()

print("Token counts:")
print("=" * 50)
print(f"System prompt: {count_tokens(system_prompt)} tokens")
print(f"Waking message: {count_tokens(waking_message)} tokens")
print(f"Tool schema: {len(tool_schema)} tools")
schema_tokens = sum(count_tokens(json.dumps(tool, indent=2)) for tool in tool_schema)
print(f"Tool schema total: {schema_tokens} tokens")
print()
print(f"Total sent on first turn: {count_tokens(system_prompt) + count_tokens(waking_message) + schema_tokens} tokens")
print()
print("Full waking message:")
print("-" * 50)
print(waking_message)
