# Phi-4 Information Extraction Demo

Interactive CLI demo for extracting entities, relations, and knowledge graph triples from business text using a fine-tuned Phi-4 model (15B parameters).

## Features

- **Named Entity Recognition (NER)**: Extract 40+ business entity types (companies, products, people, events, financial metrics, etc.)
- **Relation Extraction (RE)**: Identify relationships between entities
- **Triple Generation**: Output structured knowledge graph triples
- **Completely Local**: No external API calls, runs 100% on your machine
- **Semi-Closed IE**: Uses hardcoded business domain schemas

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

Run the interactive demo:

```bash
python interactive_ie_demo.py
```

### Example Session

```
📝 Enter text:
Apple Inc. acquired Beats Electronics in 2014 for $3 billion.
The company was founded by Dr. Dre and Jimmy Iovine.
###
```

Type `###` on a new line when done, or `quit` to exit.

### Example Output

The model will extract:

**Entities:**
- Apple Inc. (company)
- Beats Electronics (company)
- 2014 (year)
- $3 billion (financial_metric)
- Dr. Dre (person)
- Jimmy Iovine (person)

**Relations:**
- acquired
- founded_by

**Triples:**
- (Apple Inc., acquired, Beats Electronics)
- (Apple Inc., had_revenue_of, $3 billion)
- (Beats Electronics, founded_by, Dr. Dre)
- (Beats Electronics, founded_by, Jimmy Iovine)
- (acquisition, occurred_in_year, 2014)

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

## Supported Entity Types

company, product, service, industry, brand, country, location, organization, person, founder, position, event, action, founding, acquisition, merger, partnership, expansion, restructuring, divestment, sale, bankruptcy, financial_metric, business_concept, revenue, profit, loss, investment, funding, market_share, competition, market_trend, regulation, innovation, sustainability, corporate_social_responsibility, award, date/time, year, period

## Supported Relations

part_of, parent_company_of, subsidiary_of, acquired, divested, owns_brand, holds_stake_in, spun_off, formed_from, founded_by, has_CEO, manufactures, develops, produces, sells, has_product_line, is_a_type_of, is_brand_of, features_technology, uses_material, launched_product, had_revenue_of, had_profit_of, in_year, market_value_of, is_publicly_traded, listed_on_exchange, experienced_growth, occurred_in_year, occurred_on_date, resulted_in, preceded, followed_by, marked_milestone, influenced_by, led_to, was_a_response_to, has_trademark, uses_logo, acquired_trademark_from, is_known_for, launched_campaign

## Project Structure

```
phi4-ie-demo/
├── README.md                    # This file
├── interactive_ie_demo.py       # Main demo script
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
