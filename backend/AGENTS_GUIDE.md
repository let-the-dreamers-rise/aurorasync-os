# 🤖 AuroraSync OS - Multi-Agent System Guide

Complete guide to the multi-agent orchestration system.

---

## 📋 Overview

AuroraSync OS uses a **multi-agent architecture** with:
- **1 Master Agent** - Orchestrates all worker agents
- **6 Worker Agents** - Specialized agents for specific tasks
- **1 UEBA Agent** - Security monitoring and anomaly detection

---

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │  Master Agent   │
                    │  (Orchestrator) │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Data Analysis │    │  Diagnosis    │    │   Customer    │
│     Agent     │    │     Agent     │    │  Engagement   │
└───────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Scheduling   │    │   Feedback    │    │Manufacturing  │
│     Agent     │    │     Agent     │    │   Insights    │
└───────────────┘    └───────────────┘    └───────────────┘
                             │
                             ▼
                    ┌───────────────┐
                    │  UEBA Agent   │
                    │  (Monitoring) │
                    └───────────────┘
```

---

## 🤖 Agent Descriptions

### Master Agent
**File**: `app/agents/master_agent.py`

**Responsibilities**:
- Route events to appropriate worker agents
- Coordinate multi-agent workflows
- Monitor agent health
- Integrate with UEBA for security

**Key Methods**:
- `route_event(event)` - Route event to worker agent
- `get_agent_status()` - Get status of all agents

### Data Analysis Agent
**File**: `app/agents/data_analysis_agent.py`

**Responsibilities**:
- Process raw telematics data
- Extract features (30+ features)
- Detect anomalies
- Prepare data for ML models

**Event Types**:
- `analyze_data` - Analyze raw data
- `extract_features` - Extract features
- `detect_anomaly` - Detect anomalies

### Diagnosis Agent
**File**: `app/agents/diagnosis_agent.py`

**Responsibilities**:
- Run ML models for failure prediction
- Identify components at risk
- Calculate failure probability
- Determine severity and recommended actions

**Event Types**:
- `predict_failure` - Predict vehicle failure
- `diagnose_issue` - Diagnose specific issue
- `assess_risk` - Assess risk level

### Customer Engagement Agent
**File**: `app/agents/customer_engagement_agent.py`

**Responsibilities**:
- Generate persuasive call scripts (LLM)
- Synthesize voice (TTS)
- Manage customer interactions
- Track acceptance rates

**Event Types**:
- `engage_customer` - Engage with customer
- `generate_call_script` - Generate script
- `send_notification` - Send notification

### Scheduling Agent
**File**: `app/agents/scheduling_agent.py`

**Responsibilities**:
- Find available workshop slots
- Optimize scheduling
- Book appointments
- Manage workshop capacity

**Event Types**:
- `schedule_service` - Schedule service
- `find_availability` - Find available slots
- `book_appointment` - Book appointment

### Feedback Agent
**File**: `app/agents/feedback_agent.py`

**Responsibilities**:
- Validate predictions vs actual results
- Calculate accuracy metrics
- Track false positives/negatives
- Trigger model retraining

**Event Types**:
- `validate_prediction` - Validate prediction
- `collect_feedback` - Collect feedback
- `calculate_accuracy` - Calculate accuracy

### Manufacturing Insights Agent
**File**: `app/agents/manufacturing_insights_agent.py`

**Responsibilities**:
- Aggregate failure patterns
- Perform Root Cause Analysis (RCA)
- Generate CAPA reports
- Identify batch/serial patterns

**Event Types**:
- `generate_rca` - Generate RCA report
- `create_capa` - Create CAPA report
- `analyze_patterns` - Analyze patterns

### UEBA Agent
**File**: `app/agents/ueba_agent.py`

**Responsibilities**:
- Log all agent actions
- Monitor performance metrics
- Detect anomalous behavior
- Generate security alerts

**Key Methods**:
- `log_action(agent, action, resource)` - Log action
- `detect_anomaly(agent, metric, value)` - Detect anomaly
- `get_statistics()` - Get UEBA stats

---

## 🔄 Event Flow

### 1. Event Creation
```python
event = {
    "type": "predict_failure",
    "payload": {
        "vehicle_id": "VEH001",
        "features": {...}
    },
    "source": "api",
    "timestamp": "2025-12-03T10:30:00Z"
}
```

### 2. Event Routing
```python
# Master Agent receives event
master_agent = get_master_agent()

# Master Agent logs with UEBA
master_agent.ueba_agent.log_action(
    agent_name="master",
    action="route_event",
    resource="predict_failure"
)

# Master Agent routes to Diagnosis Agent
response = diagnosis_agent.handle_event(event)
```

### 3. Event Processing
```python
# Diagnosis Agent processes event
result = {
    "status": "success",
    "agent": "diagnosis",
    "result": {
        "prediction_id": "PRED-12345",
        "failure_probability": 0.85,
        "component": "brake_system"
    },
    "timestamp": "2025-12-03T10:30:05Z"
}
```

---

## 🧪 Testing the Agent System

### Using the API

**1. Get Agent Status**
```bash
curl http://localhost:8000/api/v1/agents/status
```

**2. Get Available Event Types**
```bash
curl http://localhost:8000/api/v1/agents/event-types
```

**3. Test Agent Routing**
```bash
curl -X POST http://localhost:8000/api/v1/agents/test-route \
  -H "Content-Type: application/json" \
  -d '{
    "type": "predict_failure",
    "payload": {
      "vehicle_id": "VEH001"
    }
  }'
