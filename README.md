# Smart-Event-Management---Team-A
# Database Documentation — Smart Event Management System

```{=html}
<div align="center">
```
# `<span style="color: #FFB300;">`{=html}Smart Event Management System 🚀`</span>`{=html} {#smart-event-management-system-rocket}

### `<span style="color: #FFB300;">`{=html}*Agentic AI Powered Event Management & Intelligent Registration Platform*`</span>`{=html} {#agentic-ai-powered-event-management--intelligent-registration-platform}

------------------------------------------------------------------------

[![Python](https://img.shields.io/badge/Python-3.12+-FFB300?style=for-the-badge&logo=python&logoColor=black)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-FFB300?style=for-the-badge&logo=fastapi&logoColor=black)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-FFB300?style=for-the-badge&logo=postgresql&logoColor=black)](https://www.postgresql.org/)
[![LangGraph](https://img.shields.io/badge/Agent-LangGraph-FFB300?style=for-the-badge)](https://www.langchain.com/langgraph)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

**An End-to-End Intelligent Event Management Ecosystem with Agentic AI,
RAG, and Database-Driven Automation.**

```{=html}
</div>
```

------------------------------------------------------------------------

### 🔗 Project Repository {#link-project-repository}

> **💻 GitHub:** [Smart Event Management --- Team
> A](https://github.com/pawsaledhanshri-007/Smart-Event-Management---Team-A)

------------------------------------------------------------------------

### 📑 Table of Contents {#bookmark_tabs-table-of-contents}

-   [🧠 Overview](#-overview)
-   [🎓 What Makes Smart Event Management
    Different?](#-what-makes-smart-event-management-different)
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
-   [🔎 RAG & Knowledge Retrieval
    System](#-rag--knowledge-retrieval-system)
-   [📊 Agent Observability & Audit
    System](#-agent-observability--audit-system)
-   [💻 Developer\'s Portal](#-developers-portal)
-   [🔮 Future Roadmap](#-future-roadmap)
-   [🤝 Contributing](#-contributing)
-   [👥 Meet the Team](#-meet-the-team)
-   [📜 License](#-license)

------------------------------------------------------------------------

### 🧠 Overview {#brain-overview}

**Smart Event Management System** is an intelligent, web-based event
management ecosystem designed to simplify the complete event lifecycle
through a combination of **traditional application workflows and Agentic
AI**.

The system allows users to manage events, venues, registrations, and
event-related information through a conventional interface while also
providing an AI assistant capable of understanding **natural-language
requests**, selecting controlled backend tools, executing multi-step
operations, and retrieving policy or knowledge information through
**RAG**.

The system is designed around an MVP that demonstrates the complete path
from a user request to backend business logic, database operation, AI
tool execution, and final response.

------------------------------------------------------------------------

### 🎓 What Makes Smart Event Management Different? {#mortar_board-what-makes-smart-event-management-different}

  Feature                Traditional Event Platforms     🚀 Smart Event Management
  ---------------------- ------------------------------- -------------------------------------------------
  **Event Discovery**    Manual browsing and filtering   Natural-language event discovery
  **Registration**       Multiple manual steps           AI-assisted registration workflow
  **Venue Management**   Separate management screens     Integrated venue and event workflow
  **User Interaction**   UI-only interaction             UI + Agentic AI interaction
  **Knowledge Access**   Static FAQs/pages               RAG-powered contextual retrieval
  **Automation**         Limited workflow automation     Controlled AI tool execution
  **Observability**      Basic application logs          Agent sessions, runs, tool calls and audit logs

------------------------------------------------------------------------

```{=html}
<div align="center">
```
## 🏛️ Core Philosophy {#classical_building-core-philosophy}

# `<span style="color: #FFB300;">`{=html}Discover. Automate. Manage.`</span>`{=html} {#discover-automate-manage}

*Reducing the friction between event discovery, registration, and
intelligent assistance.*

------------------------------------------------------------------------

```{=html}
</div>
```
Smart Event Management operates on three fundamental principles:

1.  **🤖 Agentic Intelligence:** Natural-language requests are
    interpreted and converted into controlled backend actions.
2.  **🗄️ Reliable Data Management:** PostgreSQL maintains structured
    event, venue, user, and registration data with strong relational
    integrity.
3.  **🎯 Grounded Assistance:** RAG retrieves relevant knowledge so the
    AI can answer information and policy-related questions using project
    knowledge.

------------------------------------------------------------------------

### ✨ Key Features {#sparkles-key-features}

  🛠️ Feature                       📝 Description
  -------------------------------- -----------------------------------------------------------------------------------------------
  **🤖 AI Event Assistant**        Understands natural-language requests and routes them to controlled business tools.
  **📅 Event Management**          Create, update, view, and manage events with organizer and venue relationships.
  **🏢 Venue Management**          Maintains venue information, locations, and capacity.
  **🎟️ Registration Management**   Supports event registration while enforcing duplicate and capacity rules.
  **🔐 Authentication & RBAC**     Supports authenticated users and role-based access such as admin, organizer, and participant.
  **🔎 RAG Knowledge Search**      Retrieves relevant knowledge chunks for policy and information queries.
  **🧠 Agent Observability**       Tracks agent sessions, runs, tool calls, latency, errors, and audit activity.
  **🗄️ PostgreSQL + pgvector**     Combines relational storage with vector embeddings for RAG.
  **🐳 Docker Support**            Runs the backend and database in reproducible containers.

------------------------------------------------------------------------

## 🚀 Core Capabilities {#rocket-core-capabilities}

  Capability                  Technical Realization                    Impact
  --------------------------- ---------------------------------------- ----------------------------------------------------------------------------
  **Event Management**        FastAPI + SQLAlchemy + PostgreSQL        Provides structured event creation and management.
  **Registration Workflow**   Service Layer + Relational Constraints   Prevents duplicate registrations and supports capacity-aware registration.
  **Agentic Automation**      LangGraph + Controlled Tools             Converts natural-language requests into backend actions.
  **Knowledge Retrieval**     RAG + pgvector                           Provides context-aware answers from stored knowledge.
  **Authentication**          JWT + Password Hashing                   Secures user access and role-based operations.
  **Observability**           Agent Sessions + Runs + Tool Calls       Makes AI execution traceable and debuggable.

------------------------------------------------------------------------

## 👥 Target Audience {#busts_in_silhouette-target-audience}

  User Group                  Use Case                                Primary Benefit
  --------------------------- --------------------------------------- ---------------------------------------------
  **🎓 Participants**         Discover and register for events        Faster event discovery and registration.
  **👨‍💼 Organizers**           Create and manage events                Centralized event and venue management.
  **🛡️ Administrators**       Manage users and system activity        Better control, security, and auditability.
  **🤖 AI Assistant Users**   Natural-language event requests         Conversational access to event operations.
  **🏢 Institutions**         Manage workshops, seminars and events   Structured event lifecycle management.

------------------------------------------------------------------------

## 💻 Technology Stack {#computer-technology-stack}

  Layer                  Technology                                                                                                          Purpose
  ---------------------- ------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------
  **Frontend**           ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white)              Responsive web interface and event-management experience.
  **Styling**            ![Tailwind](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white)   Modern and responsive UI styling.
  **Backend**            ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)              API routes, validation, authentication, and application services.
  **Language**           ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)                 Backend, database integration, agent and RAG orchestration.
  **ORM**                ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)     Object-relational database interaction.
  **Database**           ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)     Transactional relational data storage.
  **Vector Search**      ![pgvector](https://img.shields.io/badge/pgvector-PostgreSQL-blue?style=flat-square)                                Stores and searches knowledge embeddings.
  **Agent Framework**    ![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-FFB300?style=flat-square)                            Stateful agent workflow and controlled tool execution.
  **RAG**                ![RAG](https://img.shields.io/badge/RAG-Knowledge_Retrieval-FFB300?style=flat-square)                               Contextual knowledge retrieval.
  **Migrations**         ![Alembic](https://img.shields.io/badge/Alembic-Migrations-FFB300?style=flat-square)                                Database schema versioning.
  **Containerization**   ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)                 Reproducible development environment.

------------------------------------------------------------------------

------------------------------------------------------------------------

## 🏗️ System Architecture {#building_construction-system-architecture}

Smart Event Management follows a decoupled architecture where the
frontend communicates with the FastAPI backend, while the backend
coordinates business services, the Agentic AI workflow, RAG retrieval,
and PostgreSQL.

### 📐 High-Level Architecture {#triangular_ruler-high-level-architecture}

``` mermaid
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

### 🔄 Request Flow Architecture {#arrows_counterclockwise-request-flow-architecture}

The step-by-step lifecycle of a natural-language request from user input
to final response.

``` mermaid
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

### 🔄 Complete System Flow {#arrows_counterclockwise-complete-system-flow}

The internal architectural logic showing how the backend handles
traditional operations and Agentic AI requests.

``` mermaid
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

### ⚙️ Event Management Pipeline {#gear-event-management-pipeline}

The transformation of a user action into a validated database operation
follows a structured pipeline:

  📍 Phase      🏷️ Title             🛠️ Technical Process                                 📤 Output
  ------------- -------------------- ---------------------------------------------------- ------------------------
  **Phase 1**   **Request**          User action through UI or natural-language request   **Validated Request**
  **Phase 2**   **Routing**          FastAPI endpoint or Agent intent routing             **Operation Type**
  **Phase 3**   **Business Logic**   Service layer applies application rules              **Approved Operation**
  **Phase 4**   **Persistence**      SQLAlchemy ORM executes database operation           **Database Result**
  **Phase 5**   **Response**         Backend returns structured result to UI/Agent        **Final Response**

------------------------------------------------------------------------

------------------------------------------------------------------------

## 🤖 Agentic AI Engine {#robot-agentic-ai-engine}

The Agentic AI component is designed to do more than generate text. It
can understand a user\'s intent, select controlled tools, execute
actions, observe their results, and decide whether another step is
required.

### 🔧 How It\'s Enabled {#wrench-how-its-enabled}

The agent is triggered when a user sends a natural-language request. It
works through a controlled workflow:

1.  **Intent Understanding:** Identify what the user is asking.
2.  **Tool Selection:** Select the appropriate backend business tool or
    RAG tool.
3.  **Execution:** Execute the selected operation.
4.  **Observation:** Read the tool result.
5.  **Continuation:** Decide whether another action is required.
6.  **Response:** Return a final grounded response.

### 🔄 Agentic Flow Diagram {#arrows_counterclockwise-agentic-flow-diagram}

``` mermaid
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

## 🔬 Business Layer & Tool Logic {#microscope-business-layer--tool-logic}

The **Business Layer** sits between the API layer and the database
layer. In this project, the service layer contains the
application-specific rules and coordinates database operations.

``` text
API Layer
    ↓
Business / Service Layer
    ↓
Repository / SQLAlchemy
    ↓
PostgreSQL
```

### Example: Event Registration

When a participant requests registration:

1.  Check whether the event exists.
2.  Check whether the user is valid.
3.  Check whether the user has already registered.
4.  Check event capacity.
5.  Create the registration.
6.  Commit the transaction.
7.  Return the result.

### Business Rules

  Rule                      Purpose
  ------------------------- ----------------------------------------------
  **Unique User + Event**   Prevents duplicate registration.
  **Positive Capacity**     Prevents invalid event/venue capacity.
  **Valid Event Timing**    Ensures end time is after start time.
  **Foreign Keys**          Maintains relationships between entities.
  **Role Validation**       Restricts operations according to user role.

### Business Tool Routing

``` text
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

The Agentic AI does not directly perform uncontrolled database
operations. Tools call the backend business services.

------------------------------------------------------------------------

## 🗺️ User Journey & Experience Map {#world_map-user-journey--experience-map}

Smart Event Management is designed to provide a frictionless path from
event discovery to registration and intelligent assistance.

### 🔄 The End-to-End Journey {#arrows_counterclockwise-the-end-to-end-journey}

  Stage                 User Goal                        System Touchpoint       Experience
  --------------------- -------------------------------- ----------------------- --------------
  **1. Discovery**      Find an event                    Events / AI Assistant   🔎 Curious
  **2. Entry**          Access the system                Login / Registration    🔐 Secure
  **3. Search**         Find a suitable event            Event Search / AI       🎯 Focused
  **4. Evaluation**     Check details and availability   Event Details           🧐 Informed
  **5. Registration**   Register for the event           Registration Workflow   🎟️ Confident
  **6. Assistance**     Ask policies or questions        RAG Assistant           🤖 Supported
  **7. Management**     Manage events or registrations   Dashboard               ✅ Organized

------------------------------------------------------------------------

## 🖥️ Screen-by-Screen Breakdown {#desktop_computer-screen-by-screen-breakdown}

The interface is designed around the main event-management lifecycle and
the conversational AI experience.

  Screen Name               Core Functionality                   Key UI Elements
  ------------------------- ------------------------------------ ----------------------------------------
  **🏠 Landing Page**       Introduce the platform               Hero Section, Features, CTA
  **🔐 Login / Register**   Authenticate users                   Login Form, Registration Form
  **📊 Dashboard**          Central management view              Event Cards, Registrations, Summary
  **📅 Events**             Browse and search events             Search, Filters, Event Cards
  **📄 Event Details**      View complete event information      Description, Venue, Capacity, Register
  **🏢 Venues**             Manage venue information             Venue Cards, Capacity, Location
  **🎟️ Registrations**      View registrations                   Status, Event Details, Cancellation
  **🤖 AI Assistant**       Natural-language event interaction   Chat Interface, Tool Responses
  **🛡️ Admin Area**         Manage users/system activity         User Management, Audit/Agent Activity

------------------------------------------------------------------------

## 🚀 Landing Screen {#rocket-landing-screen}

The landing page introduces the platform\'s core value proposition:
managing events through a conventional interface while also providing
intelligent conversational assistance.

  Section                  Content / Feature                            Strategic Purpose
  ------------------------ -------------------------------------------- --------------------------------------
  **Hero Area**            Smart Event Management headline              Communicates the primary purpose.
  **Feature Grid**         Events, Venues, Registration, AI Assistant   Highlights major capabilities.
  **AI Section**           Agentic AI workflow                          Demonstrates intelligent automation.
  **Technology Section**   FastAPI, PostgreSQL, LangGraph, Docker       Establishes technical foundation.
  **Primary CTA**          Explore / Get Started                        Guides users into the application.

------------------------------------------------------------------------

## 🏁 Onboarding Screen {#checkered_flag-onboarding-screen}

The onboarding flow prepares a user to interact with the
event-management ecosystem.

  Interface Element         User Input                        System Action
  ------------------------- --------------------------------- ----------------------------------
  **Account Setup**         Name, email, password             Creates authenticated account.
  **Role**                  Participant / Organizer / Admin   Applies role-based permissions.
  **Profile Information**   Phone, age, college               Stores user profile information.
  **Dashboard Entry**       User selects destination          Opens the appropriate workspace.

------------------------------------------------------------------------

------------------------------------------------------------------------

## ⚙️ Event & Registration Screen Breakdown {#gear-event--registration-screen-breakdown}

### 🛠️ Event Management Screen {#hammer_and_wrench-event-management-screen}

  Feature                Control Type      Logic / Impact
  ---------------------- ----------------- ----------------------------------------------------------
  **Event Title**        Text Input        Defines the event identity.
  **Description**        Text Area         Stores event information.
  **Venue**              Selection         Connects event to a venue.
  **Capacity**           Numeric Input     Controls maximum participation.
  **Start / End Time**   Date-Time Input   Defines event schedule.
  **Status**             Status Selector   Tracks scheduled, ongoing, completed or cancelled state.

------------------------------------------------------------------------

### 🎟️ Registration Interface {#tickets-registration-interface}

The registration environment applies business rules before storing a
registration.

  Element                   Component Type        Functionality
  ------------------------- --------------------- -------------------------------------------------
  **Event Selection**       Event Card / Detail   Identifies the event.
  **Availability**          Capacity Indicator    Shows whether registration can proceed.
  **Register Button**       CTA                   Starts the registration workflow.
  **Duplicate Check**       Business Logic        Prevents repeated registration.
  **Registration Status**   Status Indicator      Shows confirmed, cancelled or waitlisted state.

------------------------------------------------------------------------

### 🤖 AI Assistant Screen {#robot-ai-assistant-screen}

The AI Assistant provides conversational access to event operations and
knowledge.

  Interaction           AI Behaviour    Example
  --------------------- --------------- -----------------------------------------------------
  **Event Search**      Business Tool   \"Find workshops this week.\"
  **Registration**      Business Tool   \"Register me for this event.\"
  **Venue Query**       Business Tool   \"Which venues are available?\"
  **Policy Question**   RAG             \"What is the cancellation policy?\"
  **Hybrid Request**    Tool + RAG      \"Register me and tell me the cancellation rules.\"

------------------------------------------------------------------------

------------------------------------------------------------------------

## 🏗️ Layout Component Architecture {#building_construction-layout-component-architecture}

The Smart Event Management UI follows a modular layout system so that
navigation and core application structure remain consistent across
different workflows.

  Component               UI Role                    Functionality & Logic
  ----------------------- -------------------------- --------------------------------------------------------------
  **Navbar**              Header Navigation          User profile, navigation and application controls.
  **Sidebar**             Navigation Rail            Quick access to Dashboard, Events, Venues and Registrations.
  **Main Content**        Viewport Wrapper           Renders the active application screen.
  **Event Card**          UI Primitive               Displays event information and actions.
  **Registration Card**   Status Component           Shows registration details and status.
  **AI Chat Panel**       Conversational Interface   Sends natural-language requests to the Agentic AI layer.
  **Status Overlay**      Feedback Layer             Displays loading, success and error states.

------------------------------------------------------------------------

### 🎨 Visual Hierarchy Breakdown {#art-visual-hierarchy-breakdown}

The layout follows a clear application hierarchy:

1.  **Layer 0 (Background):** Application background and global visual
    styling.
2.  **Layer 1 (Layout):** Navbar and Sidebar.
3.  **Layer 2 (Content):** Event, venue, registration and dashboard
    cards.
4.  **Layer 3 (Interaction):** Forms, dialogs, AI responses and status
    overlays.

------------------------------------------------------------------------

------------------------------------------------------------------------

## 🗄️ Database Architecture & Design {#file_cabinet-database-architecture--design}

The database is the persistent foundation of the system. PostgreSQL
stores transactional application data while pgvector supports the vector
representation required for RAG.

### 🧱 Core Application Tables {#bricks-core-application-tables}

  Table               Purpose
  ------------------- ---------------------------------------------------------
  **users**           User accounts, roles and profile information.
  **venues**          Venue location and capacity information.
  **events**          Event details, organizer, venue, schedule and capacity.
  **registrations**   Relationship between users and events.

### 🤖 Agent / Observability Tables {#robot-agent--observability-tables}

  Table                Purpose
  -------------------- --------------------------------------------------------
  **agent_sessions**   Stores user/agent conversation sessions.
  **agent_runs**       Stores individual agent executions.
  **tool_calls**       Stores tools executed during agent runs.
  **audit_logs**       Stores important system/user actions for traceability.

### 📚 RAG Tables {#books-rag-tables}

  Table                     Purpose
  ------------------------- -----------------------------------------------
  **knowledge_documents**   Stores source knowledge documents.
  **knowledge_chunks**      Stores document chunks and vector embeddings.

------------------------------------------------------------------------

### 🔗 Database Relationship Diagram {#link-database-relationship-diagram}

``` mermaid
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

### 🔐 Database Integrity & Constraints {#closed_lock_with_key-database-integrity--constraints}

The database uses relational constraints to prevent invalid data.

  Constraint              Example
  ----------------------- --------------------------------------------------
  **Primary Key**         UUID-based entity identifiers
  **Foreign Key**         Event → Venue / Organizer
  **Unique Constraint**   User email / User + Event registration
  **Check Constraint**    Positive capacity / valid event timing
  **Indexes**             Frequently queried foreign keys and timestamps
  **Delete Rules**        CASCADE, RESTRICT and SET NULL where appropriate

### 🔄 Registration Data Flow {#arrows_counterclockwise-registration-data-flow}

``` mermaid
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

## 🔎 RAG & Knowledge Retrieval System {#mag_right-rag--knowledge-retrieval-system}

The RAG subsystem allows the AI assistant to answer knowledge and
policy-related questions using stored project information.

### 📚 RAG Pipeline {#books-rag-pipeline}

``` mermaid
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

### 📊 RAG Components {#bar_chart-rag-components}

  Component           Purpose
  ------------------- ------------------------------------------------------
  **Document**        Original source material.
  **Chunk**           Smaller searchable unit of the document.
  **Embedding**       Numerical vector representation of semantic meaning.
  **Vector Search**   Finds semantically relevant chunks.
  **Context**         Retrieved information supplied to the AI.
  **Final Answer**    Response grounded in retrieved knowledge.

------------------------------------------------------------------------

## 📊 Agent Observability & Audit System {#bar_chart-agent-observability--audit-system}

The system records AI execution information so that agent behaviour can
be traced and evaluated.

### 🔄 Agent Observability Flow {#arrows_counterclockwise-agent-observability-flow}

``` mermaid
flowchart TD
    A[User Request] --> B[Agent Session]
    B --> C[Agent Run]
    C --> D[Tool Call]
    D --> E[Tool Result]
    E --> F[Latency / Error / Status]
    F --> G[Audit / Observability Data]
```

### 📋 Recorded Information {#clipboard-recorded-information}

  Data                      Purpose
  ------------------------- ----------------------------------------------
  **Session ID**            Groups related interactions.
  **Run ID**                Identifies an individual agent execution.
  **Tool Name**             Shows which backend capability was selected.
  **Tool Input / Result**   Helps inspect tool execution.
  **Latency**               Measures execution performance.
  **Error Information**     Supports debugging.
  **Actor/User**            Connects activity to the responsible user.
  **Timestamp**             Establishes execution history.

------------------------------------------------------------------------

------------------------------------------------------------------------

## 💻 Developer\'s Portal {#computer-developers-portal}

This section provides the technical roadmap for setting up a local
development environment for Smart Event Management.

### 📋 Prerequisites {#clipboard-prerequisites}

-   **Python 3.12+**: For FastAPI, SQLAlchemy and Agentic AI backend
    development.
-   **Node.js**: For the frontend application.
-   **PostgreSQL 15+**: For relational database storage.
-   **Docker Desktop**: Recommended for running the backend and database
    together.
-   **Git**: For source control and collaboration.
-   **pgvector**: Required for vector-based RAG functionality when
    enabled.

### 🛠️ Installation & Setup {#hammer_and_wrench-installation--setup}

1.  **Clone the Project**

    ``` bash
    git clone https://github.com/pawsaledhanshri-007/Smart-Event-Management---Team-A.git
    cd Smart-Event-Management---Team-A
    ```

2.  **Docker Configuration**

    ``` bash
    docker compose up --build
    ```

3.  **Check Running Services**

    ``` bash
    docker compose ps
    ```

4.  **Backend API** Open:

    ``` text
    http://localhost:8000/docs
    ```

5.  **Frontend Configuration**

    ``` bash
    cd frontend
    npm install
    npm run dev
    ```

6.  **Database** The development configuration uses:

    ``` text
    Database: event_management
    User: event_admin
    Host: localhost
    Port: 5432
    ```

7.  **Environment Variables** Create a local `.env` based on
    `.env.example` and keep secrets out of Git:

    ``` env
    DATABASE_URL=postgresql+psycopg://event_admin:YOUR_PASSWORD@localhost:5432/event_management
    ```

------------------------------------------------------------------------

## 🐳 Docker Development {#whale-docker-development}

The project supports containerized backend and database execution.

### Start

``` bash
docker compose up --build
```

### Background Mode

``` bash
docker compose up -d
```

### Check Containers

``` bash
docker compose ps
```

### Stop

``` bash
docker compose down
```

### Development Services

  Service        Port       Purpose
  -------------- ---------- -----------------------------
  **web**        `8000`     FastAPI backend
  **db**         `5432`     PostgreSQL database
  **frontend**   `3000`\*   Frontend development server

\*The frontend may be run separately depending on the current Docker
Compose configuration.

------------------------------------------------------------------------

## 🔄 Database Migrations {#arrows_counterclockwise-database-migrations}

Alembic is used for database schema versioning.

### Check Current Revision

``` bash
cd backend
alembic current
```

### Create a Migration

``` bash
alembic revision --autogenerate -m "describe change"
```

### Migration Structure

``` text
backend/
├── alembic.ini
└── alembic/
    ├── env.py
    └── versions/
```

The project uses a baseline migration for the existing database schema.
Database migrations should be reviewed before application, and an
existing database should not be blindly dropped or recreated.

------------------------------------------------------------------------

## 🧪 Testing {#test_tube-testing}

The project includes a `tests/` area for validating the application.

Testing areas include:

-   Backend API testing
-   Database integration testing
-   Registration business-rule testing
-   Authentication testing
-   Agent tool testing
-   RAG retrieval testing
-   Frontend / end-to-end testing

------------------------------------------------------------------------

## 🔐 Security {#closed_lock_with_key-security}

The system is designed with multiple security layers:

-   Password hashing
-   JWT-based authentication
-   Role-based access control
-   Input validation
-   Authorization checks
-   Environment-based secrets
-   Database constraints
-   Controlled AI tools
-   Audit logging

### Environment Security

Actual passwords, secret keys, and AI API keys must remain local and
must not be committed to Git.

------------------------------------------------------------------------

## 🔮 Future Roadmap {#crystal_ball-future-roadmap}

Smart Event Management is evolving from a conventional event-management
application into a more autonomous event-management assistant.

### 🛠️ Phase 1: MVP Completion {#hammer_and_wrench-phase-1-mvp-completion}

-   [ ] Complete core event CRUD
-   [ ] Complete venue management
-   [ ] Complete registration workflow
-   [ ] Complete authentication and RBAC
-   [ ] Integrate frontend with backend
-   [ ] Complete database integration
-   [ ] Validate Docker development environment

### 🤖 Phase 2: Agentic Intelligence {#robot-phase-2-agentic-intelligence}

-   [ ] Expand controlled business tools
-   [ ] Multi-step event-management workflows
-   [ ] Improved intent classification
-   [ ] Better agent state management
-   [ ] Agent evaluation and tracing
-   [ ] Personalized event recommendations

### 🧠 Phase 3: RAG & Advanced Automation {#brain-phase-3-rag--advanced-automation}

-   [ ] Expand knowledge base
-   [ ] Improve semantic retrieval
-   [ ] Advanced policy assistant
-   [ ] Multi-agent workflows
-   [ ] Calendar integrations
-   [ ] Automated notifications
-   [ ] Advanced analytics and reporting

------------------------------------------------------------------------

## 🤝 Contributing {#handshake-contributing}

Contributions are welcome.

1.  Pull the latest project changes.
2.  Work in the relevant feature branch.
3.  Keep changes limited to the assigned module.
4.  Test the changes locally.
5.  Commit the changes with a clear message.
6.  Push the branch.
7.  Open a Pull Request for review.

------------------------------------------------------------------------

------------------------------------------------------------------------

## 👥 Meet the Team {#busts_in_silhouette-meet-the-team}

**Smart Event Management --- Team A** is a 7-member project developed
through separate module responsibilities covering Database, Backend,
Authentication & Security, Agentic AI, RAG, Frontend, and
Testing/Integration/Deployment.

  Team Area                                Core Contribution
  ---------------------------------------- --------------------------------------------------------------------------------------------------------
  **Database**                             PostgreSQL schema, SQLAlchemy models, relationships, constraints, migrations and database integration.
  **Backend**                              FastAPI APIs, services, repositories and backend integration.
  **Authentication & Security**            Authentication, authorization, JWT and security controls.
  **Agentic AI**                           LangGraph workflow, intent handling and controlled business tools.
  **RAG**                                  Knowledge documents, chunks, embeddings and semantic retrieval.
  **Frontend**                             User interface, dashboards, event and registration workflows.
  **Testing / Integration / Deployment**   Testing, integration, Docker and deployment workflow.

### 📩 Project Contact {#envelope_with_arrow-project-contact}

For project-related technical discussions, refer to the **Smart Event
Management --- Team A** repository and the assigned module owners.

------------------------------------------------------------------------

## 📜 License {#scroll-license}

This project is developed as an academic/team project. Refer to the
repository `LICENSE` file for the applicable license terms.

------------------------------------------------------------------------
