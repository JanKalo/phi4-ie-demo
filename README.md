# Phi-4 Information Extraction Demo

Interactive CLI demo for extracting entities, relations, and knowledge graph triples from business text using a fine-tuned Phi-4 model (15B parameters).

## Features

- **Named Entity Recognition (NER)**: Extract 40+ business entity types (companies, products, people, events, financial metrics, etc.)
- **Relation Extraction (RE)**: Identify relationships between entities
- **Triple Generation**: Output structured knowledge graph triples
- **Completely Local**: No external API calls, runs 100% on your machine
- **Semi-Closed IE**: Uses hardcoded business domain schemas

## Prerequisites

1. **Ollama** - For running the quantized model locally
   ```bash
   brew install ollama
   brew services start ollama
   ```

2. **Python 3.8+** with `requests` library
   ```bash
   pip install requests
   # or use conda:
   conda install requests
   ```

3. **Quantized Model** - Download the pre-quantized model (8.3GB):
   - Model: `FinaPolat/phi4_adaptable_IE`
   - You need the Q4_K_M quantized GGUF version (not included in this repo due to size)
   - Place it in: `models/phi4_ie_q4_k_m.gguf`

## Setup

1. **Clone this repository**
   ```bash
   git clone <repo-url>
   cd phi4-ie-demo
   ```

2. **Create the models directory**
   ```bash
   mkdir -p models
   ```

3. **Get the quantized model**

   Either download the pre-quantized GGUF file and place it in `models/phi4_ie_q4_k_m.gguf`, or convert it yourself using the included scripts (see Advanced section).

4. **Create the Ollama model**
   ```bash
   ollama create phi4-ie -f Modelfile
   ```

## Usage

Run the interactive demo:

```bash
python interactive_ie_demo.py
```

### Example Input

```
Apple Inc. acquired Beats Electronics in 2014 for $3 billion.
The company was founded by Dr. Dre and Jimmy Iovine.
```

Type `###` on a new line when done, or `quit` to exit.

### Example Output

The model will extract:
- **Entities**: Apple Inc. (company), Beats Electronics (company), 2014 (year), $3 billion (financial_metric), Dr. Dre (person), Jimmy Iovine (person)
- **Relations**: acquired, founded_by
- **Triples**: (Apple Inc., acquired, Beats Electronics), (Beats Electronics, founded_by, Dr. Dre), etc.

## Performance Notes

⚠️ **This is a 15B parameter model running on CPU** - inference will be slow:
- First query: 30-60 seconds (model loading)
- Subsequent queries: 10-30 seconds per extraction
- Requires ~16GB RAM
- Works best on machines with high CPU performance

For production use, consider:
- Running on a machine with GPU
- Using a smaller model (7B or 3B parameters)
- Deploying to a server with better hardware

## Supported Entity Types

company, product, service, industry, brand, country, location, organization, person, founder, position, event, action, founding, acquisition, merger, partnership, expansion, restructuring, divestment, sale, bankruptcy, financial_metric, business_concept, revenue, profit, loss, investment, funding, market_share, competition, market_trend, regulation, innovation, sustainability, corporate_social_responsibility, award, date/time, year, period

## Supported Relations

part_of, parent_company_of, subsidiary_of, acquired, divested, owns_brand, holds_stake_in, spun_off, formed_from, founded_by, has_CEO, manufactures, develops, produces, sells, has_product_line, is_a_type_of, is_brand_of, features_technology, uses_material, launched_product, had_revenue_of, had_profit_of, in_year, market_value_of, is_publicly_traded, listed_on_exchange, experienced_growth, occurred_in_year, occurred_on_date, resulted_in, preceded, followed_by, marked_milestone, influenced_by, led_to, was_a_response_to, has_trademark, uses_logo, acquired_trademark_from, is_known_for, launched_campaign

## Project Structure

```
phi4-ie-demo/
├── README.md                    # This file
├── Modelfile                    # Ollama model configuration
├── interactive_ie_demo.py       # Main demo script
├── convert_and_quantize.sh      # (Advanced) Convert HF model to GGUF
└── models/                      # Place quantized model here
    └── phi4_ie_q4_k_m.gguf     # Quantized model (not included)
```

## Advanced: Model Conversion

If you want to convert the HuggingFace model yourself instead of using a pre-quantized version:

1. Install llama.cpp and required dependencies
2. Download the HF model: `FinaPolat/phi4_adaptable_IE`
3. Run: `./convert_and_quantize.sh`

This will convert from HuggingFace format → GGUF F16 → Q4_K_M quantized (27GB → 8.3GB).

## Credits

- Base model: Microsoft Phi-4
- Fine-tuned model: FinaPolat/phi4_adaptable_IE
- Quantization: llama.cpp
- Local inference: Ollama

## License

Model usage subject to Microsoft Phi-4 license terms.
