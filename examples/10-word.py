# Wordprocessor usage example


import json
import sys
import csv
sys.path.insert(0, '..') # ensures that the package is imported from the parent directory, not the Python installation


import tinytroupe
from tinytroupe.openai_utils import force_api_type
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.agent import TinyPerson, TinyToolUse
from tinytroupe.environment import TinyWorld
from tinytroupe import control
from tinytroupe.extraction import ResultsExtractor, ResultsReducer
from tinytroupe.enrichment import TinyEnricher
from tinytroupe.extraction import ArtifactExporter
from tinytroupe.tools import TinyWordProcessor
from tinytroupe.story import TinyStory
import tinytroupe.utils as utils
from tinytroupe.examples import create_lisa_the_data_scientist, create_oscar_the_architect, create_marcos_the_physician
data_export_folder = "../data/extractions/wordprocessor"
exporter = ArtifactExporter(base_output_folder=data_export_folder)
enricher = TinyEnricher()
tooluse_faculty = TinyToolUse(tools=[TinyWordProcessor(exporter=exporter, enricher=enricher)])
lisa = create_lisa_the_data_scientist()
lisa.add_mental_faculties([tooluse_faculty])

lisa.listen_and_act("You have just been fired and need to find a new job. You decide to think about what you want in life and then write a resume. Make it very detailed.")
lisa.listen_and_act("What did I just told you?")
