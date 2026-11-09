# All-round AI Engineer Roadmap
## Practical, Project-First Learning Plan (6–8 Months)

**Goal:** Become an all-round AI Engineer who can build LLM applications, RAG systems, autonomous agents, fine-tune models, and deploy reliable AI systems to production.

**Learning style:** 30% course/theory, 70% coding, experiments, and projects.  
**Suggested pace:** 8–10 hours per week.  
**Background assumed:** Backend development, Java/Spring Boot, Docker, Kubernetes, Jenkins, PostgreSQL, and Linux.

---

## 1. Target capabilities

By the end of this roadmap, aim to be able to:

- [ ] Use proprietary and open-source LLMs through APIs and local inference.
- [ ] Build LLM applications with structured outputs, tool calling, and streaming.
- [ ] Build RAG pipelines with embeddings and vector databases.
- [ ] Design agents with tools, memory, state, and multi-step workflows.
- [ ] Build and expose MCP servers and clients.
- [ ] Fine-tune small open models using LoRA/QLoRA.
- [ ] Evaluate model and agent quality systematically.
- [ ] Deploy, monitor, secure, and optimize AI applications in production.
- [ ] Integrate Python AI services with Java/Spring Boot systems.

## 2. Recommended Udemy courses

Course titles and availability can change. Check the current syllabus, update date, instructor, reviews, and sale price before purchasing.

