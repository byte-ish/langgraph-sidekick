# **LangGraph Sidekick**
> **LangGraph Sidekick** is a multi-agent AI assistant built with **LangGraph**, **LangChain**, **Playwright**, and **Gradio**.  
> It collaborates with users to complete tasks, evaluates responses against success criteria, and provides structured feedback in a continuous loop until the criteria are met or user clarification is required.

---

## **Features**
- **Multi-Agent Orchestration**  
  - **Worker Agent**: Executes tasks using ChatGPT and browser automation tools.  
  - **Evaluator Agent**: Validates results against user-defined success criteria with structured feedback.  
- **Tool Integration**  
  - Equipped with **Playwright** for web browsing and automated actions.  
- **Structured Outputs**  
  - Evaluator produces consistent, machine-readable feedback using **Pydantic models**.  
- **Stateful Execution**  
  - **LangGraph** maintains state (messages, feedback, criteria) across iterative steps.  
- **Interactive Chat Interface**  
  - Powered by **Gradio**, enabling an easy-to-use, real-time conversational interface.

---

## **Architecture**
### **Flow Diagram**
```mermaid
flowchart TD
    subgraph User["👤 User"]
        UI["Gradio UI"]
    end

    subgraph LangGraph["LangGraph Orchestrator"]
        Start[START]
        Worker["Worker Node (ChatOpenAI + Tools)"]
        Router["Worker Router"]
        Tools["ToolNode (Playwright Toolkit)"]
        Evaluator["Evaluator Node (ChatOpenAI + Structured Output)"]
        End[END]
    end

    subgraph State["Shared State"]
        Messages["messages[]"]
        Criteria["success_criteria"]
        Feedback["feedback_on_work"]
        Flags["success_criteria_met / user_input_needed"]
    end

    %% User interaction
    UI -->|Input: Request & Success Criteria| Start

    %% LangGraph flow
    Start --> Worker
    Worker --> Router
    Router -->|Tool Calls Present| Tools
    Router -->|No Tool Calls| Evaluator
    Tools --> Worker
    Evaluator -->|Criteria Met OR Needs User Input| End
    Evaluator -->|Criteria NOT Met| Worker

    %% State
    Worker -->|Updates| State
    Tools -->|Updates| State
    Evaluator -->|Updates| State

    %% Output
    End -->|Assistant Response + Evaluator Feedback| UI
```
### **Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User (Gradio UI)
    participant G as LangGraph Orchestrator
    participant W as Worker Node (ChatOpenAI + Tools)
    participant R as Router
    participant T as ToolNode (Playwright)
    participant E as Evaluator Node (ChatOpenAI)
    participant S as State (MemorySaver)

    U->>G: Submit task + success criteria
    G->>S: Initialize state (messages, criteria, flags)
    G->>W: Invoke Worker with current state
    W->>S: Update messages with Worker response
    W->>R: Pass response for routing decision

    alt Tool Calls Present
        R->>T: Execute ToolNode (Playwright action)
        T->>S: Update state with tool results
        T->>W: Return control to Worker
    else No Tool Calls
        R->>E: Invoke Evaluator with conversation + criteria
        E->>S: Update state (feedback, flags)
        alt Success criteria met OR user input needed
            E->>G: Return Assistant Response + Evaluator Feedback
        else Criteria not met
            E->>W: Loop back to Worker for another attempt
        end
    end

    G->>U: Display response & feedback in chat
```
### Project Structure
```
langgraph-sidekick/
│
├── app/
│   ├── __init__.py
│   ├── state.py             # State & Pydantic models
│   ├── worker.py            # Worker node (task execution)
│   ├── evaluator.py         # Evaluator node (feedback & validation)
│   ├── router.py            # Routing logic
│   ├── tools.py             # Playwright browser toolkit setup
│   ├── graph_builder.py     # LangGraph orchestration setup
│
├── ui/
│   ├── __init__.py
│   ├── gradio_app.py        # Gradio chat interface
│
├── main.py                  # Entry point to launch the app
├── .env                     # Environment variables (e.g., OpenAI key)
├── requirements.txt         # Project dependencies
└── README.md                # Project overview & documentation
```
<img width="1017" height="726" alt="image" src="https://github.com/user-attachments/assets/62e8af49-1d02-4405-90fa-124392502548" />
<img width="899" height="1081" alt="image" src="https://github.com/user-attachments/assets/693fb21b-a1b7-4f16-84d3-88fbb326b4eb" />



