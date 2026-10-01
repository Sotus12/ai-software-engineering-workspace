# AI-Powered Multi-Agent Software Engineering Workspace

An end-to-end multi-agent system that transforms natural-language software requirements into requirements, architecture, source code, automated tests, code review reports, and execution artifacts.

## System Architecture

The workspace coordinates specialized AI agents using a central **LangGraph Orchestrator**:

1. **Requirement Agent** — Converts user prompt into structured user stories, functional/non-functional requirements, and task lists.
2. **Architecture Agent** — Designs the tech stack, API specifications, DB schema, and directory layout.
3. **Developer Agent** — Generates and writes project files using approved tool interfaces.
4. **Testing Agent** — Generates unit/integration tests, runs tests, and reports pass/fail feedback.
5. **Code Review Agent** — Performs quality, security, and maintainability audits.
6. **Orchestrator (Person 1)** — Coordinates state flow, agent handoffs, testing feedback loops, and retry limits.

## Project Structure

```
ai-software-engineering-workspace/
├── README.md
├── .gitignore
├── .env.example
├── backend/
│   ├── main.py              # FastAPI server & endpoints
│   ├── config.py            # Global settings & environment variables
│   ├── requirements.txt     # Backend dependencies
│   ├── workflow/
│   │   ├── state.py         # Shared ProjectState schema
│   │   └── graph.py         # LangGraph state machine & feedback loop
│   ├── agents/              # Specialized agent implementations
│   │   ├── requirement_agent.py
│   │   ├── architecture_agent.py
│   │   ├── developer_agent.py
│   │   ├── testing_agent.py
│   │   └── review_agent.py
│   ├── tools/               # File & terminal execution tools
│   │   ├── file_tools.py
│   │   ├── terminal_tools.py
│   │   └── docker_tools.py
│   └── projects/            # Storage for generated project workspaces
├── frontend/                # React / Vite UI workspace
├── tests/                   # Backend tests
└── docs/                    # Architecture & API documentation
```

## Quick Start (Backend)

1. Clone the repository and switch to your feature branch:
   ```bash
   git clone https://github.com/Sotus12/ai-software-engineering-workspace.git
   cd ai-software-engineering-workspace
   git checkout feature/orchestrator
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate

   pip install -r backend/requirements.txt
   ```

3. Run the FastAPI development server:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

4. API documentation will be available at: `http://localhost:8000/docs`
