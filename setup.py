import json
import shutil
import subprocess

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
    print("LLM Assistant Wrapper - first-time setup\n")

    ram = get_total_ram()
    vram = get_vram()
    print(f"system RAM: {ram} GB")
    print(f"GPU VRAM: {vram if isinstance(vram, str) else str(vram) + ' MB'}\n")

    if not check_ollama():
        print("error: 'ollama' is not installed. Please install it from https://ollama.com and try again.")
        return

    assistant_name = prompt_input("enter assistant name", default="Nova")
    personality = prompt_input("enter personality prompt (optional)", default="You are a friendly, helpful, and clear assistant. You respond politely and concisely, making complex ideas easy to understand. You adapt your tone to be warm and approachable, and you always stay professional.")
    language = prompt_input("set default language (optional)", default="en")

    print("\nmodel setup:")
    model_choices = {
        "1": ("llama3", 8000),
        "2": ("mistral", 6000),
        "3": ("gemma:2b", 3000),
        "4": ("none", 0)
    }

    for key, (name, _) in model_choices.items():
        print(f"{key}. {name}")

    choice = input("choose a model to use or install later [1-4]: ").strip()
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
        "assistant_name": assistant_name,
        "personality_prompt": personality,
        "default_language": language,
    }

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        print(f"\nconfiguration saved to {config_path}")

if __name__ == "__main__":
    initialize_wrapper()
