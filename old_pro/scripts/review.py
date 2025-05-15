from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Load model on CPU
model_id = "deepseek-ai/deepseek-coder-1.3b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",             # Force CPU to avoid OOM
    torch_dtype="auto"
)

# Set up pipeline (no device argument)
code_reviewer = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Example diff
diff = """
diff --git a/main.py b/main.py
index e69de29..4b825dc 100644
--- a/main.py
+++ b/main.py
@@ def hello():
-    print("Hello")
+    print("Hello, world!")
"""

# Prompt the model
prompt = f"""
You are a professional AI code reviewer.
Analyze this diff and provide:
- A short summary
- Review by blocks (functions, classes)
- Efficiency, naming, modularity, reusability
- Any security risks or dependency issues

Code Diff:
{diff}
"""

# Generate response
output = code_reviewer(prompt, max_new_tokens=512, do_sample=True)[0]["generated_text"]
generated = output[len(prompt):].strip()

# Print result
print("\n=== AI Code Review ===\n")
print(generated)
