import os
import sys

def setup_hub():
    print("🚀 Initializing Agent-Kit Framework...")
    
    # Create required directories if missing
    dirs = [
        "memory/product",
        "memory/backend",
        "memory/frontend",
        "docs/prd",
        "docs/architecture",
        "src/components",
        "src/api",
    ]
    
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"Created: {d}")
        else:
            print(f"Exists: {d}")
            
    # Create basic memory files if missing
    memory_files = {
        "memory/global/architecture.md": "# Global Architecture\n\n- Tech Stack: \n- Architecture Pattern: \n- Deployment: \n",
        "memory/frontend/design-system.md": "# Design System\n\n- Colors: \n- Typography: \n- Components: \n",
    }
    
    for path, content in memory_files.items():
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            print(f"Created: {path}")
            
    print("\n✅ Agent-Kit Setup Complete!")
    print("Suggestions: Run 'api-architect' or 'ui-architect' to begin development.")

if __name__ == "__main__":
    setup_hub()
