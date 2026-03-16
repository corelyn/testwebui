# Corelyn TestWebUI
A WebUi to test MLM's

# Setup
Requires **Python +3.9**
## Endpoint
Clone with :
```git
git clone https://github.com/corelyn/testwebui.git
cd testwebui
```

When you create a MLM by yourself or with [MLMConstruct](https://corelyn.github.io/mlmconstruct/) you should get a folder like :
```
- MyModel
|_ config.json
|_ generation_config.json
|_ model.safetensors
|_ tokenizer_config.json
|_ tokenizer.json
|_ training_args.bin
```

If you have one place it in the **testwebui** folder and if you don't you can make one using [MLMConstruct](https://corelyn.github.io/mlmconstruct/) and come back to this.

Now dependencies :
```pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 # Cuda
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu # Cpu
pip install transformers
pip install flask
```

And now you can run :
```python
python endpoint.py C:/Path/to/Model/Folder/
```

## Web UI
Clone with :
```git
git clone https://github.com/corelyn/testwebui.git
cd testwebui
```

Now dependencies :
```pip
pip install gradio requests
```

You can modify this(in corelyn_testui.py) :
```python
demo.launch(share=False)
```
to this :
```python
demo.launch(share=True)
```
to make the URL public and modify this with your link :
```python
API_URL = "http://192.168.0.136:5000/chat/completions" # Replace link here
```
If you wnat you can modify the logo in the **images** folder

Now you can start by running :
```python
python corelyn_testui.py
```

Bye!




