import random
import pandas as pd
from tinytroupe.agent import TinyPerson

class ABRandomizer():

    def __init__(self, real_name_1="control", real_name_2="treatment",
                       blind_name_a="A", blind_name_b="B",
                       passtrough_name=[],
                       random_seed=42):
        """
        An utility class to randomize between two options, and de-randomize later.
        The choices are stored in a dictionary, with the index of the item as the key.
        The real names are the names of the options as they are in the data, and the blind names
        are the names of the options as they are presented to the user. Finally, the passtrough names
        are names that are not randomized, but are always returned as-is.

        Args:
            real_name_1 (str): the name of the first option
            real_name_2 (str): the name of the second option
            blind_name_a (str): the name of the first option as seen by the user
            blind_name_b (str): the name of the second option as seen by the user
            passtrough_name (list): a list of names that should not be randomized and are always
                                    returned as-is.
            random_seed (int): the random seed to use
        """

        self.choices = {}
        self.real_name_1 = real_name_1
        self.real_name_2 = real_name_2
        self.blind_name_a = blind_name_a
        self.blind_name_b = blind_name_b
        self.passtrough_name = passtrough_name
        self.random_seed = random_seed

    def randomize(self, i, a, b):
        """
        Randomly switch between a and b, and return the choices.
        Store whether the a and b were switched or not for item i, to be able to
        de-randomize later.

        Args:
            i (int): index of the item
            a (str): first choice
            b (str): second choice
        """
        # use the seed
        if random.Random(self.random_seed).random() < 0.5:
            self.choices[i] = (0, 1)
            return a, b
            
        else:
            self.choices[i] = (1, 0)
            return b, a
    
    def derandomize(self, i, a, b):
        """
        De-randomize the choices for item i, and return the choices.

        Args:
            i (int): index of the item
            a (str): first choice
            b (str): second choice
        """
        if self.choices[i] == (0, 1):
            return a, b
        elif self.choices[i] == (1, 0):
            return b, a
        else:
            raise Exception(f"No randomization found for item {i}")
    
    def derandomize_name(self, i, blind_name):
        """
        Decode the choice made by the user, and return the choice. 

        Args:
            i (int): index of the item
            choice_name (str): the choice made by the user
        """

        # was the choice i randomized?
        if self.choices[i] == (0, 1):
            # no, so return the choice
            if blind_name == self.blind_name_a:
                return self.real_name_1
            elif blind_name == self.blind_name_b:
                return self.real_name_2
            elif blind_name in self.passtrough_name:
                return blind_name
            else:
                raise Exception(f"Choice '{blind_name}' not recognized")
            
        elif self.choices[i] == (1, 0):
            # yes, it was randomized, so return the opposite choice
            if blind_name == self.blind_name_a:
                return self.real_name_2
            elif blind_name == self.blind_name_b:
                return self.real_name_1
            elif blind_name in self.passtrough_name:
                return blind_name
            else:
                raise Exception(f"Choice '{blind_name}' not recognized")
        else:
            raise Exception(f"No randomization found for item {i}")

# TODO under development
class Intervention:

    def __init__(self, agent=None, agents:list=None, environment=None, environments:list=None):
        """
        Initialize the intervention.

        Args:
            agent (TinyPerson): the agent to intervene on
            environment (TinyWorld): the environment to intervene on
        """
        # at least one of the parameters should be provided. Further, either a single entity or a list of them.
        if agent and agents:
            raise Exception("Either 'agent' or 'agents' should be provided, not both")
        if environment and environments:
            raise Exception("Either 'environment' or 'environments' should be provided, not both")
        if not (agent or agents or environment or environments):
            raise Exception("At least one of the parameters should be provided")

        # initialize the possible entities
        self.agents = None
        self.environments = None
        if agent is not None:
            self.agents = [self.agent]
        elif environment is not None:
            self.environments = [self.environment]

        # initialize the possible preconditions
        self.text_precondition = None
        self.precondition_func = None

        # effects
        self.effect_func = None

    ################################################################################################
    # Intervention flow
    ################################################################################################     
        
    def check_precondition(self):
        """
        Check if the precondition for the intervention is met.
        """
        raise NotImplementedError("TO-DO")

    def apply(self):
        """
        Apply the intervention.
        """
        self.effect_func(self.agents, self.environments)

    ################################################################################################
    # Pre and post conditions
    ################################################################################################

    def set_textual_precondition(self, text):
        """
        Set a precondition as text, to be interpreted by a language model.

        Args:
            text (str): the text of the precondition
        """
        self.text_precondition = text
    
    def set_functional_precondition(self, func):
        """
        Set a precondition as a function, to be evaluated by the code.

        Args:
            func (function): the function of the precondition. 
              Must have the arguments: agent, agents, environment, environments.
        """
        self.precondition_func = func
    
    def set_effect(self, effect_func):
        """
        Set the effect of the intervention.

        Args:
            effect (str): the effect function of the intervention
        """
        self.effect_func = effect_func
