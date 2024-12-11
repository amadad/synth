from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Agent(BaseModel):
    id: str
    name: str
    location: str
    status: str

class Object(BaseModel):
    id: str
    name: str
    location: str

class Environment(BaseModel):
    id: str
    name: str

class EnvironmentState(BaseModel):
    currentTime: str
    location: str
    agents: List[Agent]
    objects: List[Object]

class TimelineEvent(BaseModel):
    id: str
    timestamp: str
    agent: str
    action: str
    description: str

class StorySegment(BaseModel):
    id: str
    content: str
    timestamp: str

class SimulationControlRequest(BaseModel):
    environment_id: Optional[str] = None 