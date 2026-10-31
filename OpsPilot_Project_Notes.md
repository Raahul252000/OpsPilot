# OpsPilot — AI Incident Investigation & Resolution Assistant

## 1. Project Overview

**OpsPilot** is an AI-powered incident investigation and resolution assistant for software engineering / DevOps teams.

The goal is to help engineers investigate production incidents by:

- Understanding the incident
- Searching company knowledge and runbooks
- Analyzing application logs
- Checking metrics and service health
- Checking recent deployments
- Investigating databases when required
- Identifying a likely root cause
- Recommending remediation
- Asking for human approval before risky actions
- Applying approved remediation
- Verifying whether the incident is resolved
- Producing a final incident report

### Example Incident

> Payment service is returning 500 errors after the latest deployment.

Normally, an engineer may need to:

1. Check application logs
2. Check metrics
3. Check recent deployments
4. Search runbooks/documentation
5. Check database health
6. Determine the likely root cause
7. Decide how to fix it
8. Apply the fix
9. Verify the problem is resolved
10. Write an incident report

OpsPilot aims to assist with this workflow.

---

# 2. What Is an Incident?

An **incident** is a record describing a production problem.

Example:

```text
Incident
────────────────────────────────
Title:
Payment service returning 500

Service:
payment-service

Description:
Payment API started returning 500 errors
after the latest deployment.

Status:
Open
```

The incident becomes the starting point for the AI investigation.

---

# 3. What Is the Incident API?

The **Incident API** is the entry point through which a user or another system sends an incident to OpsPilot.

Example:

```text
POST /incidents
```

Conceptually:

```text
Engineer / Monitoring System
            │
            │ POST /incidents
            ▼
        OpsPilot
```

The Incident API does **not** investigate the problem itself.

Its responsibility is to receive the incident information and pass it into the application.

Later, the application can expose APIs such as:

```text
POST /incidents
        → create incident

POST /incidents/{id}/investigate
        → start AI investigation

GET /incidents/{id}
        → get incident details

GET /incidents/{id}/timeline
        → see investigation timeline

GET /incidents/{id}/report
        → get final RCA report
```

---

# 4. Overall Project Flow

The complete high-level flow is:

```text
                     USER
                      │
                      ▼
               Create Incident
                      │
                      ▼
              ┌───────────────┐
              │   OpsPilot    │
              └───────┬───────┘
                      │
                      ▼
               Understand Issue
                      │
                      ▼
             Investigate Incident
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Knowledge     Logs       Metrics
         Base
          │           │           │
          └───────────┼───────────┘
                      ▼
                 Analyze Evidence
                      │
                      ▼
                 Find Root Cause
                      │
                      ▼
              Recommend Solution
                      │
                      ▼
              Human Approval
                      │
                      ▼
               Apply Fix
                      │
                      ▼
             Verify Resolution
                      │
                      ▼
                Final Report
```

---

# 5. Project Components

## 5.1 FastAPI — The Front Door

FastAPI is the backend API layer.

It allows users and external systems to communicate with OpsPilot.

Examples:

```text
POST /incidents
POST /incidents/{id}/investigate
GET  /incidents/{id}
GET  /incidents/{id}/report
```

### Mental model

> **FastAPI = the front door / receptionist of OpsPilot.**

It receives requests and returns responses.

FastAPI itself is not the AI.

---

# 6. Incident Service — Application Logic

The Incident Service contains normal application/business logic.

Examples:

```text
Create incident
Update incident
Change incident status
Start investigation
Store investigation result
```

We keep this logic outside the API route.

Conceptually:

```text
API Layer
    ↓
Incident Service
```

Later, the service will interact with:

```text
Database
RAG
LLM
Tools
Agents
```

### Mental model

> **Service layer = normal business/application logic.**

---

# 7. PostgreSQL — Permanent Storage

OpsPilot needs permanent storage for incidents and investigation results.

Example:

```text
incidents
────────────────────────
id
title
description
service
status
created_at
```

Eventually:

```text
investigations
────────────────────────
id
incident_id
root_cause
recommendation
created_at
```

### Mental model

> **PostgreSQL = permanent database for OpsPilot.**

It stores important application data and investigation history.

---

# 8. Knowledge Base and RAG

The company can have documents such as:

