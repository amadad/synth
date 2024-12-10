import json
import sys
import textwrap

sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.validation import TinyPersonValidator
from tinytroupe.extraction import default_extractor as extractor
from tinytroupe.extraction import ResultsReducer
import tinytroupe.control as control

# Create and validate specific types of agents
## The Banker
banker_spec = """
A vice-president of one of the largest Brazilian banks. Has a degree in engineering and an MBA in finance. 
Is facing a lot of pressure from the board of directors to fight off the competition from the fintechs.    
"""
banker_factory = TinyPersonFactory(banker_spec)

banker = banker_factory.generate_person()
print(banker.minibio())

# Define expectations for the Banker
banker_expectations = """
He/she is:
 - Wealthy
 - Very intelligent and ambitious
 - Has a lot of connections
 - Is in his 40s or 50s

Tastes:
  - Likes to travel to other countries
  - Either read books, collect art or play golf
  - Enjoy only the best, most expensive, wines and food
  - Dislikes taxes and regulation

Other notable traits:
  - Has some stress issues, and might be a bit of a workaholic
  - Deep knowledge of finance, economics and financial technology
  - Is a bit of a snob
"""
banker_score, banker_justification = TinyPersonValidator.validate_person(
    banker,
    expectations=banker_expectations,
    include_agent_spec=False,
    max_content_length=None
)
print(f"Banker Score: {banker_score}")
print(textwrap.fill(banker_justification, width=100))

## The Busy Knowledge Worker
bkw_spec = """
A typical knowledge worker in a large corporation grinding his way into upper middle class.
"""
bkw_factory = TinyPersonFactory(bkw_spec)

busy_knowledge_worker = bkw_factory.generate_person()
print(busy_knowledge_worker.minibio())

# Define expectations for the Busy Knowledge Worker
bkw_expectations = """
Some characteristics of this person:
  - Very busy
  - Likes to have lunch with colleagues
  - To travel during vacations
  - Is married and worrying about the cost of living, particularly regarding his/her children
  - Has some stress issues, and potentially some psychiatric problems
  - Went to college and has a degree in some technical field
  - Has some very specific skills
  - Does not have a wide range of interests, being more focused on his/her career, family and very few hobbies if any
"""
score, justification = TinyPersonValidator.validate_person(
    busy_knowledge_worker,
    expectations=bkw_expectations,
    include_agent_spec=False,
    max_content_length=None
)
print(f"Knowledge Worker Score: {score}")
print(textwrap.fill(justification, width=100))

# Check the Busy Knowledge Worker against Banker expectations
wrong_expectations_score, wrong_expectations_justification = TinyPersonValidator.validate_person(
    busy_knowledge_worker,
    expectations=banker_expectations,
    include_agent_spec=False,
    max_content_length=None
)
print(f"Wrong Expectations Score: {wrong_expectations_score}")
print(textwrap.fill(wrong_expectations_justification, width=100))