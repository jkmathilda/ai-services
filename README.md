# GenieGPT

This web application, featuring GPT functionalities such as a chatbot, document analyzer, text-to-speech, and vision capabilities, is a dynamic platform. It's designed for regular updates to incorporate new features, ensuring continuous improvement and alignment with evolving digital needs.

![Image](https://github.com/jkmathilda/gpt-GenieGPT/assets/142202145/79fdd76d-8c36-486c-8583-62ca50c10ada)

# Getting Started

To get started with this project, you'll need to clone the repository and set up a virtual environment. This will allow you to install the required dependencies without affecting your system-wide Python installation.

### Cloning the Repository

    git clone https://github.com/jkmathilda/gpt-GenieGPT.git

### Setting up a Virtual Environment

    cd ./gpt-GenieGPT

    pyenv versions

    pyenv local 3.11.6

    echo '.env'  >> .gitignore
    echo '.venv' >> .gitignore

    ls -la

    python -m venv .venv        # create a new virtual environment

    source .venv/bin/activate   # Activate the virtual environment

    python -V                   # Check a python version

### Install the required dependencies

    pip list

    pip install -r requirements.txt

    pip freeze | tee requirements.txt.detail

### Configure the Application

To configure the application, there are a few properties that can be set the environment

    echo 'OPENAI_API_KEY="sk-...."' >> .env

or select 'Your key' and enter your API key. 

### Running the Application

    python -m streamlit run Home.py

### Deactivate the virtual environment

    deactivate

### Examples
<img width="1692" alt="Screenshot 2024-01-23 at 12 06 43 AM" src="https://github.com/jkmathilda/gpt-quizzer/assets/142202145/3208a8ec-b733-4a9a-8b34-5d84f48e0f0e">
<img width="1710" alt="Screenshot 2024-01-23 at 12 08 58 AM" src="https://github.com/jkmathilda/gpt-quizzer/assets/142202145/278334ef-16cd-48f9-8e2f-43f56d6e946b">


# Reference

[Introduction a ChatGPT & DALL·E](https://www.youtube.com/watch?v=Mw9lM5yYHBw)
