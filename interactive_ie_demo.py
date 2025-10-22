#!/usr/bin/env python3
"""
Interactive Information Extraction Demo using Ollama
Text → NER → RE → Triples (No disambiguation, completely local)
"""

import json
import requests
import sys

# Ollama configuration
OLLAMA_API = "http://localhost:11434/api/chat"
MODEL_NAME = "jankalo/phi4-ie"

# Hardcoded schemas from the existing input files
ENTITY_TYPES = [
    "company", "product", "service", "industry", "brand", "country", "location",
    "organization", "person", "founder", "position", "event", "action",
    "founding", "accusition", "merger", "partnership", "expansion",
    "restructuring", "divestment", "sale", "bankruptcy", "financial_metric",
    "business_concept", "revenue", "profit", "loss", "investment", "funding",
    "market_share", "competition", "market_trend", "regulation", "innovation",
    "sustainability", "corporate_social_responsibility", "award", "date/time",
    "year", "period"
]

RELATIONS = [
    "part_of", "parent_company_of", "subsidiary_of", "acquired", "divested",
    "owns_brand", "holds_stake_in", "spun_off", "formed_from", "founded_by",
    "has_CEO", "manufactures", "develops", "produces", "sells", "has_product_line",
    "is_a_type_of", "is_brand_of", "features_technology", "uses_material",
    "launched_product", "had_revenue_of", "had_profit_of", "in_year",
    "market_value_of", "is_publicly_traded", "listed_on_exchange",
    "experienced_growth", "occurred_in_year", "occurred_on_date", "resulted_in",
    "preceded", "followed_by", "marked_milestone", "influenced_by", "led_to",
    "was_a_response_to", "has_trademark", "uses_logo", "acquired_trademark_from",
    "is_known_for", "launched_campaign"
]

# Prompt template
PROMPT_TEMPLATE = """Information Extraction is the process of automatically identifying and extracting structured information from unstructured text data. The goal is to transform raw text into meaningful data that can be easily analyzed and used in various applications. Named Entity Recognition (NER) and Relation Extraction are two common tasks in Information Extraction.

Named Entity Recognition involves identifying and classifying named entities such as people, organizations, locations, and other domain-specific concepts. Relation Extraction involves identifying and extracting relationships between entities.

The task at hand is {task}.

Here is an example of task execution:

{example}

Analyze the text and targets carefully, identify relevant information.

Extract the information in the following format: `{output_format}`. If no matching entities are found, return an **empty list**. Please provide only the extracted information without any explanations.

Schema: {schema}
Text: {inputs}
"""


def query_ollama(prompt):
    """Query Ollama API"""
    system_message = "You are a helpful AI assistant specializing in Information Extraction (IE) tasks such as Named Entity Recognition (NER) or Relation Extraction (RE). Analyze the following text and provide the requested information."

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {
            "temperature": 0.001,
            "num_predict": 8192
        }
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=300)
        response.raise_for_status()
        result = response.json()
        return result['message']['content']
    except Exception as e:
        print(f"❌ Error querying Ollama: {e}", file=sys.stderr)
        return None


def extract_entities(text):
    """Extract entities from text using NER"""
    example = {
        "text": "Adidas AG is a German multinational corporation, founded and headquartered in Herzogenaurach, Germany, that designs and manufactures shoes, clothing and accessories.",
        "extracted_entities": [
            ["Adidas AG", "company"],
            ["German", "country"],
            ["Herzogenaurach", "location"],
            ["Germany", "country"],
            ["shoes", "product"],
            ["clothing", "product"],
            ["accessories", "product"]
        ]
    }

    prompt = PROMPT_TEMPLATE.format(
        task="NER: Named Entity Recognition",
        example=json.dumps(example, indent=2),
        schema=json.dumps(ENTITY_TYPES),
        inputs=text,
        output_format='[["Entity", "Type"], ...]'
    )

    print("\n🔍 Extracting entities...")
    result = query_ollama(prompt)

    if result:
        try:
            entities = json.loads(result)
            return entities
        except json.JSONDecodeError:
            print(f"⚠️  Failed to parse NER output as JSON: {result}")
            return []
    return []


