# MiniAgent

A lightweight tool-calling AI Agent built with Python and DeepSeek.

This project is designed to learn and practice real-world Agent engineering step by step, including:

- Agent Loop
- Tool Calling
- Tool Registry
- File System Tools
- Error Recovery
- Logging
- Security Restrictions
- Automated Testing
- Dependency Management
- Git Workflow

---

## 1. Project Architecture

MiniAgent follows a simple Agent loop:

```text
User
  ↓
Agent
  ↓
LLM
  ↓
Tool Call?
  ├── No → Return final answer
  │
  └── Yes
        ↓
      Python Tool
        ↓
      Tool Result
        ↓
      History
        ↓
      LLM
        ↓
      Repeat