import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.examples import create_lisa_the_data_scientist, create_marcos_the_physician, create_oscar_the_architect
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import ResultsExtractor

# Define travel ads
travel_ad_1 = """
Tailor-Made Tours Of Europe - Nat'l Geographic Award Winner
https://www.kensingtontours.com/private-tours/europe

AdPrivate Guides; Custom Trip Itineraries; 24/7 In-Country Support. Request A Custom Quote. Europe's Best Customized For You - Historic Cities, Scenic Natural Wonders & More.
"""

travel_ad_2 = """
Europe all-inclusive Packages - Europe Vacation Packages
https://www.exoticca.com/europe/tours

AdDiscover our inspiring Europe tour packages from the US: Capitals, Beaches and much more. Enjoy our most exclusive experiences in Europe with English guides and Premium hotels
"""

travel_ad_3 = """
Travel Packages - Great Vacation Deals
https://www.travelocity.com/travel/packages

AdHuge Savings When You Book Flight and Hotel Together. Book Now and Save! Save When You Book Your Flight & Hotel Together At Travelocity.
"""

travel_ad_4 = """
Europe Luxury Private Tours
https://www.kensingtontours.com
Kensington Tours - Private Guides, Custom Itineraries, Hand Picked Hotels & 24/7 Support
"""

eval_request_msg = f"""
Can you evaluate these Bing ads for me? Which one convices you more to buy their particular offering? 
Select a single ad, not multiple ones. Please explain your reasoning, based on your background and personality.

To do so, also follow these steps:
  - Read all of the 4 ads below. **Do not** skip any, since the best one might be the last one.
  - Disconsider the order of the ads, and focus on the content itself, since they are shuffled at random.

# AD 1 {travel_ad_1}
# AD 2 {travel_ad_2}
# AD 3 {travel_ad_3}
# AD 4 {travel_ad_4}

"""

print(eval_request_msg)

# Define the situation
situation = "You decided you want to visit Europe and you are planning your next vacations. You start by searching for good deals as well as good ideas."
extraction_objective = "Find the ad the agent chose. Extract the Ad number, title and justification for the choice. Extract only ONE choice."

# Try with example agents
people = [create_lisa_the_data_scientist(), create_marcos_the_physician(), create_oscar_the_architect()]

for person in people:
    person.change_context(situation)
    person.listen_and_act(eval_request_msg)

# Extract results from predefined agents
extractor = ResultsExtractor()
choices = []

for person in people:
    res = extractor.extract_results_from_agent(person,
                                               extraction_objective=extraction_objective,
                                               situation=situation,
                                               fields=["ad_id", "ad_title", "justification"])
    choices.append(res)

print(choices)
choices[0]

# Generate agents dynamically
factory = TinyPersonFactory("""
Americans with a broad and very diverse range of personalities, interests, backgrounds and socioeconomic status, 
who are looking for a travel package to Europe. 

Focus in particular on these dimensions:
  - partner status: from those traveling alone to those traveling with a partner.
  - financial situation: from poor to rich.
  - luxury preferences: from simple tastes to sophisticated tastes.
  - security concerns: from very cautious to very adventurous.
  - hotel amenities: from basic to luxury.
  - travel planning: from those who prefer to plan every detail themselves to those who prefer to delegate the planning.
  - social confirmation: from those who prefer to do their own thing to those who prefer to follow the crowd.
""")
people = factory.generate_people(100, "A random person from the target audience who is planning a trip to Europe.", 
                                 temperature=1.9, 
                                 verbose=True)

for person in people:
    person.listen_and_act(eval_request_msg)

# Extract results from dynamic agents
choices = []

for person in people:
    res = extractor.extract_results_from_agent(person,
                                               extraction_objective=extraction_objective,
                                               situation=situation,
                                               fields=["ad_id", "ad_title", "justification"],
                                               fields_hints={"ad_id": "Must be an integer, not a string."},
                                               verbose=True)
    choices.append(res)

votes = {}
for choice in choices:
    try:
        ad_id = choice.get('ad_id')
        if ad_id:
            print(f"{ad_id}: {choice.get('ad_title', 'No title')}")
            if ad_id not in votes:
                votes[ad_id] = 0
            votes[ad_id] += 1
    except (KeyError, AttributeError):
        continue

print("Vote results:", votes)

# Determine the winning ad
winner = max(votes, key=votes.get)
print("Winning Ad:", winner)