def extract_relations(text):
    """Extract relations from text using RE"""
    example = {
        "text": "Adidas AG is a German multinational corporation, founded and headquartered in Herzogenaurach, Germany.",
        "extracted_relations": [
            ["Adidas AG", "founded_by", "Adolf Dassler"],
            ["Adidas AG", "part_of", "Germany"]
        ]
    }

    # Convert relations list to dict format for the prompt
    relations_dict = [{"relation": r} for r in RELATIONS]

    prompt = PROMPT_TEMPLATE.format(
        task="RE: Relation Extraction",
        example=json.dumps(example, indent=2),
        schema=json.dumps(relations_dict),
        inputs=text,
        output_format='[["Subject", "Relation", "Object"], ...]'
    )

    print("🔗 Extracting relations...")
    result = query_ollama(prompt)

    if result:
        try:
            relations = json.loads(result)
            return relations
        except json.JSONDecodeError:
            print(f"⚠️  Failed to parse RE output as JSON: {result}")
            return []
    return []


def display_results(text, entities, relations):
    """Display extraction results in a nice format"""
    print("\n" + "="*80)
    print("📄 INPUT TEXT")
    print("="*80)
    print(text)

    print("\n" + "="*80)
    print("🏷️  ENTITIES EXTRACTED")
    print("="*80)
    if entities:
        for entity, entity_type in entities:
            print(f"  • {entity:30} → {entity_type}")
    else:
        print("  (No entities found)")

    print("\n" + "="*80)
    print("🔗 RELATIONS EXTRACTED")
    print("="*80)
    if relations:
        for subj, rel, obj in relations:
            print(f"  • {subj:20} --[ {rel} ]--> {obj}")
    else:
        print("  (No relations found)")

    print("\n" + "="*80)
    print("📊 TRIPLES (Subject-Predicate-Object)")
    print("="*80)
    if relations:
        for subj, rel, obj in relations:
            print(f"  ({subj}, {rel}, {obj})")
    else:
        print("  (No triples found)")
    print("="*80 + "\n")


def save_results(text, entities, relations, filename="ie_output.json"):
    """Save results to JSON file"""
    output = {
        "text": text,
        "entities": entities,
        "relations": relations,
        "triples": [[s, r, o] for s, r, o in relations]
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"💾 Results saved to: {filename}")


def check_ollama():
    """Check if Ollama is running and model exists"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = [m['name'] for m in response.json()['models']]

        if MODEL_NAME not in models:
            print(f"❌ Error: Model '{MODEL_NAME}' not found in Ollama")
            print(f"\nAvailable models: {models}")
            print(f"\nPlease create the model first:")
            print(f"  1. Wait for model download to complete")
            print(f"  2. Run: ./convert_and_quantize.sh")
            print(f"  3. Run: ollama create {MODEL_NAME} -f Modelfile")
            sys.exit(1)

        print(f"✅ Ollama is running with model: {MODEL_NAME}\n")
        return True

    except Exception as e:
        print(f"❌ Error: Cannot connect to Ollama")
        print(f"Make sure Ollama is running: brew services start ollama")
        print(f"Error details: {e}")
        sys.exit(1)


def main():
    """Main interactive loop"""
    print("="*80)
    print(" "*20 + "📝 Interactive IE Demo - Ollama")
    print("="*80)
    print(f"\nModel: {MODEL_NAME}")
    print("Task: Extract entities and relations from text")
    print("No disambiguation - completely local!\n")

    check_ollama()

    print("Enter text to analyze (or 'quit' to exit)")
    print("For multi-line input, enter '###' on a new line when done\n")

    while True:
        print("-" * 80)
        print("📝 Enter text:")

        # Read input (support multi-line)
        lines = []
        while True:
            try:
                line = input()
                if line.strip().lower() == 'quit':
                    print("\n👋 Goodbye!")
                    sys.exit(0)
                if line.strip() == '###':
                    break
                lines.append(line)
            except EOFError:
                sys.exit(0)

        text = " ".join(lines).strip()

        if not text:
            print("⚠️  No text entered. Please try again.\n")
            continue

        # Extract entities and relations
        entities = extract_entities(text)
        relations = extract_relations(text)

        # Display results
        display_results(text, entities, relations)

        # Ask to save
        save = input("💾 Save results to file? (y/n): ").strip().lower()
        if save == 'y':
            filename = input("Filename (default: ie_output.json): ").strip()
            if not filename:
                filename = "ie_output.json"
            save_results(text, entities, relations, filename)

        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
