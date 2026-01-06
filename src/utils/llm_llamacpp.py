from llama_cpp import Llama
from pathlib import Path


MODEL_PATH = Path("/home/adityasr7/llama.cpp/models/Llama-3.2-1B-Instruct-Q8_0.gguf")

if not MODEL_PATH.exists():
    raise ValueError(f"Model path does not exist: {MODEL_PATH}")

llm = Llama(
    model_path=str(MODEL_PATH),
    n_ctx=2048,
    n_threads=8,
    n_batch=256,
    verbose=False,
)

def llm_generate(prompt, **kwargs):
    """
    Local llama.cpp text generation.
    """
    max_tokens = kwargs.get("max_tokens", 128)
    temperature = kwargs.get("temperature", 0.7)
    top_p = kwargs.get("top_p", 0.9)

    output = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stop=["</s>"],
    )

    return output["choices"][0]["text"].strip()
