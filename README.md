# Daily Commit Automation

A Python script for automating daily commits to maintain consistent activity in your Git repository. This tool is designed to help users establish a regular commit habit.

## What it does

- Picks random files from your repo and adds small updates
- Creates realistic commit messages with timestamps

## Prerequisites

Before you start, make sure you have:

- Python 3.6 or newer
- Git installed and configured (`git config --global user.name "Your Name"`)
- A Git repository initialized and connected to a remote (e.g., GitHub, GitLab)
- Either SSH keys set up OR a personal access token configured for Git operations

## Setup

1.  **Clone or download this repository** to your local machine.
2.  **Navigate into the repository directory** in your terminal.
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the setup script**:
    ```bash
    python setup_automation.py
    ```
    *   **For Windows users**: This script will automatically create a `daily_commit_launcher.bat` file in your repository directory. You will then be guided to add this batch file to your Windows Startup folder for automatic execution.
    *   **For macOS/Linux users**: The script will verify your Git setup and provide instructions on how to manually set up automation (e.g., using `cron` or `systemd`) by referring to the relevant sections in this README.
5.  **Test the daily commit script**:
    ```bash
    python daily_commit_automation.py
    ```
    You should see a success message if everything is configured correctly.

## Customization

You can customize the script's behavior by editing `daily_commit_automation.py`:

-   **Files to update**: Modify the `FILES_CONFIG` dictionary to specify which files are updated and their update frequency.
-   **Commit messages**: Change the `COMMIT_TEMPLATES` list to define your preferred commit message formats.
-   **Activities**: Update the `ACTIVITIES` list with your desired activity descriptions.

## Automation (macOS/Linux)

If you are on macOS or Linux, after running `setup_automation.py` and verifying your Git setup, follow these instructions to automate the daily commits.

### macOS
1. Open `Automator` → New Document → Application.
2. Add "Run Shell Script" action with:
   ```bash
   cd /path/to/your/repo
   /usr/bin/env python3 daily_commit_automation.py
   ```
3. Save as an Application.
4. Add it to System Preferences → Users & Groups → Login Items.

### Linux (Cron)
Add this line to your crontab (`crontab -e`):
```bash
@reboot cd /path/to/your/repo && /usr/bin/env python3 daily_commit_automation.py
```

## Troubleshooting

**Script fails to run?**
-   Check that Python and Git are in your system's PATH.
-   Ensure your Git remote authentication is working (`git push` manually to verify).
-   Review the output of `python setup_automation.py` for any errors or warnings.

**No commits appearing?**
-   Verify that the files specified in `FILES_CONFIG` exist in your repository.
-   Look for error messages when running `daily_commit_automation.py` manually.
-   Ensure your Git credentials haven't expired or been revoked.

## Creating a Standalone Executable (Windows)

For advanced users who want to distribute the automation as a standalone executable (`.exe`) on Windows, you can use PyInstaller.

1.  **Install PyInstaller** (if you haven't already, it's listed as optional in `requirements.txt`):
    ```bash
    pip install pyinstaller
    ```
2.  **Navigate to the script directory** and run PyInstaller:
    ```bash
    pyinstaller --onefile daily_commit_automation.py
    ```
    This will create a `dist` folder containing `daily_commit_automation.exe`.
3.  **Update the batch file**: If you created a `daily_commit_launcher.bat`, you'll need to update it to point to the `.exe` file:
    ```batch
    @echo off
    CHCP 65001 > NUL
    cd /d "C:\path\to\your\repo\dist"
    daily_commit_automation.exe
    ```

--- 
"# GitLog-Daily" 
