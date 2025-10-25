# Phi-4 Information Extraction Demo

Interactive CLI demo for extracting entities, relations, and knowledge graph triples from business text using a fine-tuned Phi-4 model (15B parameters).

## Features

- **Named Entity Recognition (NER)**: Extract entities from text based on custom schemas
- **Relation Extraction (RE)**: Identify relationships between entities
- **Triple Generation**: Output structured knowledge graph triples
- **Completely Local**: No external API calls, runs 100% on your machine
- **Schema-Driven IE**: Flexible extraction using interchangeable JSON schemas
- **Domain Switching**: Same text, different semantic extractions by changing schemas

## Prerequisites

- **macOS** (or Linux/Windows with Ollama support)
- **Python 3.8+**
- **16GB+ RAM recommended** (model is 8.3GB quantized)

## Installation

### 1. Install Ollama

```bash
# macOS
brew install ollama
brew services start ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

### 2. Pull the Model

This downloads the quantized model (8.3GB):

```bash
ollama pull jckalo/phi4-ie
```

### 3. Install Python Dependency

```bash
pip install requests
```

### 4. Clone This Repository

```bash
git clone https://github.com/JanKalo/phi4-ie-demo.git
cd phi4-ie-demo
```

## Usage

Run the interactive demo with a schema:

```bash
# Business domain extraction
python interactive_ie_demo.py --schema schema_business.json

# Academic domain extraction
python interactive_ie_demo.py --schema schema_academic.json
```

### Example: Schema Switching Demo

The same text extracts **different information** depending on the schema.

**Input Text:**
```
Dr. Sarah Johnson at Stanford University published a paper on AI funded by the National Science Foundation.
###
```

#### With Business Schema:
```bash
python interactive_ie_demo.py --schema schema_business.json
```

**Entities Extracted:**
- Dr. Sarah Johnson → `person`
- Stanford University → `institution`
- Artificial intelligence → `topic`
- National Science Foundation → `funding_source`

**Relations & Triples:**
- (AI, funded_by, National Science Foundation)
- (Stanford University, has_member, Dr. Sarah Johnson)
- (AI, published_in, "Journal of Artificial Intelligence")

#### With Academic Schema:
```bash
python interactive_ie_demo.py --schema schema_academic.json
```

**Entities Extracted:**
- Sarah Johnson (scientist) → `researcher`
- Stanford University → `institution`
- National Science Foundation → `funding_agency`
- Artificial intelligence → `research_field`

**Relations & Triples:**
- (Dr. Sarah Johnson, affiliated_with, Stanford University)
- (AI, funded_by, National Science Foundation)
- (Dr. Sarah Johnson, published_in, "Artificial Intelligence")

**Key Difference:** Business schema sees organizational membership (`has_member`), while academic schema sees research affiliation (`affiliated_with`). Same text, different semantic interpretation!

Type `###` on a new line when done, or `quit` to exit.

## Performance Notes

⚠️ **This is a 15B parameter model running on CPU** - inference will be slow:

- **First query:** 30-60 seconds (model loading into RAM)
- **Subsequent queries:** 10-30 seconds per extraction
- **RAM usage:** ~10-12GB during inference
- **Best performance:** Machines with high-end CPUs or GPUs

### Unloading the Model

The model stays loaded in RAM for faster subsequent queries. To free up memory:

```bash
# Stop Ollama completely
brew services stop ollama

# Or restart it
brew services restart ollama
```

### Performance Tips

For production use, consider:
- Running on a machine with GPU support
- Using a smaller quantized version (contact maintainer)
- Deploying to a dedicated inference server

## Included Schemas

### Business Schema (`schema_business.json`)
Extracts corporate and commercial information:
- **40 entity types**: company, product, service, industry, brand, financial metrics, people, locations, events, etc.
- **42 relations**: acquired, founded_by, owns_brand, has_CEO, manufactures, had_revenue_of, etc.

### Academic Schema (`schema_academic.json`)
Extracts research and scholarly information:
- **44 entity types**: researcher, professor, university, paper, journal, conference, grant, funding_agency, etc.
- **46 relations**: affiliated_with, authored, published_in, cited, funded_by, collaborated_with, etc.

### Custom Schemas

You can create your own schema JSON files! Format:

```json
{
  "name": "Your Schema Name",
  "description": "What this schema extracts",
  "entity_types": ["type1", "type2", ...],
  "relations": ["relation1", "relation2", ...]
}
```

## Project Structure

```
phi4-ie-demo/
├── README.md                    # This file
├── interactive_ie_demo.py       # Main demo script
├── schema_business.json         # Business domain schema
├── schema_academic.json         # Academic domain schema
├── Modelfile                    # (Reference) Ollama model config
└── convert_and_quantize.sh      # (Advanced) Convert HF model to GGUF
```

## Troubleshooting

### "Model not found" error

Make sure you've pulled the model:
```bash
ollama pull jckalo/phi4-ie
```

### "Cannot connect to Ollama" error

Start the Ollama service:
```bash
brew services start ollama
```

### Laptop freezing or very slow

The 15B model is resource-intensive. Try:
- Closing other applications
- Running on a more powerful machine
- Using a smaller model variant

## Advanced: Model Conversion

Want to convert a different HuggingFace model to GGUF format? See `convert_and_quantize.sh` for the conversion pipeline.

This repo includes the conversion script for reference, but you don't need it to run the demo.

## Credits

- **Base model:** Microsoft Phi-4
- **Fine-tuned model:** [FinaPolat/phi4_adaptable_IE](https://huggingface.co/FinaPolat/phi4_adaptable_IE)
- **Quantization:** llama.cpp
- **Local inference:** Ollama
- **Model hosting:** Ollama Registry

## License

Model usage subject to Microsoft Phi-4 license terms.

## Citation

If you use this model in your research, please cite:

```bibtex
@misc{phi4-ie-demo,
  author = {Jan Kalo},
  title = {Phi-4 Information Extraction Demo},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/JanKalo/phi4-ie-demo}
}
```
