# 🏗️ AuroraSync OS - Architecture Diagrams

This document contains visual diagrams for presentations and documentation.

---

## 1. High-Level System Architecture

```mermaid
graph TB
    subgraph "Vehicle Layer"
        V1[Vehicle 001]
        V2[Vehicle 002]
        V3[Vehicle 003]
        V4[Vehicle 004-010]
    end
    
    subgraph "Data Ingestion"
        MQTT[Telematics Stream<br/>Every 5 seconds]
        HIST[Historical Database<br/>6 months data]
    end
    
    subgraph "Master Agent Orchestrator"
        MA[Master Agent<br/>Task Queue & Routing]
    end
    
    subgraph "Worker Agents"
        WA1[Data Analysis<br/>Feature Extraction]
        WA2[Diagnosis<br/>ML Prediction]
        WA3[Customer Engagement<br/>Voice AI]
        WA4[Scheduling<br/>Workshop Booking]
        WA5[Feedback<br/>Validation]
        WA6[Manufacturing<br/>RCA/CAPA]
        WA7[UEBA<br/>Security Monitor]
    end
    
    subgraph "ML Pipeline"
        ML1[Failure Predictor<br/>RF + XGBoost]
        ML2[Anomaly Detector<br/>Isolation Forest]
        ML3[Demand Forecaster<br/>Prophet]
    end
    
    subgraph "External Systems"
        TTS[Voice AI<br/>ElevenLabs TTS]
        WS[Workshop API<br/>Booking System]
        MFG[Manufacturing<br/>OEM System]
    end
    
    subgraph "Presentation Layer"
        UI[React Dashboard<br/>Dark Mode UI]
    end
    
    V1 --> MQTT
    V2 --> MQTT
    V3 --> MQTT
    V4 --> MQTT
    MQTT --> MA
    HIST --> MA
    
    MA --> WA1
    MA --> WA2
    MA --> WA3
    MA --> WA4
    MA --> WA5
    MA --> WA6
    
    WA1 --> ML2
    WA1 --> WA2
    WA2 --> ML1
    WA2 --> WA3
    WA3 --> TTS
    WA3 --> WA4
    WA4 --> ML3
    WA4 --> WS
    WA4 --> WA5
    WA5 --> WA6
    WA6 --> MFG
    
    WA7 -.Monitor.-> MA
    WA7 -.Monitor.-> WA1
    WA7 -.Monitor.-> WA2
    WA7 -.Monitor.-> WA3
    WA7 -.Monitor.-> WA4
    WA7 -.Monitor.-> WA5
    WA7 -.Monitor.-> WA6
    
    UI <--> MA
    
    style MA fill:#4a9eff,stroke:#333,stroke-width:3px,color:#fff
    style WA7 fill:#ef4444,stroke:#333,stroke-width:2px,color:#fff
    style UI fill:#8b5cf6,stroke:#333,stroke-width:2px,color:#fff
```

---

## 2. Data Flow Sequence

```mermaid
sequenceDiagram
    participant V as Vehicle 003
    participant MA as Master Agent
    participant DA as Data Analysis
    participant DG as Diagnosis
    participant CE as Customer Engagement
    participant SC as Scheduling
    participant FB as Feedback
    participant MI as Manufacturing
    participant UEBA as UEBA Agent
    
    V->>MA: Telematics data (every 5s)
    MA->>DA: Process data
    DA->>DA: Extract 30 features
    DA->>DA: Run anomaly detection
    DA->>MA: Anomaly detected!
    
    MA->>DG: Analyze features
    DG->>DG: Run ML model
    DG->>MA: 85% brake failure in 7 days
    
    MA->>CE: Engage customer
    CE->>CE: Generate script (LLM)
    CE->>CE: Synthesize voice (TTS)
    CE->>V: Voice call
    V->>CE: Customer accepts
    CE->>MA: Acceptance confirmed
    
    MA->>SC: Schedule service
    SC->>SC: Check availability
    SC->>SC: Optimize slot
    SC->>MA: Booked: Dec 10, 10 AM
    
    Note over V: Service completed
    
    V->>MA: Service report
    MA->>FB: Validate prediction
    FB->>FB: Compare predicted vs actual
    FB->>MA: True Positive ✓
    
    MA->>MI: Aggregate feedback
    MI->>MI: Cluster failures
    MI->>MI: Generate RCA/CAPA
    MI->>MA: Report: Supplier defect
    
    UEBA-->>MA: Monitor all actions
    UEBA-->>UEBA: Detect anomalies
    UEBA-->>MA: Alert if suspicious
```

