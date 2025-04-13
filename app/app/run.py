import sys
import subprocess


def main():
    """
    Main entry point for SignalForge.
    Runs CLI if arguments provided,
    else runs the API server.
    """
    if len(sys.argv) > 1:
        # Run CLI Mode
        from cli.main import main as cli_main
        cli_main()
    else:
        # Run API Mode (FastAPI)
        print("Starting SignalForge API...")
        subprocess.run(["python3", "api/server.py"])


if __name__ == "__main__":
    main()
