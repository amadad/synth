import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.examples import *
from tinytroupe.extraction import default_extractor as extractor

focus_group = TinyWorld("Focus group", [create_lisa_the_data_scientist(), create_oscar_the_architect(), create_marcos_the_physician()])

situation = \
""" 
This is a focus group dedicated to finding the best way to advertise an appartment for rent.
Everyone in the group is a friend to the person who is renting the appartment, called Paulo.
The objective is to find the best way to advertise the appartment, so that Paulo can find a good tenant.
"""

apartment_description = \
"""	
The appartment has the following characteristics:
  - It is in an old building, but was completely renovated and remodeled by an excellent architect. 
    There are almost no walls, so it is very spacious, mostly composed of integrated spaces. 
  - It was also recently repainted, so it looks brand new.
  - 1 bedroom. Originally, it had two, but one was converted into a home office.
  - 1 integrated kitchen and living room. The kitchen is very elegant, with a central eating wood table,
    with 60s-style chairs. The appliances are in gray and steel, and the cabinets are in white, the wood
    is light colored.
  - Has wood-like floors in all rooms, except the kitchen and bathroom, which are tiled.  
  - 2 bathrooms. Both with good taste porcelain and other decorative elements.
  - 1 laundry room. The washing machine is new and also doubles as a dryer.
  - Is already furnished with a bed, a sofa, a table, a desk, a chair, a washing machine, a refrigerator, 
    a stove, and a microwave.
  - It has a spacious shelf for books and other objects.
  - It is close to: a very convenient supermarket, a bakery, a gym, a bus stop, and a subway station. 
    It is also close to a great argentinian restaurant, and a pizzeria.
  - It is located at a main avenue, but the appartment is in the back of the building, so it is very quiet.
  - It is near of the best Medicine School in the country, so it is a good place for a medical student.  
"""

task = \
"""
Discuss the best way to advertise the appartment, so that Paulo can find a good tenant.
"""

focus_group.broadcast(situation)
focus_group.broadcast(apartment_description)
focus_group.broadcast(task)

focus_group.run(3)

extractor.extract_results_from_world(focus_group,
                                     extraction_objective="Compose an advertisement copy based on the ideas given.",
                                     fields=["ad_copy"],
                                    verbose=True)