---

## 3. Agent Communication Architecture

```mermaid
graph LR
    subgraph "Message Bus (Redis Pub/Sub)"
        CH1[telematics.raw]
        CH2[tasks.data_analysis]
        CH3[tasks.diagnosis]
        CH4[tasks.customer]
        CH5[tasks.scheduling]
        CH6[tasks.feedback]
        CH7[tasks.manufacturing]
        CH8[events.all]
    end
    
    MA[Master Agent] -->|publish| CH2
    MA -->|publish| CH3
    MA -->|publish| CH4
    MA -->|publish| CH5
    MA -->|publish| CH6
    MA -->|publish| CH7
    
    CH1 -->|subscribe| MA
    CH2 -->|subscribe| DA[Data Analysis]
    CH3 -->|subscribe| DG[Diagnosis]
    CH4 -->|subscribe| CE[Customer Engagement]
    CH5 -->|subscribe| SC[Scheduling]
    CH6 -->|subscribe| FB[Feedback]
    CH7 -->|subscribe| MI[Manufacturing]
    CH8 -->|subscribe| UEBA[UEBA Agent]
    
    DA -->|publish| CH8
    DG -->|publish| CH8
    CE -->|publish| CH8
    SC -->|publish| CH8
    FB -->|publish| CH8
    MI -->|publish| CH8
    
    style MA fill:#4a9eff,stroke:#333,stroke-width:3px
    style UEBA fill:#ef4444,stroke:#333,stroke-width:2px
```

---

## 4. ML Pipeline Architecture

```mermaid
graph TB
    subgraph "Data Generation"
        GEN1[Vehicle Generator]
        GEN2[Telematics Generator]
        GEN3[Failure Injector]
    end
    
    subgraph "Feature Engineering"
        FE1[Raw Features<br/>10 sensors]
        FE2[Derived Features<br/>std, rate of change]
        FE3[Time Features<br/>hour, day, season]
        FE4[Historical Features<br/>7-day avg]
    end
    
    subgraph "Model Training"
        M1[Random Forest<br/>n_estimators=100]
        M2[XGBoost<br/>learning_rate=0.1]
        M3[Ensemble<br/>Average probabilities]
    end
    
    subgraph "Model Evaluation"
        E1[Accuracy: 92%]
        E2[Precision: 85%]
        E3[Recall: 95%]
        E4[F1-Score: 0.90]
    end
    
    subgraph "Deployment"
        D1[Save to .pkl]
        D2[Load in Diagnosis Agent]
        D3[Real-time Prediction]
    end
    
    GEN1 --> GEN2
    GEN2 --> GEN3
    GEN3 --> FE1
    
    FE1 --> FE2
    FE2 --> FE3
    FE3 --> FE4
    
    FE4 --> M1
    FE4 --> M2
    M1 --> M3
    M2 --> M3
    
    M3 --> E1
    M3 --> E2
    M3 --> E3
    M3 --> E4
    
    E1 --> D1
    E2 --> D1
    E3 --> D1
    E4 --> D1
    D1 --> D2
    D2 --> D3
    
    style M3 fill:#10b981,stroke:#333,stroke-width:2px
    style D3 fill:#8b5cf6,stroke:#333,stroke-width:2px
```

---

## 5. UEBA Security Architecture

```mermaid
graph TB
    subgraph "Agent Actions"
        A1[Data Analysis<br/>10 vehicles/min]
        A2[Diagnosis<br/>0.5s latency]
        A3[Customer Engagement<br/>80% acceptance]
        A4[Scheduling<br/>95% success]
    end
    
    subgraph "Logging Layer"
        L1[Action Logger]
        L2[Metrics Collector]
        L3[Event Stream]
    end
    
    subgraph "UEBA Agent"
        U1[Baseline Establishment<br/>30 days normal data]
        U2[Anomaly Detection<br/>Isolation Forest]
        U3[Rule Engine<br/>5 security rules]
        U4[Alert Generator]
    end
    
    subgraph "Response Actions"
        R1[Throttle Activity]
        R2[Alert Admin]
        R3[Restart Agent]
        R4[Trigger Retraining]
    end
    
    A1 --> L1
    A2 --> L1
    A3 --> L1
    A4 --> L1
    
    L1 --> L2
    L2 --> L3
    L3 --> U1
    
    U1 --> U2
    U2 --> U3
    U3 --> U4
    
    U4 -->|If anomaly| R1
    U4 -->|If critical| R2
    U4 -->|If degraded| R3
    U4 -->|If drift| R4
    
    style U2 fill:#ef4444,stroke:#333,stroke-width:3px,color:#fff
    style U4 fill:#f59e0b,stroke:#333,stroke-width:2px
```

