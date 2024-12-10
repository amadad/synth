# Synth: Persona Maker & Market Research Simulator

A powerful toolkit for conducting market research using synthetic personas. This project leverages AI to simulate diverse consumer responses and analyze market potential across different demographics.

## Features

- **Market Research Simulation** (`examples/03-gaz.py`):
  - Generate synthetic consumer panels
  - Conduct market surveys
  - Analyze response distributions
  - Compare markets across nationalities
  - Visualize results with matplotlib

- **Ad Testing** (`examples/06-travel.py`): 
  - Test ad effectiveness across different personas
  - Generate diverse consumer profiles
  - Extract structured feedback
  - Analyze ad preferences
  - Track voting patterns

## Getting Started

1. Install dependencies using uv:
```bash
uv pip install openai python-dotenv pandas matplotlib
```

2. Set up your OpenAI API key in `.env`:
```env
OPENAI_API_KEY=your_key_here
OPENAI_API_TYPE=openai  # or 'azure' if using Azure OpenAI
OPENAI_MODEL=gpt-4  # or your preferred model
```

3. Run example simulations:
```bash
python examples/03-gaz.py  # Market research simulation
python examples/06-travel.py  # Ad testing
```

## Usage Examples

### Market Research
```python
# Create synthetic consumer panel
factory = TinyPersonFactory(context)
people = factory.generate_people(100)

# Run market survey
market = TinyWorld("Target audience", people)
market.broadcast(survey_question)
market.run(1)

# Analyze results
results = ResultsExtractor().extract_results_from_agents(people)
```

### Ad Testing
```python
# Generate diverse consumer profiles
factory = TinyPersonFactory(target_audience_context)
people = factory.generate_people(100)

# Test ads
for person in people:
    person.listen_and_act(ad_evaluation_request)

# Extract preferences
results = ResultsExtractor().extract_results_from_agents(people)
```

## Project Structure

- `examples/` - Example simulations and use cases
  - `03-gaz.py` - Market research simulation example
  - `06-travel.py` - Ad testing example
- `tinytroupe/` - Core library components
  - `agent.py` - Persona simulation
  - `environment.py` - Simulation environment
  - `factory.py` - Persona generation
  - `extraction.py` - Result analysis
  - `validation.py` - Input validation
  - `prompts/` - Template files for AI interactions

## Output Formats

### Market Research Results
```json
{
    "response": "Yes/No/Maybe",
    "justification": "Detailed reasoning...",
    "demographics": {
        "nationality": "...",
        "age": "...",
        "interests": [...]
    }
}
```

### Ad Testing Results
```json
{
    "ad_id": 1,
    "ad_title": "...",
    "justification": "...",
    "persona_details": {
        "background": "...",
        "preferences": "..."
    }
}
```

## Limitations

- Results are simulations and should be validated with real market research
- Quality depends on the OpenAI model and prompts used
- Response times scale with the number of personas
- Costs scale with API usage

## Disclaimer

This toolkit uses AI to simulate consumer responses. While powerful for early-stage research, it should be used as a complement to, not a replacement for, real consumer feedback. Results should be validated with actual market research.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details