| Priority | Course | Purpose | Decision |
|---:|---|---|---|
| 1 | [AI Engineer Core Track: LLM Engineering, RAG, QLoRA, Agents](https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models) | LLM fundamentals, RAG, embeddings, fine-tuning, AI applications | Core |
| 2 | [AI Engineer Agentic Track: The Complete Agent & MCP Course](https://www.udemy.com/course/the-complete-agentic-ai-engineering-course) | Agent loops, tools, MCP, orchestration, multi-agent systems | Core |
| 3 | [AI Engineer Production Track: Deploy LLMs & Agents at Scale](https://www.udemy.com/course/generative-and-agentic-ai-in-production) | Cloud deployment, AWS Bedrock/SageMaker, Terraform, CI/CD, MCP deployment, multi-agent production systems | Core |
| 4 | [AI FDE: The Forward Deployed Engineer & Agentic AI Architect](https://www.udemy.com/course/ai-fde-forward-deployed-engineer-agentic-ai-architect) | Agent architecture, harnesses, durable execution, evaluations, security | Core |
| 5 | [PyTorch for Deep Learning Bootcamp](https://www.udemy.com/course/pytorch-for-deep-learning) | Tensors, neural networks, training loops, model evaluation | Supplement |
| 6 | [LLM Production Engineering: Ship AI Apps That Scale](https://www.udemy.com/course/llm-production-engineering-ship-ai-apps-that-scale) | Reliability, latency, cost, observability, production practices | Optional |

> **Important:** Udemy course slugs and curricula can change. If a link does not resolve, search the exact course title on Udemy. Do not buy based on title alone; inspect the current curriculum first.

### Purchase strategy

Do not buy everything immediately.

1. Start with AI Engineer Core Track.
2. Buy Agentic Track when ready to begin agent projects.
3. Buy AI Engineer Production Track after you can build basic agents; use it to learn cloud deployment and AI platform engineering.
4. Buy AI FDE after that to deepen agent harnesses, durable execution, evaluation, and security.
5. Take selected PyTorch sections when entering model engineering.
6. Treat LLM Production Engineering as targeted supplements.

---

## 3. Roadmap overview

| Phase | Timeline | Main focus | Main deliverable |
|---|---|---|---|
| 1 | Months 1–2 | AI & LLM Engineering | Enterprise Knowledge Assistant |
| 2 | Month 3 | Agent Engineering | Autonomous IT Support Agent |
| 3 | Months 4–5 | Model Engineering | Fine-tuned Domain Model |
| 4 | Month 6 | AI Platform & Cloud Deployment | Deployed AI applications and agents |
| 5 | Month 7 | AI Architecture & Reliability | Production-grade Agent Platform |
| 6 | Months 8–9 | Production Integration & Hardening | Enterprise AI Platform |

The timeline is an estimate. Extend a phase if the project does not meet its exit criteria.

---

## 4. Detailed learning phases

## Phase 1 — AI & LLM Engineering
**Timeline:** Months 1–2  
**Main course:** AI Engineer Core Track

### Learn

- [ ] LLM concepts: tokens, context windows, inference, temperature, sampling.
- [ ] Transformer architecture at a practical conceptual level.
- [ ] Prompt engineering and structured outputs.
- [ ] Calling hosted LLM APIs.
- [ ] Open-source models and Hugging Face basics.
- [ ] Local inference with Ollama.
- [ ] Embeddings and semantic search.
- [ ] Vector databases: Qdrant or PostgreSQL pgvector.
- [ ] RAG ingestion, retrieval, reranking, and citations.
- [ ] Basic model evaluation and hallucination checks.

### Project 1 — Enterprise Knowledge Assistant

Build an assistant that can answer questions from internal documentation.

**Minimum features**

- [ ] Upload PDF, Markdown, and text documents.
- [ ] Parse, chunk, and index documents.
- [ ] Generate embeddings and store them in Qdrant or pgvector.
- [ ] Retrieve relevant passages for each question.
- [ ] Answer with source citations.
- [ ] Say when the knowledge base does not contain the answer.
- [ ] Expose a REST API.
- [ ] Add a basic evaluation dataset.

**Suggested stack**

- Python + FastAPI
- Hosted LLM API initially
- Hugging Face embeddings
- Qdrant or PostgreSQL pgvector
- Docker Compose

**Exit criteria**

A user can upload documents, ask questions, receive grounded answers with citations, and get a clear refusal when evidence is insufficient.

---

## Phase 2 — Agent Engineering
**Timeline:** Month 3  
**Main course:** AI Engineer Agentic Track

### Learn

- [ ] Agent loop: observe → decide → act → observe.
- [ ] Tool/function calling and tool schemas.
- [ ] State, memory, and context management.
- [ ] Planning and task decomposition.
- [ ] LangGraph workflows and checkpoints.
- [ ] MCP server/client concepts.
- [ ] Multi-agent patterns and their trade-offs.
- [ ] Human approval and escalation.
- [ ] Tool error handling and bounded retries.

### Project 2 — Autonomous IT Support Agent

Build on the IT Support/Hermes direction: a Slack-facing agent that can diagnose issues and perform approved operational actions.

**Minimum features**

- [ ] Receive requests through Slack.
- [ ] Classify and clarify user intent.
- [ ] Search internal IT documentation using the Phase 1 RAG system.
- [ ] Expose read-only tools first: Kubernetes status, pod list, logs, service health.
- [ ] Plan actions and explain intended changes.
- [ ] Require approval for risky or destructive operations.
- [ ] Execute approved actions through narrowly scoped tools.
- [ ] Verify the result after execution.
- [ ] Send a report containing actions, results, and failures.
- [ ] Record an audit trail.

**Suggested stack**

- Python + FastAPI
- LangGraph
- MCP
- Slack API
- Kubernetes API with least-privilege service account
- PostgreSQL for state/audit records

**Safety rule**

Start with read-only tools. Add write actions only after permission checks, approval gates, scoped credentials, and audit logging are implemented. Never give an agent unrestricted shell or cluster-admin access.

**Exit criteria**

The agent can complete a bounded IT support workflow, use tools correctly, ask for approval when needed, verify outcomes, and produce an auditable report.

---

## Phase 3 — Model Engineering
**Timeline:** Months 4–5  
**Main course:** Selected sections of PyTorch for Deep Learning Bootcamp, plus the fine-tuning sections in Core Track.

### Learn

Prioritize practical sections; do not feel obligated to watch every computer-vision lesson.

- [ ] Python tensor operations with PyTorch.
- [ ] Autograd and gradients.
- [ ] Neural network building blocks.
- [ ] Loss functions and optimizers.
- [ ] Training, validation, and test loops.
- [ ] Overfitting, regularization, and data leakage.
- [ ] Model evaluation and experiment tracking.
- [ ] Hugging Face Transformers and datasets.
- [ ] Fine-tuning with LoRA/QLoRA.
- [ ] Quantization and inference trade-offs.

### Project 3 — Fine-tuned Domain Model

Fine-tune a small open model for a narrow domain task, such as IT ticket classification or structured incident summarization.

**Minimum features**

- [ ] Define a narrow task and success metric.
- [ ] Build and clean a dataset.
- [ ] Split train/validation/test data correctly.
- [ ] Establish a base-model baseline.
- [ ] Fine-tune using LoRA/QLoRA.
- [ ] Compare base and fine-tuned model on held-out examples.
- [ ] Record quality, latency, and resource usage.
- [ ] Document limitations and failure cases.

**Hardware strategy**

- Use free/low-cost hosted GPU notebooks when available.
- Use CPU VPS for API development, data preparation, and small inference experiments.
- Avoid buying a GPU before measuring actual requirements.

**Exit criteria**

You can explain the dataset, training configuration, evaluation method, and measurable difference between the base model and fine-tuned model.

> Fine-tuning is not the same as training a foundation model from scratch. Training a competitive general-purpose LLM requires much larger datasets, compute, and engineering resources.

---

## Phase 4 — AI Architecture & Reliability
**Timeline:** Month 6  
**Main course:** AI FDE: The Forward Deployed Engineer & Agentic AI Architect

### Learn

- [ ] Agent harness design and execution boundaries.
- [ ] Durable execution and checkpointing.
- [ ] Recovery after process or tool failures.
- [ ] Human-in-the-loop workflows.
- [ ] Agent evaluation and regression testing.
- [ ] Tracing and observability with tools such as Langfuse.
- [ ] Prompt injection and tool security.
- [ ] Permissions, secrets, and auditability.
- [ ] MCP gateway and enterprise integration patterns.
- [ ] Cost, latency, and reliability trade-offs.

### Project 5 — Production-grade Agent Platform

Upgrade Project 2 rather than starting a disconnected project.

**Minimum features**

- [ ] Durable workflow state.
- [ ] Idempotency for repeatable operations.
- [ ] Timeouts, bounded retries, and failure handling.
- [ ] Model fallback strategy.
- [ ] Role-based tool permissions.
- [ ] Approval gates for sensitive operations.
- [ ] Trace each agent run and tool call.
- [ ] Maintain evaluation datasets and regression tests.
- [ ] Audit every state-changing action.
- [ ] Test interruption and recovery.

**Exit criteria**

A failed run can be diagnosed, safely retried or resumed, and evaluated. Risky actions are controlled by explicit permissions and approvals.

---

## Phase 6 — Production Integration & Hardening
**Timeline:** Months 8–9  
**Main courses:** Spring AI Masterclass and selected LLM Production Engineering sections.

### Learn

- [ ] Integrate LLM capabilities into Spring Boot.
- [ ] Design boundaries between Java business services and Python AI services.
- [ ] REST APIs, streaming, and asynchronous processing.
- [ ] Docker image optimization.
- [ ] Kubernetes deployment and resource limits.
- [ ] CI/CD and automated tests.
- [ ] Metrics, logs, traces, and alerting.
- [ ] Latency, throughput, and token-cost optimization.
- [ ] Caching, rate limiting, and backpressure.
- [ ] Secrets management and network security.

### Project 6 — Enterprise AI Platform

Combine the previous projects into one coherent platform.

**Suggested architecture**

```text
Slack / Web UI / REST Clients
            |
       AI Gateway
  Auth / Rate Limit / Routing
            |
      Orchestration Layer
   Agent Runtime / Workflows
       /       |       \
     RAG     Tools    Model Router
      |        |          |
 Vector DB  MCP/API   Hosted / Local LLM
       \       |       /
        Evaluation & Audit
                |
       Observability Stack
                |
       Docker / Kubernetes
```

**Minimum deliverables**

- [ ] Authentication and authorization.
- [ ] Model routing and fallback.
- [ ] RAG and agent workflows.
- [ ] MCP/tool integrations.
- [ ] Evaluation and regression tests.
- [ ] Observability and audit trail.
- [ ] CI/CD deployment pipeline.
- [ ] Documentation and architecture diagram.
- [ ] Load, latency, and failure testing.
- [ ] Cost and operational runbook.

**Exit criteria**

A reproducible deployment can serve users, enforce permissions, expose operational metrics, and recover from expected failures.

---

## 5. Recommended technology stack

| Area | Recommended tools |
|---|---|
| Main AI language | Python |
| Existing backend integration | Java + Spring Boot |
| AI API | FastAPI |
| LLM access | Hosted model APIs, Hugging Face |
| Local inference | Ollama initially |
| Deep learning | PyTorch |
| Model ecosystem | Hugging Face Transformers, Datasets, PEFT |
| Agent orchestration | LangGraph |
| Agent/tool interoperability | MCP |
| RAG | Qdrant or PostgreSQL pgvector |
| Cache and queues | Redis; add a message broker when needed |
| Observability | Langfuse, OpenTelemetry, Prometheus/Grafana |
| Packaging | Docker |
| Deployment | Kubernetes |
| CI/CD | Jenkins or GitHub Actions |
| Secrets | Vault or an appropriate cloud secret manager |

Do not learn every framework at once. Pick one primary implementation for each problem, then compare alternatives only when you have a concrete reason.

---

## 6. Weekly learning schedule

Suggested allocation for 8–10 hours per week:

| Activity | Hours/week |
|---|---:|
| Course and theory | 2 |
| Coding and experiments | 5 |
| Project and documentation | 2 |
| Evaluation and review | 1 |
| **Total** | **10** |

A practical weekly rhythm:

- **Session 1:** Watch a lesson and write concise notes.
- **Session 2:** Reproduce the lesson without copying blindly.
- **Session 3:** Add the concept to the current project.
- **Session 4:** Test edge cases, measure results, and document what changed.

---

## 7. Evaluation checklist

Do not measure progress by video completion alone.

For each project, track:

### Functionality
- [ ] Core user workflow works end-to-end.
- [ ] Invalid inputs and missing context are handled.
- [ ] Errors are visible and actionable.

### Quality
- [ ] A small representative evaluation dataset exists.
- [ ] Results are measured against a baseline.
- [ ] Regressions are tested after prompt/model/tool changes.

### Reliability
- [ ] Timeouts and bounded retries exist.
- [ ] Duplicate operations are handled safely.
- [ ] Failure and recovery paths are tested.

### Security
- [ ] Tools have least-privilege access.
- [ ] Secrets are not embedded in prompts or source code.
- [ ] State-changing actions have authorization and audit logs.
- [ ] Prompt injection and untrusted tool output are considered.

### Operations
- [ ] Logs, metrics, and traces are available.
- [ ] Latency and token usage are measured.
- [ ] Deployment is reproducible.
- [ ] A runbook explains common failures.

---

## 8. Budget and hardware strategy

Keep costs low while learning.

1. Use existing laptop/PC for coding and Docker-based development.
2. Use hosted LLM APIs with strict spending limits for early projects.
3. Use Ollama and small quantized models for local experiments if hardware permits.
4. Use free GPU notebook quotas when available for PyTorch and LoRA/QLoRA experiments.
5. Use a CPU VPS for APIs, databases, orchestration, and lightweight inference.
6. Rent GPU compute temporarily only after identifying a workload that needs it.

Do not purchase a GPU or large server just to follow a course. Measure memory, throughput, and latency requirements first.

---

## 9. What to postpone

To avoid spreading effort too thin, postpone these until the core projects work:

- Training a general-purpose LLM from scratch.
- Learning multiple agent frameworks in parallel.
- Building complex multi-agent systems without a clear need.
- Premature Kubernetes scaling and GPU infrastructure.
- Fine-tuning before establishing a baseline and evaluation dataset.
- Collecting certificates without shipping working projects.

---

## 10. Final portfolio target

At the end of the roadmap, aim to have:

1. **Enterprise Knowledge Assistant** — grounded RAG with citations and evaluation.
2. **Autonomous IT Support Agent** — Slack, tools, MCP, and controlled execution.
3. **Fine-tuned Domain Model** — reproducible LoRA/QLoRA experiment with comparison.
4. **Production-grade Agent Platform** — durable execution, security, evals, and observability.
5. **Enterprise AI Platform** — integrated Java/Python services deployed through Docker/Kubernetes.

The strongest outcome is not five certificates. It is one coherent, documented platform that demonstrates the ability to build, evaluate, secure, deploy, and operate AI systems.

---

## Progress tracker

- [ ] Phase 1 — AI & LLM Engineering
- [ ] Project 1 — Enterprise Knowledge Assistant
- [ ] Phase 2 — Agent Engineering
- [ ] Project 2 — Autonomous IT Support Agent
- [ ] Phase 3 — Model Engineering
- [ ] Project 3 — Fine-tuned Domain Model
- [ ] Phase 4 — AI Platform & Cloud Deployment
- [ ] Project 4 — Deploy the AI Support Agent
- [ ] Phase 5 — AI Architecture & Reliability
- [ ] Project 5 — Production-grade Agent Platform
- [ ] Phase 6 — Production Integration & Hardening
- [ ] Project 6 — Enterprise AI Platform

**Guiding principle:** 30% learning, 70% building. Learn a concept, implement it, evaluate it, and integrate it into the platform.
