# 🧪 TESTING GUIDE - LOCAL MODELS

## ✅ CRITICAL CHANGES MADE

**Problem:** Models load successfully but return 0 tokens

**Root Cause Hypothesis:** [INST] tag formatting was incompatible with your model files

**Solution Applied:** Removed ALL formatting, use raw user prompts

---

## 🔄 WHAT TO DO NOW

### Step 1: Restart Server

```bash
# Stop current server (CTRL+C)
python run.py
```

### Step 2: Watch Server Logs Carefully

Look for this when server starts:
```
⚡ Loading Mistral-7B with SPEED OPTIMIZATIONS...
✅ Mistral-7B loaded - BEST general chat quality!
```

### Step 3: Test Simple Message

1. Open browser: http://localhost:8000
2. Click **"New Chat"**
3. Send message: **"hello"**

### Step 4: Check Server Console

You should now see:
```
🚀 Starting streaming response for model: auto
📡 Got generator: <class 'generator'>
🔄 Mistral streaming started...
🎯 Mistral RAW prompt: 'hello'
🎯 Mistral formatted prompt: 'hello'
🧪 Sending test token...
📦 Token 1: 'Hello'
📦 Token 2: '!'
📦 Token 3: ' How'
...
✅ Mistral streaming done: X real tokens
```

---

## 🎯 KEY CHANGES

### Before (Broken):
```python
formatted_prompt = "[INST] hello [/INST]"
response = model(formatted_prompt, stream=True)
# Returns 0 tokens!
```

### After (Fixed):
```python
formatted_prompt = "hello"  # RAW prompt
response = model(formatted_prompt, stream=True)
# Should return tokens!
```

---

## 📊 EXPECTED OUTCOMES

### Scenario A: NOW WORKS! ✅

**Server logs:**
```
📦 Token 1: 'Hello'
📦 Token 2: '!'
📦 Token 3: ' How'
✅ Streaming complete: 15 tokens
```

**Browser shows:** Tokens streaming in real-time! 🎉

**This means:** [INST] formatting WAS the problem!

### Scenario B: Still 0 Tokens ❌

**Server logs:**
```
🧪 Sending test token...
⚠️  Generator completed with 0 tokens! Using fallback...
📝 Fallback word 1: ...
```

**Browser shows:** Fallback response

**This means:** Issue is deeper - likely model file format or llama-cpp version incompatibility

---

## 🔍 IF STILL 0 TOKENS

### Check 1: Model File Integrity

```bash
# Check file sizes
ls -lh models/*.gguf

# Should see:
# Mistral-7B-Instruct-v0.3-Q4_K_M.gguf    (~4.4GB)
# codellama-13b-instruct.Q4_K_M.gguf      (~7.87GB)
# Meta-Llama-3-8B-Instruct-Q4_K_M.gguf    (~4.92GB)
# openhermes-2.5-mistral-7b.Q4_K_M.gguf   (~4.4GB)
```

If files are much smaller → incomplete download!

### Check 2: llama-cpp-python Version

```bash
python3 -c "import llama_cpp; print(llama_cpp.__version__)"
```

Should be: `0.2.x` or higher

If older → update:
```bash
pip install --upgrade llama-cpp-python
```

### Check 3: Model Loading Parameters

Add to MistralAdapter.__init__:
```python
print(f"🔧 Loading with:")
print(f"   n_ctx: 2048")
print(f"   n_threads: 8")
print(f"   n_gpu_layers: 0")
```

### Check 4: Test Non-Streaming Mode

Add temporary test in MistralAdapter.generate:
```python
# Test non-streaming first
print(f"🧪 Testing non-streaming mode...")
test_response = self.model("Hello", max_tokens=20, stream=False)
print(f"📝 Non-stream result: {test_response}")
```

If non-streaming works but streaming doesn't → llama-cpp streaming issue

---

## 🛠️ ADVANCED DEBUGGING

### Enable Verbose Mode

In MistralAdapter.__init__, change:
```python
verbose=False  # Change to True
```

This will show detailed llama.cpp logs.

### Try Different Models

Test each model separately:
```python
# In routes.py or test script
models_to_test = ['mistral', 'codellama', 'llama3', 'hermes']
for model_name in models_to_test:
    response = get_model_response("hello", model_name, stream=False)
    print(f"{model_name}: {response}")
```

### Check Generation Parameters

Try simplest parameters:
```python
response = self.model(
    prompt,
    max_tokens=10,  # Very small
    temperature=1.0,  # Default
    stream=False  # No streaming
)
```

---

## 📝 REPORT RESULTS

After testing, please share:

1. **Server startup logs:**
   - Did models load? (✅ or ❌)
   
2. **When you send "hello", server shows:**
   - Test token appears? (🧪)
   - Real tokens appear? (📦)
   - Fallback triggered? (📝)
   
3. **Browser shows:**
   - "Testing... " appears?
   - Real tokens streaming?
   - Fallback message?

4. **Model file sizes:**
   ```bash
   ls -lh models/*.gguf
   ```

5. **llama-cpp-python version:**
   ```bash
   pip show llama-cpp-python
   ```

---

## 🎯 MOST LIKELY SCENARIOS

### Scenario 1: Works Now! ✅
**Cause:** [INST] formatting was incompatible
**Solution:** Using raw prompts fixed it
**Action:** Enjoy real AI streaming! 🎉

### Scenario 2: Still 0 Tokens ❌
**Possible causes:**
- Model file corrupted/incomplete
- llama-cpp-python version incompatible
- Model requires specific prompt format we haven't tried
- streaming=True parameter not working in llama-cpp version

**Next steps:**
1. Test non-streaming mode
2. Update llama-cpp-python
3. Try simplest parameters
4. Test other models

---

## 💡 QUICK WINS TO TRY

### Try 1: Update llama-cpp-python
```bash
pip install --upgrade llama-cpp-python
python run.py
```

### Try 2: Increase max_tokens
In model_service.py, change:
```python
max_tokens=512  # Try 1024 or 2048
```

### Try 3: Disable stop tokens (already done)
```python
stop=[]  # Already set
```

### Try 4: Test with longer prompt
Instead of "hello", try:
```
"Please write a short greeting message."
```

Sometimes longer prompts work better!

---

## 🔥 EMERGENCY FALLBACK

If NOTHING works after all tests:

**Option A:** Use non-streaming mode temporarily
```python
# In routes.py, change stream_message() to use stream=False
response = get_model_response(..., stream=False)
# Then send complete response at once
```

**Option B:** Try different model files
- Phi-2 (smaller, often more compatible)
- TinyLlama (very lightweight)
- Different quantization (Q5_K_M instead of Q4_K_M)

**Option C:** Check model file source
- Re-download from HuggingFace
- Verify SHA256 checksums
- Try different mirror

---

## ✅ SUCCESS CRITERIA

**You know it's working when:**
1. Server logs show "📦 Token X: ..." with actual text
2. Browser shows tokens appearing one-by-one
3. No fallback messages
4. Response is coherent and relevant
5. Different questions get different answers

**TEST WITH:**
- Simple: "hello"
- Question: "what is the capital of France?"
- Indonesian: "siapa presiden Indonesia?"
- Code: "write a Python hello world"

All should stream tokens in real-time! 🚀

---

Good luck with testing! 🎯✨