```

**4. Get UEBA Statistics**
```bash
curl http://localhost:8000/api/v1/agents/ueba/stats
```

### Using the Test Script

```bash
python scripts/test_agents.py
```

This will test:
- ✅ Agent status
- ✅ Event types
- ✅ All 7 worker agents
- ✅ UEBA logging

### Using Interactive API Docs

Visit http://localhost:8000/docs and navigate to the **Agents** section.

---

## 📝 API Endpoints

### Agent Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/agents/status` | Get agent status |
| GET | `/api/v1/agents/event-types` | Get available event types |
| POST | `/api/v1/agents/test-route` | Test agent routing |
| GET | `/api/v1/agents/ueba/stats` | Get UEBA statistics |

---

## 🔧 Extending Agents

### Adding a New Event Type

**1. Update Master Agent routing**
```python
# In master_agent.py
self._event_routing = {
    # ... existing routes ...
    "new_event_type": "target_agent_name"
}
```

**2. Implement handler in worker agent**
```python
# In worker_agent.py
def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
    event_type = event.get("type")
    
    if event_type == "new_event_type":
        # Process event
        return self.create_response(
            status="success",
            result={...}
        )
```

### Adding Full Agent Logic

Replace stub implementations with real logic:

**Example: Data Analysis Agent**
```python
def handle_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
    if event_type == "analyze_data":
        # 1. Load raw data
        raw_data = event["payload"]["data"]
        
        # 2. Extract features
        features = self.extract_features(raw_data)
        
        # 3. Detect anomalies
        anomaly_score = self.anomaly_detector.predict(features)
        
        # 4. Return results
        return self.create_response(
            status="success",
            result={
                "features": features,
                "anomaly_score": anomaly_score
            }
        )
```

---

## 🔒 UEBA Integration

Every agent action is automatically logged by UEBA:

```python
# Master Agent logs routing
self.ueba_agent.log_action(
    agent_name="master",
    action="route_event",
    resource=event_type
)

# Worker agent action is logged
self.ueba_agent.log_action(
    agent_name="diagnosis",
    action="handle_event",
    resource=event_type
)
```

**UEBA Log Entry**:
```python
{
    "timestamp": "2025-12-03T10:30:00Z",
    "agent": "diagnosis",
    "action": "handle_event",
    "resource": "predict_failure",
    "metadata": {...},
    "action_id": 42
}
```

---

## 📊 Current Implementation Status

### ✅ Implemented
- [x] BaseAgent abstract class
- [x] MasterAgent with routing
- [x] All 7 worker agent stubs
- [x] UEBA logging hooks
- [x] Event routing system
- [x] API endpoints for testing
- [x] Test script

### 🔄 To Be Implemented (Next Steps)
- [ ] Full agent logic (replace stubs)
- [ ] ML model integration
- [ ] Redis pub/sub for async communication
- [ ] WebSocket for real-time updates
- [ ] Database persistence for events
- [ ] UEBA anomaly detection algorithms
- [ ] Agent health monitoring
- [ ] Retry logic and error handling

---

## 🎯 Next Steps

### Day 4 Tasks (Continue Implementation)

1. **Add Vehicle CRUD Endpoints**
   - Create vehicle management API
   - Integrate with agents

2. **Implement ML Models**
   - Train failure prediction model
   - Integrate with Diagnosis Agent

3. **Add Redis Integration**
   - Set up Redis pub/sub
   - Async agent communication

4. **Add WebSocket Support**
   - Real-time event streaming
   - Live agent status updates

---

## 🐛 Troubleshooting

### Agent not responding

**Check**:
1. Server is running: `uvicorn app.main:app --reload`
2. Agent is initialized: Check logs for "Agent 'name' initialized"
3. Event type is valid: Use `/api/v1/agents/event-types`

### UEBA not logging

**Check**:
1. UEBA agent is initialized
2. Master Agent is calling `ueba_agent.log_action()`
3. Check server logs for UEBA entries

### Event routing fails

**Check**:
1. Event type exists in `_event_routing` dict
2. Target agent is implemented
3. Event payload is valid

---

## 📚 Code Examples

### Example 1: Send Event from Python

```python
import requests

event = {
    "type": "predict_failure",
    "payload": {
        "vehicle_id": "VEH001",
        "features": {
            "rpm_avg": 2500,
            "temp_avg": 85.5
        }
    }
}

response = requests.post(
    "http://localhost:8000/api/v1/agents/test-route",
    json=event
)

print(response.json())
```

### Example 2: Get Agent Status

```python
import requests

response = requests.get(
    "http://localhost:8000/api/v1/agents/status"
)

status = response.json()
print(f"Master Agent: {status['master_agent']['status']}")
print(f"Worker Agents: {status['worker_agents']}")
```

### Example 3: Monitor UEBA

```python
import requests
import time

while True:
    response = requests.get(
        "http://localhost:8000/api/v1/agents/ueba/stats"
    )
    stats = response.json()
    print(f"Actions logged: {stats['total_actions_logged']}")
    time.sleep(5)
```

---

## 🎉 Summary

You now have a working multi-agent system with:
- ✅ Master Agent orchestration
- ✅ 7 worker agents (stubs)
- ✅ UEBA security monitoring
- ✅ Event routing system
- ✅ API endpoints for testing
- ✅ Comprehensive test suite

**Ready to extend with full agent logic!** 🚀

---

<div align="center">

**Next**: Implement full agent logic and ML model integration

**Follow**: Day 4 tasks in `IMPLEMENTATION_ROADMAP.md`

</div>
