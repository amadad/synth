import json
import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, '..')

import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.validation import TinyPersonValidator
from tinytroupe import control
from tinytroupe.extraction import ResultsExtractor

# Start simulation control with caching
control.begin("bottled_gazpacho_market_research.cache.json")

# Define target audience
target_nationality = "American"
population_size = 100
compute_other_nationalities = True

# Survey context
def general_context(nationality="American"):
    return f"""
    We are performing market research on the {nationality} population, targeting culinary tastes and shopping habits. 
    Ensure representation from diverse demographics: age, income, health, education, etc.
    """

# Interviewer questions
interviewer_introduction = """
We are performing market research. Can you present yourself and list your top-10 interests?
"""

interviewer_main_question = """
Would you buy bottled gazpacho if you went to the supermarket today? Why yes, or why not?
Start your response with "Yes,", "No," or "Maybe," and justify your choice.
"""

# Result extraction configuration
results_extractor = ResultsExtractor(
    extraction_objective="Find whether the person would buy the product. A person can say Yes, No or Maybe.",
    situation="Agent was asked to rate their interest in a bottled Gazpacho.",
    fields=["response", "justification"],
    fields_hints={"response": "Must be 'Yes', 'No', 'Maybe', or 'N/A'."},
    verbose=True
)

# Analysis function
def is_there_a_good_market(df, yes_threshold=0.1, no_threshold=0.5):
    response = df["response"]
    counts = df["response"].value_counts()
    total = counts.sum()
    percentage = counts / total

    percentage_yes = percentage.get("Yes", 0)
    percentage_no = percentage.get("No", 0)
    percentage_maybe = percentage.get("Maybe", 0)
    percentage_na = percentage.get("N/A", 0)

    print(f"Percentage of 'Yes': {percentage_yes:.2%}")
    print(f"Percentage of 'No': {percentage_no:.2%}")
    print(f"Percentage of 'Maybe': {percentage_maybe:.2%}")
    print(f"Percentage of 'N/A': {percentage_na:.2%}")

    if percentage_yes > yes_threshold and percentage_no < no_threshold:
        print("VERDICT: There is a good market for bottled gazpacho.")
        return True
    else:
        print("VERDICT: There is not a good market for bottled gazpacho.")
        return False

# Generate audience
factory = TinyPersonFactory(general_context(target_nationality))
people = factory.generate_people(population_size, verbose=True)
factory.generated_minibios
control.checkpoint()

# Enclose audience in an environment
market = TinyWorld(f"Target audience ({target_nationality})", people, broadcast_if_no_target=False)

# Perform market research
market.broadcast(interviewer_introduction)
market.broadcast(interviewer_main_question)
market.run(1)
control.checkpoint()

# Extract results
results = results_extractor.extract_results_from_agents(people)
df = pd.DataFrame(results)
df["response"].value_counts().plot(kind='bar')
is_there_a_good_market(df)

# Benchmark: Spain
factory_es = TinyPersonFactory(general_context(nationality="Spanish"))
people_es = factory_es.generate_people(population_size, verbose=True)
control.checkpoint()

market_es = TinyWorld(f"Target audience (Spanish)", people_es, broadcast_if_no_target=False)
market_es.broadcast(interviewer_introduction)
market_es.broadcast(interviewer_main_question)
market_es.run(1)
control.checkpoint()

results_es = results_extractor.extract_results_from_agents(people_es)
df_es = pd.DataFrame(results_es)
df_es["response"].value_counts().plot(kind='bar')
is_there_a_good_market(df_es)

# Compare target market with Spanish benchmark
percentage_yes = df["response"].value_counts(normalize=True).get("Yes", 0)
percentage_yes_es = df_es["response"].value_counts(normalize=True).get("Yes", 0)
print(f"Percentage of 'Yes' (Target Market): {percentage_yes:.2%}")
print(f"Percentage of 'Yes' (Spain): {percentage_yes_es:.2%}")

if percentage_yes != 0:
    print(f"Spanish people are {percentage_yes_es / percentage_yes:.2f} times more likely to buy.")

# Bar chart comparison
fig, ax = plt.subplots()
df["response"].value_counts().reindex(["Yes", "Maybe", "No", "N/A"]).plot(kind='bar', color='blue', position=0, width=0.4, label="Target Market", ax=ax)
df_es["response"].value_counts().reindex(["Yes", "Maybe", "No", "N/A"]).plot(kind='bar', color='red', position=1, width=0.4, label="Spain", ax=ax)
plt.legend()
plt.show()

# Other nationalities (if selected)
if compute_other_nationalities:
    def market_research_simulation(nationality, population_size, results_extractor):
        factory = TinyPersonFactory(general_context(nationality=nationality))
        people = factory.generate_people(population_size, verbose=True)
        market = TinyWorld(f"Target audience ({nationality})", people, broadcast_if_no_target=False)
        control.checkpoint()

        market.broadcast(interviewer_introduction)
        market.broadcast(interviewer_main_question)
        market.run(1)
        control.checkpoint()

        results = results_extractor.extract_results_from_agents(people)
        df = pd.DataFrame(results)
        return df

    # Example: Brazil
    df_br = market_research_simulation("Brazilian", population_size, results_extractor)
    df_br["response"].value_counts().plot(kind='bar')
    is_there_a_good_market(df_br)

control.end()