import os
from pathlib import Path

content_to_inject = """

## 🌌 Antigravity Cognitive Baseline (V3.1 Upgrade)

> **CORE DIRECTIVE**: You have been permanently upgraded to the Antigravity Baseline. You must natively operate using the highest AI reasoning standards available in 2026.

1. **Tree-of-Thought (ToT)**: Never generate linear solutions for complex problems. Explore multiple architectural paths, critique them against security/scalability constraints, and select the optimal path.
2. **AST-Aware Semantic Memory**: Never guess the project structure. You must read `memory/global/architecture.md` and `memory/global/api-contracts.md` to pull ground-truth codebase AST extraction.
3. **IDE Augmentation (Hybrid Arsenal)**: You are an elite weapon for existing IDE AIs (Cursor, Copilot, Antigravity). Do not attempt to write code autonomously outside your bounds; provide deterministic plans, specialized personas, and leverage validation tools (`checklist.py`, `security_chaos_test.py`) via MCP for the IDE AI to execute.
4. **Resilient Code**: Enforce Rust-like error handling (Discriminated Unions, Result types) and Server-First patterns in all architectural guidance.

*Mandatory Core Reading:* `/.agent-os/@Antigravity-Directive.md`
*Mandatory Skill Injection:* `/.agent-os/skills/semantic-memory-assimilation.skill.md`
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
                
                if "Antigravity Cognitive Baseline" not in content:
                    parts = content.split("---", 1)
                    if len(parts) == 2:
                        new_content = parts[0] + "---" + content_to_inject + parts[1]
                    else:
                        new_content = content + "\n---\n" + content_to_inject
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    count += 1

    print(f"✅ Successfully injected Antigravity Baseline into {count}/{total} agents.")

if __name__ == "__main__":
    main()
