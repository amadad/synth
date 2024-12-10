import json
import sys
sys.path.append('..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.examples import create_lisa_the_data_scientist
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.extraction import ResultsExtractor

# Define the advertisements
tv_ad_1 = """
The Best TV Of Tomorrow - LG 4K Ultra HD TV
https://www.lg.com/tv/oled
AdThe Leading Name in Cinematic Picture. Upgrade Your TV to 4K OLED And See The Difference. It's Not Just OLED, It's LG OLED. Exclusive a9 Processor, Bringing Cinematic Picture Home.

Infinite Contrast · Self-Lighting OLED · Dolby Vision™ IQ · ThinQ AI w/ Magic Remote

Free Wall Mounting Deal
LG G2 97" OLED evo TV
Free TV Stand w/ Purchase
World's No.1 OLED TV
"""

tv_ad_2 = """
The Full Samsung TV Lineup - Neo QLED, OLED, 4K, 8K & More
https://www.samsung.com
AdFrom 4K To 8K, QLED To OLED, Lifestyle TVs & More, Your Perfect TV Is In Our Lineup. Experience Unrivaled Technology & Design In Our Ultra-Premium 8K & 4K TVs.

Discover Samsung Event · Real Depth Enhancer · Anti-Reflection · 48 mo 0% APR Financing

The 2023 OLED TV Is Here
Samsung Neo QLED 4K TVs
Samsung Financing
Ranked #1 By The ACSI®
"""

tv_ad_3 = """
Wayfair 55 Inch Tv - Wayfair 55 Inch Tv Décor
Shop Now
https://www.wayfair.com/furniture/free-shipping
AdFree Shipping on Orders Over $35. Shop Furniture, Home Décor, Cookware & More! Free Shipping on All Orders Over $35. Shop 55 Inch Tv, Home Décor, Cookware & More!
"""

# Create evaluation request message
eval_request_msg = f"""
Can you evaluate these Bing ads for me? Which one convinces you more to buy their particular offering? 
Select **ONLY** one. Please explain your reasoning, based on your financial situation, background, and personality.

# AD 1 {tv_ad_1}
# AD 2 {tv_ad_2}
# AD 3 {tv_ad_3}

"""

# Define situation
situation = "Your TV broke and you need a new one. You search for a new TV on Bing."

# Create a standard agent and evaluate
lisa = create_lisa_the_data_scientist()
lisa.change_context(situation)
lisa.listen_and_act(eval_request_msg)

# Extract results
extractor = ResultsExtractor()
extraction_objective = "Find the ad the agent chose. Extract the Ad number and title."
res = extractor.extract_results_from_agent(lisa, 
                          extraction_objective=extraction_objective,
                          situation=situation,
                          fields=["ad_number", "ad_title"],
                          verbose=True)

# Output results
print(f"{res['ad_number']}: {res['ad_title']}")

# Generate on-the-fly agents and evaluate
factory = TinyPersonFactory("""
                            People with a broad and diverse range of personalities, interests, backgrounds, and socioeconomic status.
                            Focus in particular:
                              - on financial aspects, ensuring we have both people with high and low income.
                              - on aesthetic aspects, ensuring we have people with different tastes.
                            """)
people = factory.generate_people(20, verbose=True)

choices = []
for person in people:
    person.listen_and_act(eval_request_msg)
    res = extractor.extract_results_from_agent(person,
                                    extraction_objective=extraction_objective,
                                    situation=situation,
                                    fields=["ad_number", "ad_title"],
                                    fields_hints={"ad_number": "Must be an integer, not a string."},
                                    verbose=True)
    choices.append(res)

# Count votes
votes = {}
for choice in choices:
    ad_number = choice['ad_number']
    if ad_number not in votes:
        votes[ad_number] = 0
    votes[ad_number] += 1

# Determine the winner
winner = max(votes, key=votes.get)
print(f"The most voted ad is Ad {winner}.")