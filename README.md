# 🏢 Agent-Kit — AI Software Company in Your IDE

> **Turn your AI-powered IDE into a 53-agent software company. One solo developer. The output of a 30–50 person team.**

<div align="center">
  ![Stack](https://img.shields.io/badge/Stack-Multi--Agent-orange)
  ![License](https://img.shields.io/badge/License-MIT-blue)
  ![Status](https://img.shields.io/badge/Status-Ultimate--Hub-brightgreen)
  ![Engine](https://img.shields.io/badge/Engine-Iron--Well--v2.0-blue)
</div>

---

## 📖 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Data Model (Demo)](#data-model-demo)
- [API Reference](#api-reference)
- [Getting Started](#getting-started)
- [Build & Deployment](#build--deployment)
- [Tech Stack](#tech-stack)
- [Key Design Decisions](#key-design-decisions)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview
Agent-Kit is a high-authority, multi-agent orchestration framework designed to transform solo development into a full-scale industrial-pro software operation. Built on the **Iron Well Patterns**, it features the **SFS-001 Senior Full Stack** orchestrator, a strict **2-Phase Orchestration** protocol, and the **RA-001 README Architect** for world-class documentation.

---

## 🏛️ Architecture

Agent-Kit operates on a **Tiered Governance Model**, where authority flows from the Human Owner down through Executive, Departmental, and Meta-Management layers.

### D1. System Architecture Diagram

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#1e293b',
  'primaryTextColor': '#FFFFFF',
  'primaryBorderColor': '#334155',
  'lineColor': '#6366F1',
  'secondaryColor': '#0f172a',
  'tertiaryColor': '#1e293b',
  'fontSize': '14px'
}}}%%

graph TD
  subgraph Owner ["👤 Developer Authority"]
    Human((Human Owner))
  end

  subgraph Executive ["🎯 Tier 1: Executive Council"]
    SFS[SFS-001 Senior Full Stack]
    CTS[CTS-001 Chief Supervisor]
    SP[SP-001 Strategy Planner]
    RC[RC-001 Risk & Compliance]
  end

  subgraph Departments ["⚙️ Tier 2: Specialized Divisions"]
    ENG[Engineering - 12 Agents]
    QA[QA & Verification - 6 Agents]
    SEC[Security Hub - 5 Agents]
    PROD[Product Hub - 6 Agents]
    DX[DevOps Hub - 5 Agents]
    INTEL[AI Intelligence - 4 Agents]
    GROWTH[Marketing Hub - 6 Agents]
  end

  subgraph Meta ["🧠 Tier 3: Meta-Management"]
    MM[Memory/Loop/Permission Gov]
  end

  Human -->|Command| SFS
  SFS -->|SOP| Executive
  Executive -->|Delegation| Departments
  Departments -->|Review| QA
  QA -->|Approval| CTS
  CTS -->|Verification| Human
  MM -.->|Context Sync| Departments
```

---

## 📂 Project Structure

### D2. Module Map & Directory Tree

```mermaid
graph TD
  Root[/"📁 Agent-Kit (Root)"/]
  Root --> OS[/"📁 .agent-os"/]
  Root --> SRC[/"📁 src"/]
  Root --> SCRIPTS[/"📁 scripts"/]
  Root --> MEM[/"📁 memory"/]

  OS --> AGENTS["👤 agents/ (53 Roles)"]
  OS --> SKILLS["📚 skills/ (v2.0 Directories)"]
  OS --> WF["🔄 workflows/ (SOPs)"]
  OS --> TEMP["📄 templates/"]

  SRC --> BE["⚙️ backend/ (FastAPI)"]
  BE --> AUTH["🔐 auth/"]
  
  SCRIPTS --> CHK["✅ checklist.py"]
  MEM --> GLOB["🌍 global/ (Architecture)"]
```

---

## 🔄 How It Works

### D3. Core Data Flow Diagram

```mermaid
flowchart LR
    REQ((User Requirement)) -->|Socratic Gate| PLAN[Phase 1: Planning]
    PLAN -->|CTS Approval| EXEC[Phase 2: Execution]
    EXEC -->|Code Generation| VER[Phase 3: Verification]
    VER -->|checklist.py| RA[Phase 4: RA-001 Documentation]
    RA --> OUT[Done: PR-Ready Code]

    style REQ fill:#4F46E5,color:#fff
    style OUT fill:#10B981,color:#fff
```

### D4. Request Lifecycle (Sequence)

```mermaid
sequenceDiagram
  actor User as Human Owner
  participant SFS as SFS-001 (Senior Full Stack)
  participant SP as SP-001 (Planner)
  participant ENG as Engineering Agent
  participant QA as QA Agent
  participant CTS as CTS-001 (Supervisor)

  User->>SFS: "Implement Feature X"
  SFS->>User: 3 Strategic clarifying questions
  User->>SFS: Answers
  SFS->>SP: Command Milestone Creation
  SP-->>SFS: Plan (milestones.md)
  SFS->>User: Proposed Plan Review
  User->>SFS: Approved (LGTM)
  SFS->>ENG: Targeted Task Directive
  ENG->>ENG: Implementation Phase
  ENG->>QA: Submit for Review
  QA-->>CTS: Passing Status
  CTS->>User: Final Approval Gate
```

---

## 🗄️ Data Model (Authentication Demo)

Agent-Kit includes a production-ready FastAPI authentication demo.

### D5. Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ SESSION : "authorizes"
    USER {
        int id PK
        string email UK
        string hashed_password
        datetime created_at
    }
    SESSION {
        string access_token PK
        int user_id FK
        datetime expires_at
    }
```

---

## 🔐 Authentication & Authorization

### D13. Secure Auth Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI Backend
    participant DB as User Database

    Client->>API: POST /auth/register
    API->>DB: Store Hash(Pwd)
    DB-->>API: Success
    API-->>Client: 201 Created
    
    Client->>API: POST /auth/login
    API->>DB: Query User
    API->>API: Verify Bcrypt
    API-->>Client: JWT access_token
```

---

## 🔌 API Reference

### D11. API Route Map

```mermaid
flowchart LR
    subgraph Auth ["🔐 Authentication"]
        R[POST /auth/register]
        L[POST /auth/login]
    end
    
    subgraph Root ["🏠 General"]
        RT[GET /]
    end
```

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Create a new account | No |
| POST | `/auth/login` | Authenticate and get JWT | No |
| GET | `/` | API Root / Welcome | No |

---

## ⚡ State Management

### D6. Agent Task Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Planning: New User Message
    Planning --> GatheringContext: Read Memory/Skills
    GatheringContext --> Implementing: Plan Approved
    Implementing --> Testing: Code Written
    Testing --> FinalizingDoc: checklist.py PASS
    FinalizingDoc --> Idle: notify_user
    Testing --> Implementing: checklist.py FAIL
```

---

## 🚀 Getting Started

### 📦 Quick Start (NPX Scaffolding)
The fastest way to use Agent-Kit in a new project is via `npx`. This command scaffolds the entire 53-agent framework into your current directory without requiring you to clone the whole repository.

```bash
# 1. Create and enter your new project folder
mkdir my-ai-project && cd my-ai-project

# 2. Scaffold the Agent-Kit framework
npx @ab-aswini/agent-kit-p1 init
```
**What this does:**
- Copies the `.agent-os` core (Agents, Workflows, Skills).
- Sets up the `memory/` hub for persistent context.
- Provides the `src/` demo backend for testing.
- Initializes the `scripts/` directory for health checks.

---

### 🛠️ Manual Installation (For Project Contributors)
If you want to contribute to the framework or explore its internal scripts, use the manual method:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ab-aswini/Agent-kit-P1.git
   cd Agent-kit-P1
   ```

2. **Initialize Environment:**
   ```bash
   # Prepare the hub logic
   python .agent-os/scripts/hub-setup.py
   ```

3. **Install Demo Dependencies:**
   ```bash
   pip install fastapi sqlalchemy uvicorn passlib[argon2] python-jose[cryptography]
   ```

4. **Verify System Health:**
   ```bash
   python scripts/checklist.py
   ```

---

### 🚦 Next Steps for New Users
1. **Open in AI IDE**: Open the folder in VS Code (with Cursor or Copilot).
2. **Contextualize**: Instruct your AI to: *"Read .agent-os/agents/tier-1/chief-technical-supervisor.agent.md to understand the system rules."*
3. **Start Building**: Give your first task (e.g., "Plan a new feature using the Plan Workflow") and watch the 53-agent fleet orchestrate the result.
### Configuration
Update the following environment variables if necessary:
- `SECRET_KEY`: Used for JWT signing.
- `ALGORITHM`: (Default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: (Default: 30)

---

## 🏗️ Build & Deployment

### D7. CI/CD Pipeline Flow

```mermaid
flowchart LR
    A[Git Push] --> B[Linting Check]
    B --> C[Unit tests]
    C --> D[Integration Tests]
    D --> E[Checklist.py Audit]
    E --> F{Success?}
    F -- Yes --> G[Deploy to Vercel/EC2]
    F -- No --> H[Fail & Notify]
```

---

## 📊 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Orchestration** | Markdown / JSON | High-authority agent protocols |
| **Logic (Demo)** | FastAPI | Async high-performance backend |
| **Database** | Mock (Memory) / SQLite | User storage |
| **Security Hub** | Bcrypt / JWT | Commercial-grade auth |
| **Audit** | `checklist.py` | 360-degree framework validation |
| **Diagrams** | Mermaid.js | Dynamic architecture visualization |

---

## 🧩 Key Design Decisions

1. **Iron Well Patterns**: Enforced strict planning/execution phases to prevent goal drift.
2. **Socratic Gate**: Mandatory 3-question filter for complex tasks to ensure 100% alignment.
3. **Directory-Based Skills**: Standardized on `.agent-os/skills/[NAME]/SKILL.md` for better indexability and modularity.
4. **Hierarchical Governance**: Adopted tiered agent authority (CTS-001) to prevent infinite loops and ensure quality.

---

## 🌳 Git Strategy

### D9. Branching Strategy

```mermaid
gitGraph
    commit id: "Initial"
    branch develop
    commit id: "Setup"
    branch feat/auth
    commit id: "Auth Logic"
    checkout develop
    merge feat/auth
    branch feat/ra-001
    commit id: "Master README"
    checkout develop
    merge feat/ra-001
    checkout main
    merge develop tag: "v1.0-Ultimate-Hub"
```

---

## 📄 License
This project is licensed under the **MIT License**.

---

<div align="center">
  <strong>Built for solo developers who think like companies.</strong>
  <br>
  <em>Documentation orchestrated by RA-001 README Architect.</em>
</div>
