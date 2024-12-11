from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
from datetime import datetime
from .models import (
    Agent, Environment, EnvironmentState, TimelineEvent,
    StorySegment, SimulationControlRequest
)

app = FastAPI(title="TinyTroupe API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulation state
class SimulationState:
    def __init__(self):
        self.is_running = False
        self.current_environment = None
        self.events = []
        self.story = []
        self.step_count = 0

    def reset(self):
        self.is_running = False
        self.current_environment = None
        self.events = []
        self.story = []
        self.step_count = 0

sim_state = SimulationState()

# Mock data
ENVIRONMENTS = [
    Environment(id="house", name="House Environment"),
    Environment(id="office", name="Office Environment"),
    Environment(id="park", name="Park Environment"),
]

AGENTS = [
    Agent(id="1", name="Alice", location="Living Room", status="Reading"),
    Agent(id="2", name="Bob", location="Kitchen", status="Cooking"),
]

@app.get("/environments", response_model=List[Environment])
async def list_environments():
    return ENVIRONMENTS

@app.get("/agents", response_model=List[Agent])
async def list_agents():
    return AGENTS

@app.post("/simulation/start")
async def start_simulation(data: SimulationControlRequest):
    env_id = data.environment_id or "house"
    env = next((e for e in ENVIRONMENTS if e.id == env_id), None)
    if not env:
        raise HTTPException(status_code=404, detail="Environment not found")
    
    sim_state.reset()
    sim_state.is_running = True
    sim_state.current_environment = env
    
    # Add initial event
    sim_state.events.append(
        TimelineEvent(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            agent="System",
            action="Start",
            description=f"Started simulation in {env.name}"
        )
    )
    
    return {"status": "started", "environment": env.name}

@app.post("/simulation/pause")
async def pause_simulation():
    if not sim_state.is_running:
        raise HTTPException(status_code=400, detail="No simulation running")
    sim_state.is_running = False
    return {"status": "paused"}

@app.post("/simulation/resume")
async def resume_simulation():
    if sim_state.current_environment is None:
        raise HTTPException(status_code=400, detail="No simulation to resume")
    sim_state.is_running = True
    return {"status": "resumed"}

@app.post("/simulation/stop")
async def stop_simulation():
    if sim_state.current_environment is None:
        raise HTTPException(status_code=400, detail="No simulation running")
    sim_state.reset()
    return {"status": "stopped"}

@app.post("/simulation/step")
async def step_simulation(steps: dict):
    if not sim_state.current_environment:
        raise HTTPException(status_code=400, detail="No simulation running")
    
    # Extract steps from request body
    step_count = steps.get('body', 1)  # Default to 1 if not specified
    sim_state.step_count += step_count
    
    # Add step event
    sim_state.events.append(
        TimelineEvent(
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            agent="System",
            action="Step",
            description=f"Advanced simulation by {step_count} steps"
        )
    )
    
    # Add mock story segment
    sim_state.story.append(
        StorySegment(
            id=str(uuid.uuid4()),
            content=f"The simulation advanced by {step_count} steps. Alice and Bob continued their activities.",
            timestamp=datetime.now().isoformat()
        )
    )
    
    return {"status": "stepped", "steps": step_count}

@app.get("/events", response_model=List[TimelineEvent])
async def get_events():
    return sim_state.events

@app.get("/story", response_model=List[StorySegment])
async def get_story():
    return sim_state.story

@app.get("/environment/state", response_model=EnvironmentState)
async def get_environment_state():
    # Return default state if no simulation is running
    env_name = sim_state.current_environment.name if sim_state.current_environment else "No Environment"
    
    return EnvironmentState(
        currentTime=datetime.now().isoformat(),
        location=env_name,
        agents=AGENTS,
        objects=[
            {"id": "1", "name": "Couch", "location": "Living Room"},
            {"id": "2", "name": "Stove", "location": "Kitchen"},
            {"id": "3", "name": "Table", "location": "Dining Room"}
        ]
    ) 