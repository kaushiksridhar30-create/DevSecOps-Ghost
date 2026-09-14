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