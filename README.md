# Smart Agent

`smart_agent` is a local, offline-first intelligent agent designed to help with system automation, file management, and personal tasks. It operates entirely on your machine without relying on external APIs or cloud services, ensuring maximum privacy and control.

The agent leverages a local large language model (Mistral 7B) through the Ollama framework to understand natural language commands and execute actions through a variety of integrated tools.

## Key Features

* **Local AI Engine**: Powered by a locally-hosted Mistral 7B model for intelligent responses and task planning.
* **System Monitoring**: Reports on CPU, RAM, and disk usage.
* **File Management**: Find, organize, compress, and decompress files and folders.
* **Security & Privacy**: Provides basic security checks, including project file integrity verification and scanning for suspicious files.
* **Multimedia Processing**: Reads text from PDF documents and extracts text from images using OCR.
* **Task Automation**: Capable of breaking down complex objectives into a sequence of actionable steps.
* **Desktop GUI**: Features a responsive and modern desktop interface built with PyQt6, complete with system notifications.
* **Multilingual Support**: The agent's core logic and interface are designed to support both English and Arabic commands.

## Getting Started

Follow these steps to get your local smart agent up and running.

### Prerequisites

* **Python 3.9+**
* **Git**
* **Ollama**: Download and install Ollama from [ollama.com](https://ollama.com/).
* **Mistral 7B Model**: Run the following command in your terminal to download the model:
    ```bash
    ollama pull mistral
    ```
* **Tesseract OCR**: Install Tesseract-OCR for your operating system.
    * **Windows**: Download from [tesseract-ocr.github.io](https://tesseract-ocr.github.io/tessdoc/Downloads.html).
    * **macOS**: `brew install tesseract`

### Installation

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/your-username/smart_agent.git](https://github.com/your-username/smart_agent.git)
    cd smart_agent
    ```
2.  **Create a virtual environment and install dependencies**:
    ```bash
    python -m venv venv
    # For Windows:
    .\venv\Scripts\activate
    # For macOS/Linux:
    source venv/bin/activate

    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    python app.py
    ```
    The application window will open automatically on your desktop.

## Usage

Interact with the agent through the chat interface. You can use natural language to ask questions or issue commands.

**Example Commands:**

* `What is the capital of France?`
* `monitor system`
* `find file "report.pdf"`
* `organize files`
* `security check`
* `خطط ونفذ: ابحث عن عاصمة فرنسا ثم اذكر عدد سكانها.`

For a full list of commands, use the `help me` or `ساعدني` command within the application, or refer to the [docs/help.md](docs/help.md) file.

## Project Structure