import json
import sys
sys.path.append('../..')  # Adjust the path for importing the TinyTroupe package

import tinytroupe
from tinytroupe.agent import TinyPerson, TinyToolUse
from tinytroupe.environment import TinyWorld
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import ArtifactExporter
from tinytroupe.enrichment import TinyEnricher
from tinytroupe.tools import TinyWordProcessor

# Define a factory for generating agents
factory = TinyPersonFactory("A random knowledge worker in a company providing marketing services.")

# Generate two agents
agent_1 = factory.generate_person()
agent_2 = factory.generate_person()

# Setup for exporting artifacts and enriching content
exporter = ArtifactExporter(base_output_folder="./outputs/scratches/tool_usage")
enricher = TinyEnricher()

# Define tool usage capabilities with the TinyWordProcessor tool
tooluse_faculty = TinyToolUse(tools=[TinyWordProcessor(exporter=exporter, enricher=enricher)])

# Add tool-using faculties to the agents
agent_1.add_mental_faculties([tooluse_faculty])
agent_2.add_mental_faculties([tooluse_faculty])

# Print the specification of the first agent for verification
print(agent_1.generate_agent_specification())

# Create a world for the agents to interact in
company = TinyWorld("Focus group", [agent_1, agent_2])
company.make_everyone_accessible()

# Simulate a brainstorming session with a task
company.broadcast("Brainstorm one or two ideas and then write a short document about it.")

# Run the simulation for 2 minutes
company.run_minutes(2)