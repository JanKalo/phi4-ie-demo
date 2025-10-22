#!/bin/bash
# Script to convert HF model to GGUF and quantize for Ollama

set -e  # Exit on error

echo "=== Converting phi4_adaptable_IE to GGUF and quantizing ==="
echo "Start time: $(date)"

# Paths
HF_MODEL_DIR="./models/phi4_ie_hf"
GGUF_OUTPUT="./models/phi4_ie_f16.gguf"
QUANTIZED_OUTPUT="./models/phi4_ie_q4_k_m.gguf"
LLAMA_CPP_DIR="./llama.cpp"

# Check if HF model exists
if [ ! -d "$HF_MODEL_DIR" ]; then
    echo "Error: HuggingFace model not found at $HF_MODEL_DIR"
    echo "Please run the download first"
    exit 1
fi

# Step 1: Convert to GGUF (f16 precision)
echo ""
echo "=== Step 1: Converting to GGUF (f16) ==="
/Users/jan/opt/anaconda3/envs/ollama_convert/bin/python $LLAMA_CPP_DIR/convert_hf_to_gguf.py \
    $HF_MODEL_DIR \
    --outfile $GGUF_OUTPUT \
    --outtype f16

echo "✅ GGUF conversion complete"
ls -lh $GGUF_OUTPUT

# Step 2: Quantize to Q4_K_M
echo ""
echo "=== Step 2: Quantizing to Q4_K_M ==="
$LLAMA_CPP_DIR/build/bin/llama-quantize \
    $GGUF_OUTPUT \
    $QUANTIZED_OUTPUT \
    Q4_K_M

echo "✅ Quantization complete"
ls -lh $QUANTIZED_OUTPUT

# Step 3: Cleanup intermediate file
echo ""
echo "=== Step 3: Cleaning up ==="
rm -f $GGUF_OUTPUT
echo "✅ Removed intermediate f16 GGUF file"

echo ""
echo "=== Conversion complete! ==="
echo "End time: $(date)"
echo ""
echo "Quantized model ready at: $QUANTIZED_OUTPUT"
echo "Model size: $(du -h $QUANTIZED_OUTPUT | cut -f1)"
echo ""
echo "Next steps:"
echo "1. Create Ollama model: ollama create phi4-ie -f Modelfile"
echo "2. Test the model: ollama run phi4-ie"
