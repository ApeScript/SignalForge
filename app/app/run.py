import sys
import subprocess
import os


def main():
    """
    Main entry point for SignalForge.

    - Runs CLI mode if command-line arguments are provided.
    - Otherwise runs the FastAPI server for API usage.
    """

    # Detect if CLI mode (any additional arguments given)
    if len(sys.argv) > 1:
        # Run CLI Mode (dynamic import to avoid unnecessary loading)
        try:
            from cli.main import main as cli_main
            cli_main()
        except ImportError as e:
            print(f"[ERROR] Failed to load CLI module: {e}")
            sys.exit(1)

    else:
        # Run API Mode (FastAPI server)
        print("Starting SignalForge API...")

        # Auto-detect correct Python executable (python / python3)
        python_exec = sys.executable or "python3"

        # Build API server command
        command = [python_exec, os.path.join("api", "server.py")]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to start API server: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