```text
payment-service-runbook.pdf

database-troubleshooting.pdf

deployment-guide.pdf

redis-troubleshooting.pdf

incident-response-guide.pdf
```

The LLM should not be expected to know the contents of these private/company documents automatically.

Instead, we build a RAG pipeline.

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
```

When an incident occurs:

```text
Incident:
"Payment API returning 500"

        ↓

Search Knowledge Base

        ↓

Relevant document chunks
```

Example retrieved information:

```text
"Payment service commonly returns 500
when the database connection pool is exhausted..."
```

### Mental model

> **RAG = give the AI access to relevant company knowledge.**

---

# 9. Chroma — Semantic Knowledge Storage

Chroma will be used as the vector store for the knowledge base.

The ingestion flow is:

```text
Document
   ↓
Chunks
   ↓
Embedding Model
   ↓
Vectors
   ↓
Chroma
```

When OpsPilot needs information, Chroma can help retrieve semantically relevant chunks.

### Mental model

> **Chroma = searchable semantic storage for the knowledge base.**

---

# 10. LLM — Understanding and Reasoning Engine

OpsPilot needs an LLM such as a supported provider/model.

The LLM can receive:

```text
Incident
+
Relevant documentation
+
Logs
+
Metrics
+
Deployment information
```

and produce an analysis such as:

```text
Likely root cause:
Database connection pool exhaustion.

Evidence:
1. Error rate increased immediately after deployment.
2. Logs show connection timeout errors.
3. Deployment changed DB connection configuration.

Recommended action:
Increase connection pool size and verify DB capacity.
```

### Mental model

> **LLM = language understanding and reasoning engine.**

However, the LLM does not automatically have access to our systems.

That is the purpose of tools.

---

# 11. Tools — The AI's Hands

A tool is a controlled function that allows the AI application to access information or perform an operation.

For example:

```python
get_recent_logs(service, minutes)
```

Other possible tools:

```text
get_error_rate()
get_latency()
get_service_health()
get_recent_deployments()
get_db_connection_usage()
get_slow_queries()
```

Conceptually:

```text
LLM / Agent
 │
 ├── get_recent_logs()
 ├── get_error_rate()
 ├── get_recent_deployments()
 ├── get_db_connection_usage()
 └── get_service_health()
```

### Mental model

> **Tools = capabilities that give the AI controlled access to external systems.**

Initially, we should focus on read-only tools.

Later, controlled remediation tools can be added.

---

# 12. Agent — The Decision Maker

An agent becomes useful when the AI needs to decide which information or tool it needs.

For example, for:

> Payment API is returning 500.

The agent might decide:

```text
1. Search documentation
2. Check logs
3. Check recent deployments
4. Check database health
5. Analyze the evidence
```

Conceptually:

```text
                Incident
                   │
                   ▼
                 Agent
                   │
          "I need more information"
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      RAG         Logs      Deployments
       │            │           │
       └────────────┼───────────┘
                    ▼
                  Agent
                    │
              "I have enough
                evidence"
                    │
                    ▼
               Final Analysis
```

### Mental model

> **Agent = AI that can decide which tools/information it needs to accomplish a goal.**

This is different from a fixed pipeline where every step is predetermined.

---

# 13. Redis — Temporary State and Cache

An investigation can involve multiple steps.

Example:

```text
User:
"Investigate payment-service."

AI:
"Checking recent logs..."

AI:
"Logs show DB connection errors."

User:
"What happened after deployment?"

AI:
"The deployment changed the DB configuration..."
```

The system needs to maintain relevant short-lived investigation/conversation state.

Redis can be used for:

```text
Conversation state
Temporary investigation state
Caching
Short-lived data
```

### Redis vs PostgreSQL

```text
Redis
    → fast / temporary state / cache

PostgreSQL
    → persistent application data
```

---

# 14. Human Approval

OpsPilot should not blindly execute potentially dangerous production actions.

For example, the AI may conclude:

> Rollback deployment.

Instead of immediately executing it:

```text
AI
 │
 ▼
"Rollback deployment recommended"
 │
 ▼
Human approval required
 │
 ├── Approve
 │      ↓
 │   Execute
 │
 └── Reject
        ↓
     Don't execute
```

This gives humans control over risky actions.

Initially, remediation tools should be limited and controlled.

---

# 15. Verification

After performing a remediation action, OpsPilot should verify whether the problem is actually resolved.

Example:

```text
Restart service
       ↓
