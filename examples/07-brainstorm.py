import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect, create_marcos_the_physician
from tinytroupe.extraction import ResultsExtractor

# Initialize the focus group
world = TinyWorld("Focus group", [
    create_lisa_the_data_scientist(),
    create_oscar_the_architect(),
    create_marcos_the_physician()
])

# Step 1: Introduce themselves and discuss problems
world.broadcast("""
                Hello everyone! Let's start by introducing ourselves. What is your job and what are some major problems you face in your work? 
                What are major challenges for your industry as a whole? Don't discuss solutions yet, just the problems you face.
                """)
world.run(1)

# Step 2: Brainstorm AI feature ideas
world.broadcast("""
                Folks, your mission is to brainstorm potential AI feature ideas
                to add to Microsoft Word. In general, we want features that make you or your industry more productive,
                taking advantage of all the latest AI technologies. Think about the problems you described - what could help with them? 
                Avoid obvious ideas, like summarization or translation. Also avoid simple things like minor UI improvements. 
                We want to think big here - you can fully reimagine Word if that's what it takes. 
                Do not worry about implementation details, marketing, or any other business considerations. 
                Just focus on the AI feature ideas themselves. Select and develop the most promising ideas.
                    
                Please start the discussion now.
                """)
world.run(4)

# Step 3: Add more details to the ideas
world.broadcast("""
                Ok, great. Now please add more details to these ideas - we need to understand them better. How would they actually integrate with Word? 
                Can you provide some concrete examples of what customers could do?
                """)
world.run(2)

# Step 4: Consolidate the ideas
rapporteur = world.get_agent_by_name("Lisa")
rapporteur.listen_and_act("""
                          Can you please consolidate the ideas that the group came up with? Provide a lot of details on each idea, 
                          and complement anything missing.
                          """)

# Extract and consolidate results
extractor = ResultsExtractor()
consolidated_ideas = extractor.extract_results_from_agent(
    rapporteur, 
    extraction_objective=(
        "Consolidates the ideas that the group came up with, explaining each idea as an item of a list."
        "Add all relevant details, including key benefits and drawbacks, if any."
    ), 
    situation="A focus group to brainstorm AI feature ideas for Microsoft Word."
)

# Print the consolidated ideas
print(consolidated_ideas)