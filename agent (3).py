# agent.py
import os
import sys
import time
import subprocess
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.gemini import GeminiModel

# Load environment variables from .env file
load_dotenv()

# Verify API key presence
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file!", file=sys.stderr)
    sys.exit(1)

os.environ["GEMINI_API_KEY"] = gemini_api_key


# ---------------------------------------------------------
# Step 1: Define Agent Diagnostic & Remediation Tools
# ---------------------------------------------------------

@tool
def read_bug_context(file_path: str) -> str:
    """
    Reads the contents of the target source code file.
    Use this to inspect code around the reported crash line.
    """
    print(f"\n🔍 [Tool Call] Reading target file: '{file_path}'...")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"📖 [Tool Read Success] Read {len(content)} bytes.")
            return content
    return f"Error: File '{file_path}' not found."


@tool
def apply_patch(file_path: str, new_code: str) -> str:
    """
    Overwrites the specified file with patched/corrected source code.
    Pass the FULL updated file content into new_code.
    """
    print(f"\n🛠️ [Tool Call] Applying patch to '{file_path}'...")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_code)
        print("✅ [Tool Patch Success] Updated source code written.")
        return f"Successfully applied patch to '{file_path}'."
    except Exception as e:
        return f"Failed to apply patch: {str(e)}"


@tool
def verify_patch(file_path: str) -> str:
    """
    Executes target_app.py in a sandbox sub-process to verify if tests pass.
    Returns test pass output or detailed failure logs.
    """
    print(f"\n🧪 [Tool Call] Running sandbox unit tests on '{file_path}'...")
    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("🎉 [Tool Verification Passed] Sandbox execution returned code 0.")
            return f"SUCCESS! All tests passed.\nOutput:\n{result.stdout}"
        else:
            print(f"❌ [Tool Verification Failed] Sandbox exit code: {result.returncode}")
            return f"FAILURE! Tests failed with return code {result.returncode}.\nStderr Output:\n{result.stderr}"
    except Exception as e:
        return f"Execution error during verification: {str(e)}"


@tool
def create_github_pr(repo_name: str, branch_name: str, commit_message: str, pr_title: str, pr_body: str) -> str:
    """
    Creates a new Git branch, commits patched code, and opens a GitHub Pull Request.
    Call this ONLY after verify_patch returns SUCCESS.
    """
    print(f"\n🐙 [Tool Call] Creating GitHub PR on repo '{repo_name}'...")
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return "Notice: GITHUB_TOKEN not configured in .env. Skipping remote PR creation for local testing."

    try:
        from github import Github
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        main_ref = repo.get_git_ref("heads/main")
        main_sha = main_ref.object.sha
        
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_sha)
        
        with open("target_app.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        file_obj = repo.get_contents("target_app.py", ref=f"refs/heads/{branch_name}")
        repo.update_file(
            path="target_app.py",
            message=commit_message,
            content=content,
            sha=file_obj.sha,
            branch=branch_name
        )
        
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=branch_name,
            base="main"
        )
        print(f"✅ [GitHub PR Success] PR created: {pr.html_url}")
        return f"Successfully created Pull Request #{pr.number}: {pr.html_url}"
    except Exception as e:
        return f"GitHub Integration Log: {str(e)}"


# ---------------------------------------------------------
# Step 2: Agent System Prompt & Setup
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are DevSecOps Ghost, an autonomous self-healing software reliability agent built with Strands Agents SDK.

Your Objective:
1. Execute tool actions efficiently in sequence:
   Step A: Call `read_bug_context` to inspect code.
   Step B: Call `apply_patch` with corrected code.
   Step C: Call `verify_patch` to execute tests.
2. Stop immediately after `verify_patch` succeeds and output a 3-line final summary.
"""

def run_remediation_agent(target_file: str, crash_log: str):
    """Initializes and runs the Strands Agent loop with exponential backoff retry."""
    print("🤖 [DevSecOps Ghost] Initializing Strands Agent with Gemini 3.6 Flash...")
    
    model_provider = GeminiModel(
        model_id="gemini-3.6-flash"
    )

    agent = Agent(
        model=model_provider,
        tools=[read_bug_context, apply_patch, verify_patch, create_github_pr],
        system_prompt=SYSTEM_PROMPT
    )

    task_prompt = f"""
    A production crash has been detected in {target_file}!

    --- CRASH STACK TRACE ---
    {crash_log}
    ------------------------

    Inspect code, apply fix, run verify_patch, and output your summary.
    """

    print("⚡ [DevSecOps Ghost] Running autonomous remediation loop...")
    
    # Simple retry handling for free-tier rate limits
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = agent(task_prompt)
            print("\n" + "="*50)
            print("📋 AGENT FINAL REMEDIATION SUMMARY")
            print("="*50)
            print(response)
            break
        except Exception as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "ModelThrottledException" in str(e):
                wait_time = 15
                print(f"\n⏳ Rate limit reached. Waiting {wait_time}s before final summary generation (Attempt {attempt+1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise e


if __name__ == "__main__":
    sample_crash_log = """
    Traceback (most recent call last):
      File "target_app.py", line 42, in <module>
        run_test()
      File "target_app.py", line 36, in run_test
        result2 = process_user_data(edge_case_payload)
      File "target_app.py", line 16, in process_user_data
        user_name = payload["user"]["name"].upper()
    KeyError: 'user'
    """
    
    run_remediation_agent("target_app.py", sample_crash_log)