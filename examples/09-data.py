import json
import sys
import csv
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import ResultsReducer

# Create a factory for knowledge workers
factory = TinyPersonFactory("A random knowledge worker in a company providing marketing services.")

# Generate agents
people = []
for i in range(2):
    person = factory.generate_person(temperature=1.6)
    print(person.minibio())
    people.append(person)

print(f"Number of agents created: {len(people)}")

# Create the environment
company = TinyWorld("Some Corp Inc.", people)
company.make_everyone_accessible()

# Simulate interactions
company.broadcast("Get some work done together, help each other.")
company.run(5)

# Display the current interactions of the first person
people[0].pp_current_interactions()

# Define a reducer to extract and structure conversation content
reducer = ResultsReducer()

def aux_extract_content(focus_agent: TinyPerson, source_agent: TinyPerson, target_agent: TinyPerson, kind: str, event: str, content: str, timestamp: str):
    if event == "TALK":
        author = focus_agent.name
    elif event == "CONVERSATION":
        author = "USER" if source_agent is None else source_agent.name
    else:
        raise ValueError(f"Unknown event: {event}")
    
    entry = (author, content)
    print(entry)
    return entry

# Add reduction rules for interactions
reducer.add_reduction_rule("TALK", aux_extract_content)
reducer.add_reduction_rule("CONVERSATION", aux_extract_content)

# Reduce interactions to a dataframe
df = reducer.reduce_agent_to_dataframe(people[0], column_names=["author", "content"])
print(df)

# Save the dataframe to a .csv file
output_path = "../data/extractions/synthetic_data_generation.out.csv"
df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")