import os

key_value = None
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")

def env(key: str, default: str | None = None) -> str | None:
    global key_value
    if key_value is None:
        key_value = {}
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        key_value[k.strip()] = v.strip().strip('"\'')

    return key_value.get(key, os.environ.get(key, default))