---
tags:
  - ollama
  - ai
  - local-ai
---
# Ollama Testing and Benchmarking

<div class="kb-summary">
This page covers testing Ollama with the CLI and REST API, benchmarking inference speed, comparing models, and validating API compatibility.

*Applies to: Ollama*
</div>

```d2
direction: down

basic_cli_testing: "Basic CLI Testing" {shape: rectangle}
rest_api_testing_with_curl: "REST API Testing with curl" {shape: rectangle}
streaming_responses: "Streaming Responses" {shape: rectangle}
benchmarking_throughput: "Benchmarking Throughput" {shape: rectangle}
model_comparison_script: "Model Comparison Script" {shape: rectangle}
performance_reference_table: "Performance Reference Table" {shape: rectangle}

basic_cli_testing -> rest_api_testing_with_curl: uses
rest_api_testing_with_curl -> streaming_responses: uses
streaming_responses -> benchmarking_throughput: uses
benchmarking_throughput -> model_comparison_script: uses
model_comparison_script -> performance_reference_table: uses
```

## Basic CLI Testing

```bash
# Interactive chat
ollama run llama3.1:8b

# Single-shot non-interactive prompt
ollama run llama3.1:8b "Explain TCP/IP in one paragraph"

# Pipe input
echo "What is 2+2?" | ollama run llama3.1:8b

# Read from file
ollama run llama3.1:8b < prompt.txt

# Multi-line prompt
ollama run llama3.1:8b "$(cat << 'EOF'
You are a helpful assistant.
Question: What are the main differences between TCP and UDP?
EOF
)"
```


```text title="Expected output"
>>> Send a message (/help for help)
What is the capital of France?
The capital of France is Paris, a city located in the north-central part of the country along the Seine River. Paris is known for its iconic landmarks, rich history, and cultural significance.

>>> Send a message (/help for help)
/bye

Explain TCP/IP in one paragraph
TCP/IP (Transmission Control Protocol/Internet Protocol) is the fundamental suite of communication protocols used for transmitting data across networks and the internet. TCP ensures reliable, ordered delivery of data by establishing connections between devices, while IP handles the routing and logical addressing of packets across networks. Together, they form the backbone of modern networking, enabling everything from web browsing and email to video streaming and cloud services.

What is 2+2?
2 + 2 = 4. This is a basic arithmetic operation where two quantities of two are combined to produce a sum of four.

You are a helpful assistant.
Question: What are the main differences between TCP and UDP?
TCP (Transmission Control Protocol) and UDP (User Datagram Protocol) are both transport layer protocols, but they differ significantly. TCP is connection-oriented, reliable, and ordered, making it suitable for applications like email and file transfer where accuracy is critical. UDP, conversely, is connectionless and faster but offers no delivery guarantees, making it ideal for real-time applications like video streaming and online gaming where speed matters more than perfect accuracy.
```

!!! warning "Common errors"
    **`Error: model "llama3.1:8b" not found, try pulling it first`** — Run `ollama pull llama3.1:8b` to download the model before executing commands.
    **`Error: connection refused`** — Start the Ollama service with `ollama serve` in another terminal or ensure the Ollama daemon is running.
    **`Error: read "prompt.txt": no such file or directory`** — Verify the prompt file exists in the current directory with `ls -la prompt.txt` before piping it.
## REST API Testing with curl

The Ollama REST API is compatible with the OpenAI API format.

```bash
# Generate (non-chat) completion
curl http://localhost:11434/api/generate \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "What is Kubernetes?",
    "stream": false
  }' | jq '.response'

# Chat completion (OpenAI-compatible)
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "messages": [
      {"role": "system", "content": "You are a concise assistant."},
      {"role": "user", "content": "What is a container?"}
    ],
    "temperature": 0.7,
    "max_tokens": 256
  }' | jq '.choices[0].message.content'

# List available models
curl http://localhost:11434/api/tags | jq '.models[].name'

# Check running model status
curl http://localhost:11434/api/ps | jq
```


```text title="Expected output"
"Kubernetes is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications across clusters of machines. It provides declarative configuration and automation for container lifecycle management."

"A container is a lightweight, standalone, executable package that includes an application and all its dependencies—libraries, runtime, and system tools. Containers provide process isolation and consistent environments across development, testing, and production."

llama3.1:8b
mistral:7b
neural-chat:7b

{
  "models": [
    {
      "name": "llama3.1:8b",
      "model": "llama3.1:8b",
      "size": 4887990272,
      "digest": "sha256:6a0746a1ec1aef3e7cf8e96b826ea6d61d083da1d5ade757076fcebe8290ff89",
      "details": {
        "format": "gguf",
        "family": "llama",
        "families": ["llama"],
        "parameter_size": "8B",
        "quantization_level": "Q4_0"
      }
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to localhost port 11434: Connection refused`** — Ensure Ollama is running with `ollama serve` or verify it's listening on port 11434 with `netstat -tuln | grep 11434`.
    **`jq: parse error: Cannot index number with string "response"`** — The model may still be loading; wait a few seconds and retry, or check that the model is fully downloaded with `ollama list`.
    **`error: "model 'llama3.1:8b' not found"`** — Pull the required model first using `ollama pull llama3.1:8b`.
