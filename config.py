import json
import os
import subprocess
import sys

def load_config(path="config.json"):
    try:
        if os.path.exists(path):
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                return config
        else:
            print("No config.json found.")
            answer = input("Do you want to create one now? (y/n): ").strip().lower()
            if answer == 'y':
                print("Running setup.py to create config...")
                subprocess.run([sys.executable, "setup.py"])
                # After setup.py finishes, try loading again
                if os.path.exists(path):
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            config = json.load(f)
                            return config
                    except Exception as e:
                        print(f"Failed to load config after setup: {e}")
                        return {}
                else:
                    print("Config file still not found after setup.")
                    return {}
            else:
                print("No config created. Using default configuration.")
                return {}
    except Exception as e:
        print(f"Failed to load config.json: {e}")