Check service health
       ↓
Check error rate
       ↓
Check latency
       ↓
Is incident resolved?
```

If resolved:

```text
Resolved
```

Otherwise:

```text
Continue investigation
```

This type of multi-step stateful workflow is one reason we will later study LangGraph.

---

# 16. Where LangChain Fits

LangChain is used primarily for the AI/application layer.

The project is not simply:

> "Use LangChain because it is popular."

Instead, the architecture is:

```text
                 OpsPilot
                    │
        ┌───────────┴───────────┐
        │                       │
    Normal Backend           AI Layer
        │                       │
     FastAPI                LangChain
     PostgreSQL                 │
     Redis                 ┌────┼─────┐
                           │    │     │
                          RAG Tools Agents
                           │    │     │
                           └────┼─────┘
                                │
                               LLM
```

LangChain helps us compose and manage the AI-related pieces.

---

# 17. Where LCEL Fits

LCEL (LangChain Expression Language) is useful for **deterministic AI pipelines**.

For example, our RAG pipeline:

```text
Question
   ↓
Retriever
   ↓
Relevant Documents
   ↓
Prompt
   ↓
LLM
   ↓
Parser
   ↓
Answer
```

LCEL can connect these components into a pipeline.

Conceptually:

```text
Retriever → Prompt → LLM → Parser
```

### LCEL vs Agent

```text
LCEL
 ↓
Good for known, deterministic steps

Agent
 ↓
Good when the AI needs to decide
which tool/action to use
```

---

# 18. Complete OpsPilot Architecture

Eventually, the project will look approximately like:

```text
                         USER
                           │
                           ▼
                     ┌───────────┐
                     │  FastAPI  │
                     └─────┬─────┘
                           │
                           ▼
                    Incident Service
                           │
                           ▼
                    AI Investigation
                           │
                    ┌──────┴──────┐
                    │             │
                LangChain       Redis
                    │
          ┌─────────┼─────────┐
          │         │         │
         RAG      Agent      LLM
          │         │
       Chroma       │
                    │
            ┌───────┼──────────┐
            │       │          │
           Logs   Metrics   Deployments
           Tool    Tool        Tool
            │       │          │
            └───────┼──────────┘
                    │
                    ▼
               Investigation
                    │
                    ▼
              Root Cause Analysis
                    │
                    ▼
              Recommendation
                    │
                    ▼
              Human Approval
                    │
                    ▼
               Remediation
                    │
                    ▼
                Verification
                    │
                    ▼
               Final Report
                    │
                    ▼
                PostgreSQL
```

---

# 19. Component Cheat Sheet

| Component | Purpose |
|---|---|
| **FastAPI** | Communicate with OpsPilot through APIs |
| **Incident Service** | Application/business logic |
| **PostgreSQL** | Store incidents and results permanently |
| **Redis** | Temporary state and caching |
| **LLM** | Understand and reason over information |
| **LangChain** | Build and compose the AI application |
| **RAG** | Give the AI relevant company knowledge |
| **Chroma** | Store/search knowledge embeddings |
| **Tools** | Give the AI controlled access to systems |
| **Agent** | Decide which tools/information to use |
| **LCEL** | Connect known/deterministic AI steps |
| **Human Approval** | Prevent unsafe autonomous actions |
| **Verification** | Confirm whether remediation solved the incident |
| **LangGraph (later)** | Manage complex/stateful workflows |

---

# 20. The Core Story to Remember

The entire project can be remembered as:

> **An incident enters OpsPilot → the AI investigates it → RAG gives it company knowledge → tools give it access to real system information → the agent decides what information/tools it needs → the LLM analyzes the evidence → OpsPilot recommends a fix → a human can approve risky actions → the system verifies the result → everything is recorded.**

---

# 21. Learning Path Through the Project

We will learn the remaining concepts while implementing the project.

```text
FastAPI
   ↓
Incident
   ↓
LLM
   ↓
Prompt
   ↓
LCEL
   ↓
Output Parser
   ↓
RAG
   ↓
Tools
   ↓
Tool Calling
   ↓
Agent
   ↓
Memory
   ↓
Human Approval
   ↓
LangGraph
```

The important principle is:

> **We will learn each technology when the project actually needs it, instead of learning the entire LangChain ecosystem theoretically first.**