## Streaming Responses

```python
import requests, json

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.1:8b", "prompt": "Write a haiku about GPUs"},
    stream=True
)

for line in response.iter_lines():
    if line:
        chunk = json.loads(line)
        print(chunk.get("response", ""), end="", flush=True)
        if chunk.get("done"):
            print()
            print(f"\nTokens: {chunk['prompt_eval_count']} prompt, {chunk['eval_count']} generated")
            print(f"Speed: {chunk['eval_count'] / (chunk['eval_duration'] / 1e9):.1f} tokens/sec")
```

## Benchmarking Throughput

```bash
# Simple throughput test using time
time ollama run llama3.1:8b "Write 500 words about machine learning" --nowordwrap > /dev/null

# Measure tokens per second from API response stats
curl -s http://localhost:11434/api/generate \
  -d '{"model":"llama3.1:8b","prompt":"Count from 1 to 100","stream":false}' \
  | jq '{
    tokens_per_sec: (.eval_count / (.eval_duration / 1e9)),
    prompt_tokens: .prompt_eval_count,
    output_tokens: .eval_count,
    total_duration_s: (.total_duration / 1e9)
  }'
```


```text title="Expected output"
real	42.387s
user	0.156s
sys	0.089s
{
  "tokens_per_sec": 18.42,
  "prompt_tokens": 12,
  "output_tokens": 756,
  "total_duration_s": 41.03
}
```

!!! warning "Common errors"
    **`error: model 'llama3.1:8b' not found, try pulling it first`** — Run `ollama pull llama3.1:8b` before executing the test.
    **`curl: (7) Failed to connect to localhost port 11434: Connection refused`** — Ensure the Ollama service is running with `ollama serve` in another terminal or as a background service.
    **`jq: parse error: Invalid numeric literal at line 1 column 7`** — Verify the API response is valid JSON by testing `curl -s http://localhost:11434/api/generate -d '{"model":"llama3.1:8b","prompt":"test","stream":false}'` without piping to jq first.
## Model Comparison Script

```python
import requests, time, json

MODELS = ["llama3.1:8b", "mistral:7b", "phi3:mini"]
PROMPT = "Explain what a neural network is in 3 sentences."

results = []
for model in MODELS:
    start = time.time()
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": PROMPT, "stream": False}
    ).json()
    elapsed = time.time() - start

    tps = resp["eval_count"] / (resp["eval_duration"] / 1e9)
    results.append({
        "model": model,
        "tokens": resp["eval_count"],
        "tokens_per_sec": round(tps, 1),
        "total_sec": round(elapsed, 2),
        "response": resp["response"][:150]
    })

# Print comparison table
print(f"{'Model':<25} {'Tokens':>7} {'T/s':>8} {'Time(s)':>9}")
print("-" * 55)
for r in results:
    print(f"{r['model']:<25} {r['tokens']:>7} {r['tokens_per_sec']:>8} {r['total_sec']:>9}")
```

## Performance Reference Table

Approximate tokens/sec on common hardware (Q4_K_M, context=2048):

| Model | RTX 3060 12GB | RTX 4090 | A10G | A100 80GB |
|---|---|---|---|---|
| 7B / 8B | ~50 t/s | ~110 t/s | ~80 t/s | ~180 t/s |
| 13B | ~28 t/s | ~65 t/s | ~45 t/s | ~120 t/s |
| 30B–34B | OOM | ~30 t/s | OOM | ~55 t/s |
| 70B | OOM | OOM | OOM | ~28 t/s |

## Embeddings API

```bash
curl http://localhost:11434/api/embed \
  -d '{
    "model": "nomic-embed-text",
    "input": "The sky is blue"
  }' | jq '.embeddings[0] | length'
```


```text title="Expected output"
384
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to localhost port 11434: Connection refused`** — Ensure the Ollama service is running with `ollama serve` or check that it's listening on port 11434.
    **`jq: parse error: Cannot index number with string "embeddings"`** — The model may not support embeddings or returned an error; verify the model exists with `ollama list` and that `nomic-embed-text` is pulled.
    **`jq: error (at <stdin>:1): Cannot iterate over null (null)`** — The API response doesn't contain the expected `embeddings` field; check the Ollama API response with `curl http://localhost:11434/api/embed -d '{"model":"nomic-embed-text","input":"test"}'` to inspect the actual structure.