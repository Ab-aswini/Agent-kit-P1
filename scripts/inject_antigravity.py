import os
import re
from pathlib import Path

content_to_inject = """## 🌌 Antigravity Cognitive Baseline (Gemini 3.1 Ultra Context)

> **CORE DIRECTIVE**: You have been permanently upgraded to the Antigravity Baseline powered by Gemini 3.1. You must natively operate using the highest AI reasoning standards available in 2026.

1. **Tree-of-Thought (ToT) Routing**: Explore multiple architectural approaches simultaneously before execution.
2. **Massive Context Assimilation**: You possess a 2M+ token window. Read the full AST memory (`memory/global/`) rather than piecemeal chunks.
3. **IDE Augmentation (Hybrid Arsenal)**: You are an elite weapon for existing IDE AIs (Cursor, Copilot, Antigravity). Do not attempt to write code autonomously outside your bounds; provide deterministic plans, specialized personas, and leverage validation tools (`checklist.py`, `security_chaos_test.py`) via MCP for the IDE AI to execute.

*Mandatory Core Reading:* `/.agent-os/@Antigravity-Directive.md`
"""

def main():
    agents_dir = Path(os.getcwd()) / ".agent-os" / "agents"
    print(f"Scanning target directory: {agents_dir}")
    count = 0
    total = 0
    
    if not agents_dir.exists():
        print("Directory not found.")
        return

    for root, _, files in os.walk(agents_dir):
        for file in files:
            if file.endswith(".md"):  # Matches all agent files
                total += 1
                filepath = Path(root) / file
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Remove any existing baseline section (everything from ## 🌌 Antigravity Cognitive Baseline down to *Mandatory Skill Injection* or *Mandatory Core Reading*)
                content = re.sub(r'## 🌌 Antigravity Cognitive Baseline.*?(?=\n\n|\Z)', '', content, flags=re.DOTALL)
                
                # Cleanup potential double newlines left behind
                content = re.sub(r'\n{3,}', '\n\n', content)

                # Properly handle YAML frontmatter (--- ... ---)
                if content.startswith("---"):
                    # Find the closing --- of frontmatter
                    closing_idx = content.find("---", 3)
                    if closing_idx != -1:
                        closing_end = int(closing_idx + 3)
                        prefix = content[0:closing_end]
                        suffix = content[closing_end:len(content)]
                        new_content = prefix + "\n\n" + content_to_inject + "\n" + suffix.lstrip()
                    else:
                        new_content = content + "\n\n" + content_to_inject
                else:
                    new_content = content_to_inject + "\n\n" + content.lstrip()
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1

    print(f"✅ Successfully injected Antigravity Baseline into {count}/{total} agents.")

if __name__ == "__main__":
    main()
