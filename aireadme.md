# 👻 DevSecOps Ghost: Autonomous Self-Healing Agent

An autonomous, self-healing software reliability agent built using the **Strands Agents SDK** and powered by **Google Gemini**. DevSecOps Ghost automatically intercepts production crash logs, analyzes the buggy source code, generates defensive code patches, verifies fixes inside a local sandbox runner, and automates pull request creation.

---

## 🎯 Key Features

- **Autonomous Crash Diagnosis**: Parses stack traces to localize bugs and inspect context.
- **Self-Healing Loop**: Overwrites buggy code with clean defensive patches via tool calls.
- **Sub-Process Sandbox Verification**: Executes test runners to verify patches before committing changes.
- **Automated Pull Requests**: Opens pull requests on GitHub upon verified resolution.

---

## 🏗️ Technical Architecture
|   Production Crash / Log    |
                           +--------------+--------------+
                                          |
                                          v
                           +--------------+--------------+
                           | Strands Agent Orchestrator  |
                           |  (DevSecOps Ghost Engine)   |
                           +--------------+--------------+
                                          |
                 +------------------------+------------------------+
                 |                        |                        |
                 v                        v                        v
       +-------------------+    +-------------------+    +-------------------+
       | read_bug_context  |    |    apply_patch    |    |   verify_patch    |
       | (Inspect source)  |    |   (Write fix)     |    | (Sandbox runner)  |
       +-------------------+    +-------------------+    +-------------------+
                                                                   |
                                                                   v
                                                        +---------------------+
                                                        |  create_github_pr   |
                                                        | (Open Pull Request) |
                                                        +---------------------

## 🛠️ Stack & Technologies

- **Agent Framework**: [Strands Agents SDK](https://github.com/strands-ai/strands)
- **LLM Engine**: Google Gemini 3.6 Flash (`google-genai` SDK v1)
- **Runtime Environment**: Python 3.13
- **Version Control Integration**: PyGithub / Git SSH
- **Configuration Management**: `python-dotenv`

---

## 🚀 Quickstart Guide

### 1. Repository Setup

```bash
git clone git@github.com:kaushiksridhar30-create/aiAGent.git
cd aiAGent
2. Environment Configuration
Create a virtual environment and install dependencies:

Bash
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate

pip install strands-agents google-genai PyGithub python-dotenv
3. API Credentials setup
Create a .env file in the project root:

Code snippet
GEMINI_API_KEY=your_gemini_api_key_here
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_REPO=kaushiksridhar30-create/aiAGent
4. Running the Autonomous Remediation Loop
Execute the main agent script:

Bash
python agent.py
📋 Example Execution Flow
Plaintext
🤖 [DevSecOps Ghost] Initializing Strands Agent with Gemini 3.6 Flash...
⚡ [DevSecOps Ghost] Running autonomous remediation loop...

🔍 [Tool Call] Reading target file: 'target_app.py'...
📖 [Tool Read Success] Read 1096 bytes.

🛠️ [Tool Call] Applying patch to 'target_app.py'...
✅ [Tool Patch Success] Updated source code written.

🧪 [Tool Call] Running sandbox unit tests on 'target_app.py'...
🎉 [Tool Verification Passed] Sandbox execution returned code 0.

🐙 [Tool Call] Creating GitHub PR on repo 'kaushiksridhar30-create/aiAGent'...
✅ [GitHub PR Success] PR created: [https://github.com/kaushiksridhar30-create/aiAGent/pull/1](https://github.com/kaushiksridhar30-create/aiAGent/pull/1)
📜 License
This project is licensed under the MIT License - see the LICENSE file for details.


<ElicitationsGroup message="What is your next step before submitting?">
  <Elicitation label="Generate complete text for Devpost submission fields" query="Write out the complete text description for the 'Inspiration', 'What it does', 'How we built it', and 'Challenges we ran into' sections for Devpost."/>
</ElicitationsGroup>