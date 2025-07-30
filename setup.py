import json
import shutil
import subprocess
import os

def get_total_ram():
    try:
        import psutil
        return round(psutil.virtual_memory().total / (1024**3), 2)  # in GB
    except ImportError:
        return "unknown (psutil not installed)"

def get_vram():
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            return round(gpus[0].memoryTotal, 2)  # in MB
    except ImportError:
        return "unknown (GPUtil not installed)"
    return "not detected"

def check_ollama():
    return shutil.which("ollama") is not None

def prompt_input(prompt, default=None):
    if default is not None:
        res = input(f"{prompt} [{default}]: ").strip()
        return res if res else default
    else:
        res = ""
        while not res:
            res = input(f"{prompt}: ").strip()
        return res

def warn_for_model(model_name, vram_required):
    vram = get_vram()
    if isinstance(vram, float) and vram < vram_required:
        print(f"warning: your VRAM ({vram} MB) may be insufficient for {model_name} (requires ~{vram_required} MB).")
    elif isinstance(vram, str):
        print(f"warning: VRAM check skipped: {vram}")

def install_model(model_name):
    print(f"installing model '{model_name}' via 'ollama pull'...")
    subprocess.run(["ollama", "pull", model_name])

def initialize_wrapper():
    config_path = "config.json"
    if os.path.exists(config_path):
        confirm = input(f"{config_path} already exists. Do you want to overwrite it? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Setup aborted.")
            return
        
    print("LLM Assistant Wrapper - first-time setup\n")

    ram = get_total_ram()
    vram = get_vram()
    print(f"system RAM: {ram} GB")
    print(f"GPU VRAM: {vram if isinstance(vram, str) else str(vram) + ' MB'}\n")

    if not check_ollama():
        print("error: 'ollama' is not installed. Please install it from https://ollama.com and try again.")
        return

    language = prompt_input("set default language (optional)", default="en")

    print("\nmodel setup:")
    model_choices = {
        "1": ("llama3.1", 8000),
        "2": ("mistral7b", 6000),
        "3": ("mistral12b", 8000),
        "4": ("mixtral8x7b", 8000),
        "5": ("mixtral8x22b", 8000),
        "6": ("smollm2-135m", 2048),
        "7": ("smollm2-360m", 2048),
        "8": ("smollm2-1.7b", 2048),
        "9": ("qwen2.5-vl", 8192),
        "10": ("gemma3", 4096),
        "11": ("deepseek-r1", 2048),
        "12": ("starcoder2-3b", 4096),
        "13": ("starcoder2-7b", 4096),
        "14": ("starcoder2-15b", 4096),
        "15": ("command-r-35b", 8192),
        "16": ("wizardlm2-7b", 8192),
        "17": ("wizardlm2-8x22b", 8192),
        "18": ("llava", 4096),
        "19": ("none", 0)
    }

    for key, (name, _) in model_choices.items():
        print(f"{key}. {name}")

    choice = input("choose a model to use or install later [1-19]: ").strip()
    if choice not in model_choices:
        print("error: invalid choice. aborting.")
        return

    model_name, required_vram = model_choices[choice]
    if model_name != "none":
        warn_for_model(model_name, required_vram)
        confirm = prompt_input(f"install {model_name} now? (y/N)", default="n")
        if confirm.lower() == 'y':
            install_model(model_name)

    config = {
        "Model": model_name,
        "default_language": language,
    }

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        print(f"\nconfiguration saved to {config_path}")

if __name__ == "__main__":
    initialize_wrapper()