---

## 6. Frontend Architecture

```mermaid
graph TB
    subgraph "React Components"
        C1[Dashboard]
        C2[VehicleGrid]
        C3[TelemetryChart]
        C4[PredictionPanel]
        C5[AgentStatus]
        C6[SchedulingView]
        C7[ManufacturingInsights]
        C8[UEBAMonitor]
    end
    
    subgraph "State Management"
        S1[Zustand Store]
        S2[Vehicle State]
        S3[Agent State]
        S4[Prediction State]
    end
    
    subgraph "Services"
        SV1[API Client<br/>Axios]
        SV2[WebSocket Manager]
    end
    
    subgraph "Backend"
        B1[REST API<br/>FastAPI]
        B2[WebSocket<br/>Real-time]
    end
    
    C1 --> C2
    C1 --> C3
    C1 --> C4
    C1 --> C5
    C1 --> C6
    C1 --> C7
    C1 --> C8
    
    C2 --> S1
    C3 --> S1
    C4 --> S1
    C5 --> S1
    
    S1 --> S2
    S1 --> S3
    S1 --> S4
    
    S2 --> SV1
    S3 --> SV1
    S4 --> SV1
    
    SV1 --> B1
    SV2 --> B2
    
    B2 -.Real-time updates.-> C3
    B2 -.Real-time updates.-> C5
    B2 -.Real-time updates.-> C8
    
    style C1 fill:#8b5cf6,stroke:#333,stroke-width:3px,color:#fff
    style SV2 fill:#10b981,stroke:#333,stroke-width:2px
```

---

## 7. Database Schema

```mermaid
erDiagram
    VEHICLES ||--o{ TELEMATICS : generates
    VEHICLES ||--o{ PREDICTIONS : has
    VEHICLES ||--o{ BOOKINGS : schedules
    PREDICTIONS ||--o{ BOOKINGS : triggers
    BOOKINGS ||--o{ FEEDBACK : results_in
    
    VEHICLES {
        string id PK
        string make
        string model
        int year
        int mileage
        string owner_name
        string status
    }
    
    TELEMATICS {
        int id PK
        string vehicle_id FK
        timestamp timestamp
        int rpm
        float engine_temp
        float oil_pressure
        float brake_pad_thickness
        float vibration_level
        jsonb location
    }
    
    PREDICTIONS {
        string id PK
        string vehicle_id FK
        timestamp timestamp
        string component
        float failure_probability
        date predicted_failure_date
        string severity
        float confidence
    }
    
    BOOKINGS {
        string id PK
        string vehicle_id FK
        string workshop_id
        timestamp scheduled_date
        string service_type
        string status
        float estimated_cost
    }
    
    FEEDBACK {
        string id PK
        string booking_id FK
        string prediction_id FK
        bool prediction_correct
        string actual_issue
        float accuracy_score
    }
    
    UEBA_EVENTS {
        string id PK
        string agent
        string metric
        float baseline
        float observed
        float anomaly_score
        string severity
        timestamp timestamp
    }
```

---

## 8. Deployment Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Browser]
        MOB[Mobile App]
    end
    
    subgraph "Load Balancer"
        LB[Nginx/ALB]
    end
    
    subgraph "Application Layer"
        API1[FastAPI Instance 1]
        API2[FastAPI Instance 2]
        API3[FastAPI Instance 3]
    end
    
    subgraph "Agent Layer"
        MA[Master Agent]
        WA1[Worker Agents 1-3]
        WA2[Worker Agents 4-7]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL<br/>Primary)]
        PGR[(PostgreSQL<br/>Replica)]
        REDIS[(Redis Cluster)]
    end
    
    subgraph "ML Layer"
        ML1[Model Server 1]
        ML2[Model Server 2]
    end
    
    subgraph "External Services"
        TTS[ElevenLabs API]
        WS[Workshop API]
        MFG[Manufacturing API]
    end
    
    WEB --> LB
    MOB --> LB
    
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> MA
    API2 --> MA
    API3 --> MA
    
    MA --> WA1
    MA --> WA2
    
    WA1 --> ML1
    WA2 --> ML2
    
    API1 --> PG
    API2 --> PG
    API3 --> PG
    PG --> PGR
    
    MA --> REDIS
    WA1 --> REDIS
    WA2 --> REDIS
    
    WA1 --> TTS
    WA1 --> WS
    WA2 --> MFG
    
    style LB fill:#4a9eff,stroke:#333,stroke-width:2px
    style MA fill:#8b5cf6,stroke:#333,stroke-width:3px,color:#fff
    style REDIS fill:#ef4444,stroke:#333,stroke-width:2px
