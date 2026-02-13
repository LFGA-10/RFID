
import os
import subprocess
from datetime import datetime, timedelta
import random

# Configuration
TOTAL_COMMITS = 208
DAYS_BACK = 200 # Spread commits over last ~7 months

def git_commit(date, message):
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = date.strftime('%Y-%m-%d %H:%M:%S')
    env['GIT_COMMITTER_DATE'] = date.strftime('%Y-%m-%d %H:%M:%S')
    
    subprocess.run(['git', 'add', 'activity.log'], check=True, env=env)
    subprocess.run(['git', 'commit', '-m', message], check=True, env=env)

def main():
    print(f"Generating {TOTAL_COMMITS} commits...")
    
    # Create or clear the log file
    with open('activity.log', 'w') as f:
        f.write("Project Logs\n")
        
    start_date = datetime.now() - timedelta(days=DAYS_BACK)
    
    for i in range(TOTAL_COMMITS):
        # Calculate a random time within the spread
        # We want to fill the graph, so we linearly progress but add randomness
        day_offset = (i / TOTAL_COMMITS) * DAYS_BACK
        commit_date = start_date + timedelta(days=day_offset)
        
        # Add random hours/minutes
        commit_date = commit_date.replace(
            hour=random.randint(9, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        
        # Update file
        with open('activity.log', 'a') as f:
            f.write(f"Commit {i}: {commit_date}\n")
            
        git_commit(commit_date, f"Update activity log {i}")
        
        if i % 10 == 0:
            print(f"Progress: {i}/{TOTAL_COMMITS}")
            
    print("Generation Complete.")

if __name__ == "__main__":
    main()
