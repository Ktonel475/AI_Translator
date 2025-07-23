import subprocess

def check_ollama_cli():
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            print(f"Error: {result.stderr.strip()}")
            return False
        return True
    except FileNotFoundError:
        print("Ollama CLI not found.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
