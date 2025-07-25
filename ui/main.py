from ui.gradio_app import launch_app
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv(override=True)
    launch_app()