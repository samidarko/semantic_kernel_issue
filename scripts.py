"""
Poetry commands
"""
import subprocess


def cli():
    """
    Run the app
    """
    subprocess.run(["python", "-m", "semantic_kernel_issue"], check=False)


