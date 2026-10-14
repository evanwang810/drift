import ast

with open('agent/tools.py', 'r') as f:
    content = f.read()

tree = ast.parse(content)

# Count all functions (both private and public)
all_functions = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
print(f"Total functions: {len(all_functions)}")

# Count unique function names
unique_names = set(f.name for f in all_functions)
print(f"Unique function names: {len(unique_names)}")

# Count private tools (starting with _)
private_tools = [f.name for f in all_functions if f.name.startswith('_')]
print(f"Private tools: {len(private_tools)}")

# Count public tools (not starting with _)
public_tools = [f.name for f in all_functions if not f.name.startswith('_')]
print(f"Public tools: {len(public_tools)}")

# Show all public tool names
print("\nPublic tools:")
for name in sorted(public_tools):
    print(f"  {name}")
