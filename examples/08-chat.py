import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect

# Create agents
lisa = create_lisa_the_data_scientist()
oscar = create_oscar_the_architect()

# Create the environment and add the agents
world = TinyWorld("Chat Room", [lisa, oscar])

# Make all agents accessible to each other
world.make_everyone_accessible()

# Initiate a conversation
lisa.listen("Talk to Oscar to know more about him")
world.run(4)

# Display the current interactions
lisa.pp_current_interactions()
oscar.pp_current_interactions()