<div align="center">

# Smart Event Management 🚀

### *Agentic AI Powered Event Intelligence & Event Management Platform*

[![Python](https://img.shields.io/badge/Python-3.12+-FFB300?style=for-the-badge&logo=python&logoColor=black)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-FFB300?style=for-the-badge&logo=fastapi&logoColor=black)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-FFB300?style=for-the-badge&logo=postgresql&logoColor=black)](https://www.postgresql.org/)
[![LangGraph](https://img.shields.io/badge/Agent-LangGraph-FFB300?style=for-the-badge)](https://www.langchain.com/langgraph)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**An end-to-end event management system with role-based access, an AI assistant built on LangGraph and Groq, and RAG-based knowledge retrieval.**

</div>

------------------------------------------------------------------------

### 🔗 Project Repository

> **💻 GitHub:** [Smart Event Management --- Team A](https://github.com/pawsaledhanshri-007/Smart-Event-Management---Team-A)

------------------------------------------------------------------------

### 📑 Table of Contents

-   [🧠 Overview](#-overview)
-   [🎓 What Makes Smart Event Management Different?](#-what-makes-smart-event-management-different)
-   [🎯 Core Philosophy](#-core-philosophy)
-   [✨ Key Features](#-key-features)
-   [🚀 Core Capabilities](#-core-capabilities)
-   [👥 Target Audience](#-target-audience)
-   [💻 Technology Stack](#-technology-stack)
-   [🏗️ System Architecture](#-system-architecture)
-   [🤖 Agentic AI Engine](#-agentic-ai-engine)
-   [🔬 Business Layer & Tool Logic](#-business-layer--tool-logic)
-   [🗺️ User Journey & Experience Map](#-user-journey--experience-map)
-   [🖥️ Screen-by-Screen Breakdown](#-screen-by-screen-breakdown)
-   [🏗️ Layout Component Architecture](#-layout-component-architecture)
-   [🗄️ Database Architecture & Design](#-database-architecture--design)
-   [🔎 RAG & Knowledge Retrieval System](#-rag--knowledge-retrieval-system)
-   [📊 Agent Observability & Audit System](#-agent-observability--audit-system)
-   [💻 Developer's Portal](#-developers-portal)
-   [🐳 Docker Development](#-docker-development)
-   [🔄 Database Migrations](#-database-migrations)
-   [🧪 Testing](#-testing)
-   [🔐 Security](#-security)
-   [📌 Current Status & Known Limitations](#-current-status--known-limitations)
-   [🔮 Future Roadmap](#-future-roadmap)
-   [🤝 Contributing](#-contributing)
-   [👥 Meet the Team](#-meet-the-team)
-   [📜 License](#-license)

------------------------------------------------------------------------

### 🧠 Overview

**Smart Event Management System** is a web-based event management platform that covers the event lifecycle: creating venues, scheduling events, registering participants, and managing registrations. Access is role-based, with participant, organizer and admin roles.

The platform also includes an AI assistant. It accepts natural-language requests, selects controlled backend tools based on the user's role, and answers event-information questions using RAG.

The project is an MVP. It is designed to show the full path from a user request to backend business logic, database operation, AI tool execution and final response. The current implementation status of each module is listed in [Current Status & Known Limitations](#-current-status--known-limitations).

------------------------------------------------------------------------

### 🎓 What Makes Smart Event Management Different?

| Feature | Traditional Event Platforms | 🚀 Smart Event Management |
| :--- | :--- | :--- |
| **Event Discovery** | Manual browsing and filtering | Event search in the UI and through the AI assistant |
| **Registration** | Multiple manual steps | Capacity and duplicate checks in one service call |
| **Venue Management** | Separate management screens | Venue availability checked against event schedules |
| **User Interaction** | UI-only interaction | UI and AI assistant interaction |
| **Knowledge Access** | Static FAQs and pages | RAG answers grounded in event information |
| **Automation** | Limited workflow automation | Controlled AI tool execution by role |
| **Observability** | Basic application logs | Agent session, run, tool-call and audit tables in the schema |

------------------------------------------------------------------------

<div align="center">

## 🏛️ Core Philosophy

# <span style="color: #FFB300;">Discover. Automate. Manage.</span>

*Reducing the friction between event discovery, registration, and intelligent assistance.*

------------------------------------------------------------------------

</div>

Smart Event Management operates on three fundamental principles:

1.  **🤖 Agentic Intelligence:** Natural-language requests are interpreted and converted into controlled backend actions.
2.  **🗄️ Reliable Data Management:** PostgreSQL stores event, venue, user and registration data with relational integrity constraints.
3.  **🎯 Grounded Assistance:** RAG retrieves relevant event information so the AI answers from project data rather than from general knowledge.

------------------------------------------------------------------------

### ✨ Key Features

| 🛠️ Feature | 📝 Description |
| :--- | :--- |
| **🤖 AI Event Assistant** | Understands natural-language requests and routes them to controlled business tools, filtered by role. |
| **📅 Event Management** | Create, update, cancel and delete events with venue, time and capacity validation. |
| **🏢 Venue Management** | Create venues with capacity. Check availability. Deleting a venue is blocked while an active event uses it. |
| **🎟️ Registration Management** | Register, view and cancel registrations, with duplicate and capacity checks. |
| **🔐 Authentication & RBAC** | JWT login with User and Admin account types. Public signup creates participants. Admins are seeded. |
| **🔎 RAG Knowledge Search** | Answers event questions from indexed event information using embeddings, vector search and Gemini. |
| **🧠 Agent Observability** | Database tables for agent sessions, runs, tool calls, latency, errors and audit logs. |
| **🗄️ PostgreSQL + pgvector** | Relational storage for application data, with a vector extension for embeddings. |
| **🐳 Docker Support** | Docker Compose setup for running the backend and database in containers. |

------------------------------------------------------------------------

## 🚀 Core Capabilities

| Capability | Technical Realization | Impact |
| :--- | :--- | :--- |
| **Event Management** | FastAPI + SQLAlchemy + PostgreSQL | Structured event creation and management with schedule and capacity rules. |
| **Registration Workflow** | Service layer + relational constraints | Prevents duplicate registrations and enforces capacity. |
| **Agentic Automation** | LangGraph + LangChain tools + Groq | Converts natural-language requests into backend actions. |
| **Knowledge Retrieval** | SentenceTransformers + FAISS (prototype), pgvector (schema) + Gemini | Answers event questions from indexed event information. |
| **Authentication** | bcrypt password hashing + JWT | Protects routes and enforces account-type and role checks. |
| **Observability** | Agent session, run and tool-call tables | Designed to make AI execution traceable and debuggable. |

------------------------------------------------------------------------

## 👥 Target Audience

| User Group | Use Case | Primary Benefit |
| :--- | :--- | :--- |
| **🎓 Participants** | Browse, search and register for events | Faster event discovery and registration. |
| **👨‍💼 Organizers** | Discover events and venues; event management tools defined in the agent | Centralized view of events and venues. Organizer login is not yet available. |
| **🛡️ Administrators** | Create and manage events, venues and registrations | Control over scheduling, capacity and venue usage. |
| **🤖 AI Assistant Users** | Natural-language event requests | Conversational access to event operations and event information. |
| **🏢 Institutions** | Run workshops, seminars and college events | Structured event lifecycle management. |

------------------------------------------------------------------------

## 💻 Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | ![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white) | Single-page application with React Router and Context API for auth state. |
| **Styling** | CSS | Responsive layout and reusable component styles. |
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | API routes, validation, authentication and application services. |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Backend, database integration, agent and RAG orchestration. |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2.x-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white) | Object-relational database interaction. |
| **DB Driver** | `psycopg 3` | PostgreSQL connectivity. |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL_17-336791?style=flat-square&logo=postgresql&logoColor=white) | Transactional relational data storage. |
| **Vector Search** | ![pgvector](https://img.shields.io/badge/pgvector-PostgreSQL-blue?style=flat-square) ![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-FFB300?style=flat-square) | Embedding storage in the schema (pgvector). FAISS is used by the current RAG prototype. |
| **Embeddings** | SentenceTransformers `all-MiniLM-L6-v2` | 384-dimensional sentence embeddings for RAG. |
| **Agent Framework** | ![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-FFB300?style=flat-square) ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square) | Stateful agent workflow and controlled tool execution. |
| **LLM (Agent)** | ![Groq](https://img.shields.io/badge/Groq_Cloud-F34F29?style=flat-square) | GPT-OSS-120B through LangChain's OpenAI-compatible interface. |
| **LLM (RAG)** | Google Gemini API | Generates answers from retrieved context. |
| **Authentication** | `passlib` (bcrypt), JWT (HS256) | Password hashing and signed access tokens. |
| **Migrations** | ![Alembic](https://img.shields.io/badge/Alembic-Migrations-FFB300?style=flat-square) | Database schema versioning. |
| **Containerization** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Reproducible development environment. |

------------------------------------------------------------------------

## 🏗️ System Architecture

Smart Event Management follows a decoupled architecture. The React frontend communicates with the FastAPI backend over REST. The backend coordinates the business service layer, the LangGraph agent, the RAG retrieval path and PostgreSQL.

### 📐 High-Level Architecture

```mermaid
graph TD
    User((User)) <--> |Web UI| Frontend[Frontend UI Layer]
    Frontend <--> |REST API| Backend[FastAPI Backend]

    subgraph Application[Application Layer]
        Backend --> Services[Business / Service Layer]
        Backend --> Agent[LangGraph Agent]
        Services --> ORM[SQLAlchemy ORM]
        Agent --> Tools[Controlled Business Tools]
        Agent --> RAG[RAG Tool]
    end

    ORM <--> DB[(PostgreSQL)]
    DB --> Vector[(pgvector)]
    RAG <--> Vector
```

### 🔄 Request Flow Architecture

The step-by-step lifecycle of a natural-language request from user input to final response.

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as FastAPI Backend
    participant A as LangGraph Agent
    participant T as Business Tool
    participant R as RAG
    participant DB as PostgreSQL

    U->>F: Natural-language request
    F->>B: API request
    B->>A: Agent request
    A->>A: Understand intent
    A->>T: Execute controlled tool
    T->>DB: Read / Write data
    DB-->>T: Return result
    T-->>A: Tool result
    A->>R: Retrieve knowledge if required
    R->>DB: Semantic search
    DB-->>R: Relevant chunks
    R-->>A: Retrieved context
    A-->>B: Final response
    B-->>F: Response
    F-->>U: Display result
```

### 🔄 Complete System Flow

The internal architectural logic showing how the backend handles traditional operations and Agentic AI requests.

```mermaid
flowchart TD
    Start([User Request]) --> Router{Request Type}

    Router -->|Traditional UI Action| API[FastAPI API]
    Router -->|Natural Language| Agent[LangGraph Agent]

    API --> Service[Business / Service Layer]
    Service --> ORM[SQLAlchemy]
    ORM --> DB[(PostgreSQL)]

    Agent --> Intent[Intent Understanding]
    Intent --> ToolChoice{Tool or RAG?}

    ToolChoice -->|Business Operation| Tool[Controlled Business Tool]
    Tool --> Service
    Service --> ORM

    ToolChoice -->|Knowledge Question| RAG[RAG Retrieval]
    RAG --> Vector[pgvector Search]
    Vector --> DB

    ORM --> DB
    DB --> Result[Tool / Query Result]
    Result --> Agent
    Agent --> Response[Final Response]
    API --> Response
    Response --> UI[Frontend]
```

------------------------------------------------------------------------

### ⚙️ Event Management Pipeline

The transformation of a user action into a validated database operation follows a structured pipeline.

| 📍 Phase | 🏷️ Title | 🛠️ Technical Process | 📤 Output |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Request** | User action through the UI or a natural-language request | **Validated Request** |
| **Phase 2** | **Routing** | FastAPI endpoint or agent intent routing | **Operation Type** |
| **Phase 3** | **Business Logic** | Service layer applies application rules | **Approved Operation** |
| **Phase 4** | **Persistence** | SQLAlchemy ORM executes the database operation | **Database Result** |
| **Phase 5** | **Response** | Backend returns a structured result to the UI or agent | **Final Response** |

------------------------------------------------------------------------

## 🤖 Agentic AI Engine

The Agentic AI component interprets a user's request, selects a controlled tool, runs it, reads the result, and decides whether another step is needed. The agent does not run free-form database queries. It only calls the tools provided for the user's role.

### 🔧 How It Works

The agent is triggered when a user sends a natural-language request:

1.  **Intent Understanding:** Identify what the user is asking.
2.  **Tool Selection:** Select the appropriate business tool or RAG tool for the user's role.
3.  **Execution:** Run the selected operation.
4.  **Observation:** Read the tool result.
5.  **Continuation:** Decide whether another action is required.
6.  **Response:** Return a final response based on the result.

### 🔑 Tools by Role

| Capability | Admin | Participant | Organizer |
| :--- | :---: | :---: | :---: |
| View and search events, upcoming events, event details | ✅ | ✅ | ✅ |
| View and search venues, venue details, check availability | ✅ | ✅ | ✅ |
| Create, update and cancel events | ✅ | ❌ | ❌ |
| Register for events | ✅ | ✅ | ❌ |
| View own registrations and cancel them | ✅ | ✅ | ❌ |
| View all registrations for an event and manage them | ✅ | ❌ | ❌ |
| Create and delete venues | ✅ | ❌ | ❌ |

### 🔄 Agentic Flow Diagram

```mermaid
flowchart TD
    A[User Request] --> B[Intent Understanding]
    B --> C{Select Action}

    C -->|Event / Venue / Registration| D[Business Tool]
    C -->|Policy / Knowledge Question| E[RAG Tool]

    D --> F[Backend Service]
    F --> G[(PostgreSQL)]
    G --> H[Tool Result]

    E --> I[Semantic Search]
    I --> J[(pgvector)]
    J --> K[Retrieved Context]

    H --> L[Agent Observation]
    K --> L

    L --> M{More Action Required?}
    M -->|Yes| C
    M -->|No| N[Final Response]
```

------------------------------------------------------------------------

## 🔬 Business Layer & Tool Logic

The **Business Layer** sits between the API layer and the database layer. The service layer contains the application rules and coordinates database operations.

```text
API Layer
    ↓
Business / Service Layer
    ↓
SQLAlchemy ORM
    ↓
PostgreSQL
```

### Example: Event Registration

When a participant registers for an event, the service checks:

1.  The user account is active.
2.  The event exists.
3.  The event status is `scheduled`.
4.  The user is not already registered.
5.  Event capacity is still available.
6.  A `confirmed` registration is created and the transaction is committed.

If any check fails, the service raises an error and no registration is created.

### Business Rules

| Rule | Purpose |
| :--- | :--- |
| **Unique User + Event** | Prevents duplicate registration. |
| **Active User Required** | Disabled accounts cannot register or hold valid tokens. |
| **Registration Only for Scheduled Events** | Prevents registering for ongoing, completed or cancelled events. |
| **Capacity Limits** | Registrations cannot exceed event capacity. Event capacity cannot exceed venue capacity. |
| **Valid Event Timing** | Ensures end time is after start time. |
| **Venue Overlap Check** | Prevents two events from using the same venue at overlapping times. |
| **Positive Capacity** | Prevents invalid event and venue capacity. |
| **Foreign Keys** | Maintains relationships between users, events, venues and registrations. |
| **Role Validation** | Restricts operations according to user role. |

### Business Tool Routing

```text
User Request
     ↓
Agent
     ↓
Controlled Tool
     ↓
Business Service
     ↓
Database
     ↓
Result
     ↓
Agent
     ↓
User
```

The agent does not perform uncontrolled database operations. Tools call the backend business services.

------------------------------------------------------------------------

## 🗺️ User Journey & Experience Map

Smart Event Management is designed to provide a clear path from event discovery to registration and assistance.

### 🔄 The End-to-End Journey

| Stage | User Goal | System Touchpoint | Experience |
| :--- | :--- | :--- | :--- |
| **1. Discovery** | Find an event | Events page / AI Assistant | 🔎 Curious |
| **2. Entry** | Access the system | Login / Registration | 🔐 Secure |
| **3. Search** | Find a suitable event | Event search / AI Assistant | 🎯 Focused |
| **4. Evaluation** | Check details and availability | Event Details | 🧐 Informed |
| **5. Registration** | Register for the event | Registration workflow | 🎟️ Confident |
| **6. Assistance** | Ask event information questions | RAG-backed AI Assistant | 🤖 Supported |
| **7. Management** | Review or cancel registrations | Registrations page | ✅ Organized |

------------------------------------------------------------------------

## 🖥️ Screen-by-Screen Breakdown

The interface covers the event lifecycle and the AI assistant.

| Screen Name | Core Functionality | Key UI Elements |
| :--- | :--- | :--- |
| **🔐 Login** | Authenticate as User or Admin | Account type selector, email, password, visibility toggle |
| **📝 Registration** | Create a participant account | Name, email, phone, age, college, password |
| **📊 Dashboard** | Central access point | Links to events, venues, registrations and the AI assistant |
| **📅 Events** | Browse and search events | Event cards, search by title and description, Create and Delete Event (admin) |
| **📄 Event Details** | View full event information | Date, time, venue, capacity, registration fee, status, Register or Cancel |
| **🏢 Venues** | View venues | Venue cards with name, location and capacity, Add Venue and Delete Vacant Venue (admin) |
| **🎟️ Registrations** | View own registrations | Event, registration status and date, cancellation |
| **🤖 AI Assistant** | Natural-language event interaction | Chat interface, tool responses, RAG answers |

------------------------------------------------------------------------

## 🔑 Login & Registration Screens

### Login

The login page has a User and Admin option. The selected account type sets the login request and the navigation after sign-in:

| Interface Element | User Input | System Action |
| :--- | :--- | :--- |
| **Account Type** | User or Admin | Sends the selected role with the login request. |
| **Email and Password** | Account credentials | Verifies the bcrypt hash and role match. |
| **Post-login navigation** | None | Admin opens the admin dashboard. User opens the user dashboard and AI Assistant. |

### Registration

Public registration is for participants only. Every account created here has the `participant` role. Admin accounts are created by the seed script, not from the signup page.

| Interface Element | User Input | System Action |
| :--- | :--- | :--- |
| **Account Details** | Name, email, password | Creates an active participant account with a hashed password. |
| **Profile Information** | Phone, age, college (optional) | Stores profile information. |
| **After Signup** | None | User logs in with the new credentials. |

------------------------------------------------------------------------

## ⚙️ Event & Registration Screen Breakdown

### 🛠️ Event Management Screen

| Feature | Control Type | Logic / Impact |
| :--- | :--- | :--- |
| **Event Title** | Text Input | Defines the event identity. |
| **Description** | Text Area | Stores event information. |
| **Venue** | Selection | Connects the event to a venue. The venue capacity limits the event capacity. |
| **Capacity** | Numeric Input | Controls maximum participation. |
| **Start / End Time** | Date-Time Input | Defines the event schedule. End time must be after start time. |
| **Registration Fee** | Numeric Input | Stores the fee shown on event details. |
| **Status** | Status Display | Shows scheduled, ongoing, completed or cancelled. Changed through the event update and cancel actions. |

------------------------------------------------------------------------

### 🎟️ Registration Interface

The registration interface applies business rules before storing a registration.

| Element | Component Type | Functionality |
| :--- | :--- | :--- |
| **Event Selection** | Event Card / Detail | Identifies the event. |
| **Availability** | Capacity Indicator | Shows whether registration can proceed. |
| **Register Button** | CTA | Starts the registration workflow. |
| **Duplicate Check** | Business Logic | Prevents repeated registration. |
| **Registration Status** | Status Indicator | Shows confirmed, cancelled or waitlisted state. |

------------------------------------------------------------------------

### 🤖 AI Assistant Screen

The AI Assistant provides conversational access to event operations and event information.

| Interaction | AI Behaviour | Example |
| :--- | :--- | :--- |
| **Event Search** | Business Tool | "What events are coming up?" |
| **Registration** | Business Tool | "Register me for TechFest 2026." |
| **Venue Query** | Business Tool | "Which venues have capacity above 300?" |
| **Event Information** | RAG | "When is the registration deadline?" |
| **Hybrid Request** | Tool + RAG | "Register me for TechFest 2026 and tell me what to bring." |

Event information answers come from the indexed event data. If the data does not contain the answer, the assistant should say so rather than guess.

------------------------------------------------------------------------

## 🏗️ Layout Component Architecture

The frontend uses a shared layout so navigation and the page structure stay consistent across screens.

| Component | UI Role | Functionality & Logic |
| :--- | :--- | :--- |
| **Layout** | Application shell | Common layout and structure for all pages. |
| **Navbar** | Header navigation | Navigation between Dashboard, Events, Venues, Registrations and AI Assistant, with login state. |
| **Page Views** | Main content | Login, Registration, Dashboard, Events, Event Details, Venues, Registrations, AI Assistant. |
| **CreateEventModal** | Dialog | Event creation form used by admins. |
| **AuthContext** | State provider | Current user, role, login state and logout. |
| **API Service** | Data layer | Sends requests, attaches the Bearer token, handles responses and errors. |

### 🎨 Visual Hierarchy

The layout follows a clear application hierarchy:

1.  **Layer 0 (Background):** Application background and global styling.
2.  **Layer 1 (Layout):** Navbar and page shell.
3.  **Layer 2 (Content):** Event, venue and registration cards, and the dashboard.
4.  **Layer 3 (Interaction):** Forms, the create-event modal, AI responses and error messages.

------------------------------------------------------------------------

## 🗄️ Database Architecture & Design

The database is the persistent foundation of the system. PostgreSQL stores transactional application data, and the pgvector extension supports the vector representation required for RAG.

### 🧱 Core Application Tables

| Table | Purpose |
| :--- | :--- |
| **users** | User accounts, roles (admin, organizer, participant) and profile information. |
| **venues** | Venue location and capacity. |
| **events** | Event details, organizer, venue, schedule, capacity and status. |
| **registrations** | Relationship between users and events, with registration status. |

### 🤖 Agent / Observability Tables

| Table | Purpose |
| :--- | :--- |
| **agent_sessions** | Stores user agent sessions. |
| **agent_runs** | Stores individual agent executions. |
| **tool_calls** | Stores tools executed during agent runs, with latency. |
| **audit_logs** | Stores important actions for traceability. |

### 📚 RAG Tables

| Table | Purpose |
| :--- | :--- |
| **knowledge_documents** | Stores source knowledge documents. |
| **knowledge_chunks** | Stores document chunks and vector embeddings. |

------------------------------------------------------------------------

### 🔗 Database Relationship Diagram

```mermaid
erDiagram
    USERS ||--o{ EVENTS : organizes
    USERS ||--o{ REGISTRATIONS : makes
    VENUES ||--o{ EVENTS : hosts
    EVENTS ||--o{ REGISTRATIONS : receives

    USERS ||--o{ AGENT_SESSIONS : owns
    AGENT_SESSIONS ||--o{ AGENT_RUNS : contains
    AGENT_RUNS ||--o{ TOOL_CALLS : executes

    KNOWLEDGE_DOCUMENTS ||--o{ KNOWLEDGE_CHUNKS : contains
    USERS ||--o{ AUDIT_LOGS : creates
```

------------------------------------------------------------------------

### 🔐 Database Integrity & Constraints

The database uses relational constraints to prevent invalid data.

| Constraint | Example |
| :--- | :--- |
| **Primary Key** | UUID-based identifiers (generated with `pgcrypto`). |
| **Foreign Key** | Event → Venue and Event → Organizer (user). |
| **Unique Constraint** | User email, and one registration per user and event. |
| **Check Constraint** | Positive capacity, valid event timing, valid role and status values. |
| **Indexes** | Foreign keys and frequently queried timestamps, such as `events.start_time` and `agent_runs.created_at`. |
| **Delete Rules** | Events → users and venues: RESTRICT. Registrations → events: CASCADE. Audit logs → users: SET NULL. |

### 🔄 Registration Data Flow

```mermaid
flowchart TD
    A[Participant] --> B[Registration Request]
    B --> C[Check Event]
    C --> D[Check User]
    D --> E[Check Duplicate]
    E --> F[Check Capacity]
    F --> G[Create Registration]
    G --> H[Commit Transaction]
    H --> I[Registration Confirmation]
```

------------------------------------------------------------------------

## 🔎 RAG & Knowledge Retrieval System

The RAG subsystem lets the AI assistant answer event-information questions from indexed project data.

### 📚 RAG Pipeline

```mermaid
flowchart TD
    A[Knowledge Document] --> B[Document Processing]
    B --> C[Text Chunking]
    C --> D[Embedding Generation]
    D --> E[(PostgreSQL + pgvector)]

    F[User Question] --> G[Query Embedding]
    G --> H[Similarity Search]
    H --> E
    E --> I[Relevant Chunks]
    I --> J[Agent / LLM]
    J --> K[Grounded Answer]
```

### 🧪 Current Prototype

The RAG prototype runs separately from the main backend. It is not yet connected to the database.

| Item | Prototype Value |
| :--- | :--- |
| **Data source** | `event_data.txt` (sample event: TechFest 2026) |
| **Chunks** | 7 |
| **Embedding model** | `all-MiniLM-L6-v2` (384 dimensions) |
| **Vector store** | FAISS |
| **Answer model** | Google Gemini API |

The schema defines `knowledge_chunks` with `VECTOR(1536)` for pgvector. This does not match the 384-dimensional prototype embeddings. The team needs to choose one dimension and one store before the RAG module is integrated.

### 🔌 RAG Endpoints

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `GET` | `/health` | Checks that the RAG service is running. |
| `POST` | `/ask` | Accepts `{"question": "..."}` and returns `{"question": "...", "answer": "..."}`. |

If processing fails, the API returns HTTP `503` with "The RAG service is temporarily unavailable. Please try again later."

### 📊 RAG Components

| Component | Purpose |
| :--- | :--- |
| **Document** | Original source material. |
| **Chunk** | Smaller searchable unit of the document. |
| **Embedding** | Numerical vector representation of semantic meaning. |
| **Vector Search** | Finds semantically relevant chunks. |
| **Context** | Retrieved information supplied to the AI. |
| **Final Answer** | Response grounded in retrieved knowledge. |

------------------------------------------------------------------------

## 📊 Agent Observability & Audit System

The database defines tables that record AI execution, so agent behaviour can be traced and evaluated. Full runtime recording depends on the agent integration, which is still in progress.

### 🔄 Agent Observability Flow

```mermaid
flowchart TD
    A[User Request] --> B[Agent Session]
    B --> C[Agent Run]
    C --> D[Tool Call]
    D --> E[Tool Result]
    E --> F[Latency / Error / Status]
    F --> G[Audit / Observability Data]
```

### 📋 Recorded Information

| Data | Purpose |
| :--- | :--- |
| **Session ID** | Groups related interactions. |
| **Run ID** | Identifies an individual agent execution. |
| **Tool Name** | Shows which backend capability was selected. |
| **Tool Input / Result** | Helps inspect tool execution. |
| **Latency** | Measures execution performance. |
| **Error Information** | Supports debugging. |
| **Actor / User** | Connects activity to the responsible user. |
| **Timestamp** | Establishes execution history. |

------------------------------------------------------------------------

## 💻 Developer's Portal

This section explains how to set up a local development environment.

### 📋 Prerequisites

-   **Python 3.12+:** For FastAPI, SQLAlchemy, the agent and the RAG module.
-   **Node.js (LTS):** For the React frontend.
-   **PostgreSQL 17:** For relational database storage.
-   **pgcrypto and pgvector extensions:** Required by the database schema.
-   **Docker Desktop:** Optional. Recommended for running the backend and database together.
-   **Git:** For source control and collaboration.
-   **API keys:** A Groq key for the agent, and a Gemini key for RAG.

### 🛠️ Installation & Setup

1.  **Clone the Project**

    ```bash
    git clone https://github.com/pawsaledhanshri-007/Smart-Event-Management---Team-A.git
    cd Smart-Event-Management---Team-A
    ```

2.  **Create the Environment File**

    Copy `.env.example` to `.env` in the project root. Never commit `.env`.

    ```env
    DATABASE_URL=postgresql+psycopg://event_admin:YOUR_PASSWORD@localhost:5432/event_management
    SECRET_KEY=<output of: openssl rand -hex 32>
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    ADMIN_EMAIL=admin@example.com
    ADMIN_PASSWORD=<a strong password>
    GROQ_API_KEY=your_groq_api_key_here
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

3.  **Option A: Run with Docker**

    ```bash
    docker compose up --build
    docker compose ps
    ```

4.  **Option B: Run locally**

    ```bash
    # Backend
    cd backend
    python -m venv venv
    # Mac/Linux: source venv/bin/activate
    # Windows:   venv\Scripts\activate
    pip install -r requirements.txt
    alembic upgrade head
    python seed_data.py          # creates the admin account from .env
    uvicorn app.main:app --reload
    ```

5.  **Backend API Docs**

    Open the Swagger UI:

    ```text
    http://localhost:8000/docs
    ```

6.  **Frontend**

    ```bash
    cd frontend
    npm install
    npm run dev
    ```

    The Vite dev server runs at `http://localhost:5173`. Set `VITE_API_URL=http://localhost:8000/api` in the frontend `.env` so the app reaches the backend.

7.  **Database Settings (development)**

    ```text
    Database: event_management
    User:     event_admin
    Host:     localhost
    Port:     5432
    ```

### 🔧 Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | ✅ | PostgreSQL connection string using the `postgresql+psycopg://` form. |
| `SECRET_KEY` | ✅ | Signs JWTs. Keep it long, random and private. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ❌ | Token lifetime in minutes. Default 1440 (24 h). |
| `ADMIN_EMAIL` | For seeding | Email of the seeded admin account. |
| `ADMIN_PASSWORD` | For seeding | Password of the seeded admin account. Stored hashed. |
| `GROQ_API_KEY` | For the agent | Groq Cloud API key. |
| `GEMINI_API_KEY` | For RAG | Google Gemini API key. |
| `VITE_API_URL` | Frontend | Backend base URL, for example `http://localhost:8000/api`. Read at build time. |

------------------------------------------------------------------------

## 🐳 Docker Development

The project supports containerized backend and database execution.

### Start

```bash
docker compose up --build
```

### Background Mode

```bash
docker compose up -d
```

### Check Containers

```bash
docker compose ps
```

### Stop

```bash
docker compose down
```

### Development Services

| Service | Port | Purpose |
| :--- | :--- | :--- |
| **web** | `8000` | FastAPI backend |
| **db** | `5432` | PostgreSQL database |
| **frontend** | `5173` | Vite dev server, if containerized |

> The exact services and ports depend on the project's `docker-compose.yml`. Check that file if these values differ from your setup.

------------------------------------------------------------------------

## 🔄 Database Migrations

Alembic is used for database schema versioning.

### Check Current Revision

```bash
cd backend
alembic current
```

The baseline revision for the existing database is `7c7bf3ebec9d`.

### Create a Migration

```bash
alembic revision --autogenerate -m "describe change"
```

### Migration Structure

```text
backend/
├── alembic.ini
└── alembic/
    ├── env.py
    └── versions/
```

Review every migration before applying it. Do not drop or recreate an existing database. Future schema changes go through Alembic. Do not create a new initial migration.

------------------------------------------------------------------------

## 🧪 Testing

Run the automated tests from the `backend/` folder:

```bash
cd backend
pytest tests/ -v
```

The planned PostgreSQL integration tests should run against a real PostgreSQL 17 instance with pgvector, not SQLite, because the schema uses PostgreSQL-specific features.

------------------------------------------------------------------------

## 🔐 Security

The system includes these security measures:

-   Password hashing with bcrypt. Plaintext passwords are never stored.
-   JWT-based authentication with an expiry claim. Tokens are re-checked against the database on every request.
-   Role-based access control, with admin-only operations protected by a server-side check.
-   Account-type isolation at login.
-   Public signup always creates a participant. Roles cannot be set by the client.
-   Environment-based secrets, with `.env` excluded from Git.
-   Database constraints for data integrity.
-   Agent tools restricted to the business services for the user's role.
-   Audit log table for traceability.

### Environment Security

Passwords, secret keys and AI API keys must stay local and must not be committed to Git.

### Open Security Items

These are listed in full in the project checklist. Before deployment:

-   Protect the remaining routers (events, venues, registrations, agent, RAG) with the auth dependencies.
-   Restrict CORS to the frontend origin instead of `*`.
-   Add password length and complexity rules.
-   Add rate limiting on login and registration.
-   Remove the hard-coded demo passwords and turn off SQL echo.

------------------------------------------------------------------------

## 📌 Current Status & Known Limitations

### Known Inconsistencies

-   **Admin signup:** The frontend includes an Admin registration screen, but the backend has no Admin signup endpoint and the auth module seeds Admin accounts only. One of them needs to change.
-   **Organizer login:** The `organizer` role exists, but login only accepts `user`, `participant` and `admin`.
-   **Vector dimension:** The schema uses `VECTOR(1536)`. The RAG prototype uses 384-dimensional embeddings.
-   **Database URL form:** Use `postgresql+psycopg://` everywhere.

------------------------------------------------------------------------

## 🔮 Future Roadmap

Smart Event Management is evolving from a conventional event management application into an assistant that handles multi-step event workflows.

### 🛠️ Phase 1: MVP Completion

-   [ ] Complete core event CRUD
-   [ ] Complete venue management
-   [ ] Complete registration workflow
-   [ ] Complete authentication and RBAC
-   [ ] Integrate frontend with backend
-   [ ] Complete database integration
-   [ ] Validate Docker development environment

### 🤖 Phase 2: Agentic Intelligence

-   [ ] Expand controlled business tools
-   [ ] Multi-step event-management workflows
-   [ ] Improved intent classification
-   [ ] Better agent state management
-   [ ] Agent evaluation and tracing
-   [ ] Personalized event recommendations

### 🧠 Phase 3: RAG & Advanced Automation

-   [ ] Connect RAG to the database and the backend
-   [ ] Resolve the embedding dimension and vector store choice
-   [ ] Expand the knowledge base
-   [ ] Improve semantic retrieval
-   [ ] Advanced policy assistant
-   [ ] Multi-agent workflows
-   [ ] Calendar integrations
-   [ ] Automated notifications
-   [ ] Advanced analytics and reporting

------------------------------------------------------------------------

## 🤝 Contributing

Contributions are welcome.

1.  Pull the latest project changes.
2.  Work in the relevant feature branch.
3.  Keep changes limited to the assigned module.
4.  Test the changes locally.
5.  Commit the changes with a clear message.
6.  Push the branch.
7.  Open a Pull Request for review.

------------------------------------------------------------------------

## 👥 Meet the Team

**Smart Event Management --- Team A** is a 7-member project developed through separate module responsibilities: Database, Backend, Authentication & Security, Agentic AI, RAG, Frontend, and Testing / Integration / Deployment.

| Module | Scope | Owner |
| :--- | :--- | :--- |
| **Database** | Schema, models, migrations, services, seed data | Alisha |
| **Backend** | FastAPI app, routers, CORS, route guards, API docs | Hima L |
| **Authentication & Security** | Register, login, JWT, route guards, admin seeding | Kunal Paliwal |
| **Agentic AI** | LangGraph agent, role-based tools, Groq integration | Ganesh Kota |
| **RAG** | Embeddings, FAISS search, Gemini answers | Harshitha AR |
| **Frontend** | React UI, role-based navigation, API integration | Kaif Ansari |
| **Integration, Testing & Deployment** | Service wiring, environment config, testing, release | Dhanshri Pawsale |

### 📩 Project Contact

For project-related technical discussions, refer to the **Smart Event Management --- Team A** repository and the assigned module owners.

------------------------------------------------------------------------

## 📜 License

This project is licensed under the **MIT License**. See the repository `LICENSE` file for the full license text.

------------------------------------------------------------------------
