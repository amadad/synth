import json
import sys

sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import default_extractor as extractor
from tinytroupe.extraction import ResultsReducer
from tinytroupe.validation import TinyPersonValidator
import tinytroupe.control as control

# Create a synthetic customer from the target audience
factory = TinyPersonFactory("One of the largest banks in Brazil, full of bureaucracy and legacy systems.")

customer = factory.generate_person(
    """
    The vice-president of one product innovation. Has a degree in engineering and an MBA in finance. 
    Is facing a lot of pressure from the board of directors to fight off the competition from the fintechs.    
    """
)
print(customer.minibio())

# Validate the synthetic customer
customer_expectations = """
He/she is:
- Wealthy
- Very intelligent and ambitious
- Has a lot of connections
- Is in his/her 40s or 50s

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

customer_score, customer_justification = TinyPersonValidator.validate_person(
    customer,
    expectations=customer_expectations,
    include_agent_spec=False,
    max_content_length=None
)

print("Customer score:", customer_score)
print("Customer justification:", customer_justification)

# Perform the interview
customer.think("I am now talking to a business and technology consultant to help me with my professional problems.")

# Ask specific questions and capture responses
customer.listen_and_act("What would you say are your main problems today? Please be as specific as possible.", 
                        max_content_length=3000)

customer.listen_and_act("Can you elaborate on the fintechs?", 
                        max_content_length=3000)

customer.listen_and_act("If you could improve in one of these aspects to better compete, what would that be?", 
                        max_content_length=3000)

customer.listen_and_act("Please give more detail about that, so that we can think about a project to pursue this direction.", 
                        max_content_length=3000)

customer.listen_and_act("Ah, AI-driven insights sound like a good idea. Can you give me examples of how that could help real customers?")