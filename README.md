# TinyTroupe: AI Agent Simulation Environment

A real-time simulation environment for AI agents with interactive visualization. This project provides a web interface to observe and control multiple AI agents interacting in various environments.

## Features

- **Real-time Simulation**:
  - Start, pause, and step-by-step simulation control
  - Multiple environment support (House, Office, Park)
  - Agent state tracking and visualization
  - Event timeline and story generation

- **Web Interface**:
  - Interactive control panel
  - Real-time state updates
  - Multiple views (Timeline, Story, Environment)
  - Agent status monitoring

## Getting Started

1. Install dependencies:
```bash
# Backend
cd backend
uv pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

2. Start the servers:
```bash
# Backend (in backend directory)
python run.py

# Frontend (in frontend directory)
npm run dev
```

3. Open http://localhost:3000 in your browser

## Usage

1. **Select Environment**:
   - Choose from available environments (House, Office, Park)
   - Each environment has unique objects and interaction possibilities

2. **Control Simulation**:
   - Start/Pause: Control simulation flow
   - Step: Advance simulation by specified steps
   - Monitor events in Timeline view

3. **Monitor Agents**:
   - View agent locations and status
   - Track interactions between agents
   - Follow generated story narrative

## Project Structure

- `frontend/` - Next.js web interface
  - `app/` - Next.js app router components
  - `components/` - React components
  - `lib/` - Utility functions and API client

- `backend/` - FastAPI server
  - `app/` - FastAPI application
    - `main.py` - Server endpoints
    - `models.py` - Data models
  - `requirements.txt` - Python dependencies

## Views

### Timeline View
- Chronological list of events
- Agent actions and interactions
- System events and state changes

### Story View
- Narrative description of simulation
- Agent interactions in natural language
- Environmental context and atmosphere

### Environment View
- Current simulation state
- Agent locations and status
- Object locations and properties

## Technical Details

- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python
- **Communication**: REST API with real-time polling
- **State Management**: Server-side simulation state

## Development

1. **Adding New Environments**:
```python
# backend/app/main.py
ENVIRONMENTS = [
    Environment(id="new_env", name="New Environment"),
    # Add more environments
]
```

2. **Customizing Agents**:
```python
# backend/app/main.py
AGENTS = [
    Agent(id="1", name="CustomAgent", location="Room", status="Active"),
    # Add more agents
]
```

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details