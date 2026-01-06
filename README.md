# Steps to follow 

IMPORTANT : A **Local langauge model** is used with llama cpp framework ( as I lack gpu compute), the model can be downloaded from : https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF and then the path for it should be replaced at `MODEL_PATH` of `llm_llamacpp.py` file 

1. `pip install -r requirements.txt`
2. `sqlite3 output/asana_simulation.sqlite < schema.sql`
3. `python3 src/main.py`