```

---

## 9. Technology Stack Diagram

```mermaid
graph TB
    subgraph "Presentation Layer"
        P1[React 18]
        P2[TailwindCSS]
        P3[Recharts]
        P4[Vite]
    end
    
    subgraph "API Layer"
        A1[FastAPI 0.104]
        A2[Pydantic]
        A3[WebSockets]
    end
    
    subgraph "Business Logic"
        B1[LangChain]
        B2[Agent Framework]
        B3[Task Queue]
    end
    
    subgraph "ML/AI Layer"
        M1[scikit-learn]
        M2[XGBoost]
        M3[Prophet]
        M4[OpenAI/LLM]
        M5[ElevenLabs TTS]
    end
    
    subgraph "Data Layer"
        D1[PostgreSQL 15]
        D2[SQLAlchemy]
        D3[Redis 7]
    end
    
    subgraph "Infrastructure"
        I1[Docker]
        I2[Docker Compose]
        I3[GitHub Actions]
    end
    
    P1 --> A1
    P2 --> P1
    P3 --> P1
    P4 --> P1
    
    A1 --> B1
    A2 --> A1
    A3 --> A1
    
    B1 --> M1
    B2 --> B1
    B3 --> B1
    
    M1 --> D1
    M2 --> D1
    M3 --> D1
    M4 --> B1
    M5 --> B1
    
    D1 --> I1
    D2 --> D1
    D3 --> B3
    
    I1 --> I2
    I2 --> I3
    
    style P1 fill:#61dafb,stroke:#333,stroke-width:2px
    style A1 fill:#009688,stroke:#333,stroke-width:2px
    style M1 fill:#f7931e,stroke:#333,stroke-width:2px
    style D1 fill:#336791,stroke:#333,stroke-width:2px,color:#fff
```

---

## 10. Demo Flow Diagram

```mermaid
graph LR
    START([Start Demo]) --> S1[Show Dashboard<br/>10 vehicles]
    S1 --> S2[Click VEH003<br/>Critical status]
    S2 --> S3[Show Telemetry<br/>Vibration spike]
    S3 --> S4[Show Prediction<br/>85% brake failure]
    S4 --> S5[Agent Status<br/>8 agents working]
    S5 --> S6[Play Voice Call<br/>Customer accepts]
    S6 --> S7[Show Booking<br/>Dec 10, 10 AM]
    S7 --> S8[Complete Service<br/>Brake pads replaced]
    S8 --> S9[Show RCA/CAPA<br/>Supplier defect]
    S9 --> S10[UEBA Demo<br/>Simulate attack]
    S10 --> S11[Show Mitigation<br/>Auto-throttle]
    S11 --> END([End: Impact<br/>95% reduction])
    
    style START fill:#10b981,stroke:#333,stroke-width:2px,color:#fff
    style S6 fill:#8b5cf6,stroke:#333,stroke-width:2px,color:#fff
    style S10 fill:#ef4444,stroke:#333,stroke-width:2px,color:#fff
    style END fill:#10b981,stroke:#333,stroke-width:2px,color:#fff
```

---

## Usage Instructions

### For Presentations
1. Copy any diagram to your presentation tool
2. Most tools support Mermaid (PowerPoint, Google Slides with plugins)
3. Or render to PNG using: https://mermaid.live/

### For Documentation
1. These diagrams are already in Markdown
2. GitHub, GitLab, and most doc tools render Mermaid automatically
3. Use in README, wiki, or technical docs

### For Judges
1. Print Diagram 1 (High-Level Architecture) as poster
2. Use Diagram 2 (Data Flow) during demo
3. Show Diagram 10 (Demo Flow) at start of presentation

---

## Customization

To modify diagrams:
1. Visit https://mermaid.live/
2. Paste diagram code
3. Edit and preview in real-time
4. Export as PNG/SVG

---

**These diagrams are designed to impress judges and clearly communicate your technical architecture. Use them liberally in your presentation! 🎨**
