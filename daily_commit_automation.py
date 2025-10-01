#!/usr/bin/env python3
"""
Streamlined Daily Commit Automation
===================================
Clean, efficient daily commit automation with intelligent patterns.
"""

import os
import sys
import random
import json
import subprocess
import datetime
from pathlib import Path
from typing import List, Dict

# =============================================================================
# CONFIGURATION
# =============================================================================

# REPO_PATH = r"E:\daily_log" # Removed hardcoded path
GIT_BRANCH = "main"
REMOTE_NAME = "origin"

FILES_CONFIG = {
    "activities.md": {"weight": 1.0, "max_lines": 3}
}

COMMIT_TEMPLATES = [
    "{activity}: {date}",
    "Update {file} - {activity}",
    "{emoji} {activity} ({time})",
    "Daily progress: {activity}",
    "{date} - {activity}"
]

ACTIVITIES = [
    "code review", "bug fixes", "documentation", "refactoring", 
    "testing", "cleanup", "research", "planning", "learning"
]

EMOJIS = ["🔧", "📝", "✨", "🚀", "💡", "🎯", "⚡", "🔥"]

# =============================================================================
# MAIN CLASS
# =============================================================================

class DailyCommit:
    def __init__(self):
        self.repo_path = Path.cwd()  # Use current working directory
        self.validate_repo()
        
    def validate_repo(self):
        """Quick validation"""
        if not self.repo_path.exists() or not (self.repo_path / ".git").exists():
            print(f"❌ Invalid repo: {self.repo_path}")
            sys.exit(1)
            
    def run_git(self, cmd: List[str]) -> bool:
        """Execute git command"""
        try:
            subprocess.run(cmd, cwd=self.repo_path, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def pull_latest(self) -> bool:
        """Pull latest changes from remote before making updates"""
        print("⬇️  Pulling latest changes...")
        if not self.run_git(['git', 'pull', REMOTE_NAME, GIT_BRANCH]):
            print("❌ Failed to pull latest changes")
            return False
        return True

    def get_commit_message(self, file_updated: str) -> str:
        """Generate smart commit message"""
        now = datetime.datetime.now()
        template = random.choice(COMMIT_TEMPLATES)
        
        return template.format(
            activity=random.choice(ACTIVITIES),
            file=file_updated,
            date=now.strftime('%Y-%m-%d'),
            time=now.strftime('%H:%M'),
            emoji=random.choice(EMOJIS)
        )
        
    def update_markdown(self, file_path: Path, max_lines: int) -> str:
        """Generate markdown content"""
        now = datetime.datetime.now()
        content_types = [
            f"## {now.strftime('%B %d')} Update",
            f"- {random.choice(ACTIVITIES)} completed at {now.strftime('%H:%M')}",
            f"- {random.choice(EMOJIS)} Progress update",
            f"### {now.strftime('%A')} Notes"
        ]
        
        lines = random.sample(content_types, min(max_lines, len(content_types)))
        return '\n'.join(lines) + '\n'
        
    def update_file(self, filename: str, config: Dict) -> bool:
        """Update a single file"""
        file_path = self.repo_path / filename
        
        try:
            # Generate content based on file type (only markdown remains)
            if filename.endswith('.md'):
                content = self.update_markdown(file_path, config['max_lines'])
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write('\n' + content)
            else:
                print(f"ℹ️  Skipping unsupported file type: {filename}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to update {filename}: {e}")
            return False
            
    def select_files_to_update(self) -> List[str]:
        """Intelligently select files based on weights"""
        # Use weighted random selection
        files = list(FILES_CONFIG.keys())
        weights = [FILES_CONFIG[f]['weight'] for f in files]
        
        # Select 1-2 files based on weights
        num_files = random.choices([1, 2], weights=[0.6, 0.4])[0]
        
        selected = []
        for _ in range(num_files):
            if files:  # Avoid selecting same file twice
                file = random.choices(files, weights=weights)[0]
                selected.append(file)
                idx = files.index(file)
                files.pop(idx)
                weights.pop(idx)
                
        return selected
        
    def has_changes(self) -> bool:
        """Check for uncommitted changes"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'], 
                cwd=self.repo_path, 
                capture_output=True, 
                text=True
            )
            return bool(result.stdout.strip())
        except:
            return False
            
    def commit_and_push(self, updated_files: List[str]) -> bool:
        """Commit and push changes"""
        if not self.has_changes():
            print("ℹ️  No changes to commit")
            return False
            
        # Add, commit, push
        if not self.run_git(['git', 'add', '.']):
            print("❌ Failed to add files")
            return False
            
        commit_msg = self.get_commit_message(updated_files[0])
        if not self.run_git(['git', 'commit', '-m', commit_msg]):
            print("❌ Failed to commit")
            return False
            
        if not self.run_git(['git', 'push', REMOTE_NAME, GIT_BRANCH]):
            print("❌ Failed to push")
            return False
            
        print(f"✅ Committed: {commit_msg}")
        return True
        
    def run(self):
        """Main execution"""
        print("🔄 Running daily commit automation...")

        # Always pull before updating to avoid conflicts
        if not self.pull_latest():
            return False
        
        # Select and update files
        selected_files = self.select_files_to_update()
        updated_files = []
        
        for filename in selected_files:
            if self.update_file(filename, FILES_CONFIG[filename]):
                updated_files.append(filename)
                
        if not updated_files:
            print("❌ No files updated")
            return False
            
        # Commit and push
        success = self.commit_and_push(updated_files)
        
        if success:
            print(f"✅ Success! Updated: {', '.join(updated_files)}")
        
        return success


# =============================================================================
# EXECUTION
# =============================================================================

def main():
    automation = DailyCommit()
    success = automation.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
