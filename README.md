# 🧑‍💻 DevBuddy – Your AI Coding Sidekick in the Terminal

DevBuddy is a command-line coding assistant built with Python, designed to simplify your development workflow with the power of AI. It helps you organize projects, manage environments and API keys, and even chat with coding models — all from your terminal.

Whether you're coding solo or just need someone (well, something) to talk code with, DevBuddy is here to help.

---

## ✨ Features

- 💬 **Chat with AI models** in your terminal
- 🔑 **Manage API keys** for different AI providers
- 🌐 **Support for multiple AI providers** and models
- 🧪 **Isolated environments** for different projects
- 📁 **Project-based workflows** to keep things organized
- ⚡ Fast, friendly, and runs locally

---

## 🛠️ Installation

Make sure you have Python 3.7+ installed.

```bash
# 1. Clone the repo
git clone https://github.com/JAGAN-KARTHICK-A/devbuddy.git

# 2. Navigate into the project folder
cd devbuddy

# 3. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install the dependencies
pip install -r requirements.txt

# 5. Run DevBuddy
python tool.py
```

---

## 📦 Available Commands

Here's a quick look at what you can do with DevBuddy:

| Command | Description |
|--------|-------------|
| `help` | Shows the help message |
| `clear` | Clears the screen |
| `version` | Shows tool version |
| `providers list` | Lists all available AI providers |
| `apikeys list` | Lists all saved API keys |
| `apikeys add <provider id> <key> <model name>` | Adds a new API key |
| `apikeys delete <key id>` | Deletes an API key |
| `env list` | Lists all environments |
| `env new <path>` | Creates a new environment |
| `env delete <environment id>` | Deletes an environment |
| `projects list` | Lists all projects |
| `projects new <environment id> <apikey id>` | Creates a new project |
| `projects delete <project id>` | Deletes a project |
| `projects open <project id>` | Opens a project and starts the interactive coding session |
| `exit` | Exits DevBuddy |

> 🧠 Tip: Use `projects open` to dive into an AI-powered coding session inside your chosen environment.

---

## 🌱 Getting Started

Once installed, try running:

```bash
python devbuddy.py
```

From there, you can:

- Add an API key using:  
  `apikeys add <provider-id> <api-key> <model-name>`

- Create a coding environment:  
  `env new ./my_project_env`

- Create a new project:  
  `projects new 1 1`

- Start coding with AI:  
  `projects open 1`

DevBuddy will walk you through the rest.

---

## 🧩 Extending DevBuddy

Want to add new providers or customize your prompts? DevBuddy is built to be modular and tweak-friendly. Dive into the code and make it your own!

---

## 🙌 Contributing

Contributions, ideas, and suggestions are always welcome. If you’ve got a cool idea for a feature or spot a bug, feel free to open an issue or submit a pull request.

---

## 📄 License

Licensed under the MIT License.

---

## 👨‍💻 Created by A. Jagan Karthick – Because coding should feel like a team effort.
