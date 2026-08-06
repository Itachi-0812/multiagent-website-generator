import os
import sys
import subprocess
from pathlib import Path

def setup_and_run_backend():
    backend_dir = Path("output/backend")

    if not backend_dir.exists():
        print("Error: No backend found. Generate a website first with generate_backend=True")
        sys.exit(1)

    env_file = backend_dir / ".env"
    env_example = backend_dir / ".env.example"

    if not env_file.exists() and env_example.exists():
        print("Creating .env file from .env.example...")
        with open(env_example, "r") as f:
            env_content = f.read()
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✓ .env created. Please update it with your configuration.")

    print("\nInstalling backend dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(backend_dir / "requirements.txt")],
        check=True
    )

    print("\nStarting FastAPI backend...")
    print("Backend will be available at http://localhost:8000")
    print("Admin dashboard at http://localhost:8000/admin.html")
    print("API docs at http://localhost:8000/docs")

    os.chdir(backend_dir)
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])

if __name__ == "__main__":
    setup_and_run_backend()
