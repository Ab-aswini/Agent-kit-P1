import os
import shutil
import re

def migrate_skills():
    skills_dir = '.agent-os/skills'
    agents_dir = '.agent-os/agents'
    
    # 1. Identify and migrate .skill.md files
    migrated_skills = {} # {old_filename: new_path}
    
    for file in os.listdir(skills_dir):
        if file.endswith('.skill.md'):
            skill_name = file.replace('.skill.md', '')
            old_path = os.path.join(skills_dir, file)
            new_dir = os.path.join(skills_dir, skill_name)
            new_file_path = os.path.join(new_dir, 'SKILL.md')
            
            os.makedirs(new_dir, exist_ok=True)
            
            # If sub-SKILL.md doesn't exist or is smaller, move it
            if not os.path.exists(new_file_path) or os.path.getsize(old_path) > os.path.getsize(new_file_path):
                shutil.copy2(old_path, new_file_path)
                print(f"Migrated: {file} -> {skill_name}/SKILL.md")
            
            migrated_skills[file] = f"{skill_name}/SKILL.md"
            # os.remove(old_path) # Clean up later

    # 2. Update all agent files
    for root, dirs, files in os.walk(agents_dir):
        for file in files:
            if file.endswith('.agent.md') or file.endswith('.md'):
                agent_path = os.path.join(root, file)
                try:
                    with open(agent_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    for old_file, new_suffix in migrated_skills.items():
                        # Replace .agent-os/skills/auth.skill.md with .agent-os/skills/auth/SKILL.md
                        old_ref = f".agent-os/skills/{old_file}"
                        new_ref = f".agent-os/skills/{new_suffix}"
                        new_content = new_content.replace(old_ref, new_ref)
                        
                        # Also handle short refs if any (e.g. auth.skill.md)
                        new_content = new_content.replace(old_file, f"{skill_name}/SKILL.md") # Note: skill_name logic here needs to be careful
                    
                    # Refined replacement for skill names
                    for old_file, new_suffix in migrated_skills.items():
                         pattern = re.compile(re.escape(old_file))
                         new_content = pattern.sub(new_suffix, new_content)

                    if new_content != content:
                        with open(agent_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated Agent: {agent_path}")
                except Exception as e:
                    print(f"Error updating agent {agent_path}: {e}")

    # 3. Cleanup
    for old_file in migrated_skills.keys():
        old_path = os.path.join(skills_dir, old_file)
        if os.path.exists(old_path):
            os.remove(old_path)
            print(f"Removed legacy: {old_file}")

if __name__ == "__main__":
    migrate_skills()
