from colorama import Fore, Back, Style, init
import pyfiglet
import platform
import sys
import os
from datetime import datetime
from dbms import DBMS
from tabulate import tabulate
import pickle
from models import GeminiClient
import time
from environment import Environment

MODEL_MAPS = {
    1: GeminiClient,
}

class FormatText():
    def __init__(self):
        init(autoreset=True)
        self.COLORS = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "blue": Fore.BLUE,
            "yellow": Fore.YELLOW,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
            "red-bg": Back.RED,
            "green-bg": Back.GREEN,
            "blue-bg": Back.BLUE,
            "yellow-bg": Back.YELLOW,
            "magenta-bg": Back.MAGENTA,
            "cyan-bg": Back.CYAN,
            "white-bg": Back.WHITE,
            "bold": Style.BRIGHT,
        }
    def __get_formated_text(self, text, color):
        return f"{self.COLORS[color]}{text}{Style.RESET_ALL}"
    def __create_banner_text(self, text, font):
        return pyfiglet.Figlet(font=font).renderText(text)
    def coloredText(self, text, color):
        return self.__get_formated_text(text, color)
    def boldText(self, text):
        return self.__get_formated_text(text, "bold")
    def bannerText(self, text, font):
        return self.__create_banner_text(text, font)

class Header():
    def __init__(self, text, formatter:FormatText, version):
        self.__formatter = formatter
        self.__headerText = text
        self.__version = version
        self.__helperText = """
 Commands:
    help                                                                     - Shows the help message
    clear                                                                    - Clears the screen
    version                                                                  - Shows tool version
    providers list                                                           - Lists all the available providers
    apikeys list                                                             - Lists all apikeys
    apikeys add <provider id> <key> <model name>                             - Add a new apikey
    apikeys delete <key id>                                                  - Delete an apikey
    env list                                                                 - Lists all environments
    env new <path>                                                           - Creates a new environment
    env delete <environment id>                                              - Delete an environment
    projects list                                                            - Lists all projects
    projects new <environment id> <apikey id>                                - Creates a new project
    projects delete <project id>                                             - Delete a project
    projects open <project id>                                               - Open a project and start working
    exit                                                                     - Exits the program
"""
    def __get_os_info(self):
        return sys.version.split()[0], platform.system(), platform.version()
    def printHeader(self):
        __os_info = self.__get_os_info()
        __current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        __banner_text = self.__formatter.coloredText(self.__formatter.boldText(self.__formatter.bannerText(self.__headerText, 'big')), "cyan")
        __version_string = self.__formatter.coloredText(self.__formatter.boldText("Version : v" + str(self.__version)), "yellow")
        __os_info_text = self.__formatter.coloredText(self.__formatter.boldText(" Python: " + str(__os_info[0]) + " • OS: " + str(__os_info[1] + " " + str(__os_info[2].split(".")[0]) + " (Build : " + str(__os_info[2].split(".")[2] + ")"))), "yellow")
        __current_time_formatted = self.__formatter.coloredText(self.__formatter.boldText(" Session started: " + str(__current_time)), "yellow")
        __author_info_text = "\n Author  : A.Jagan Karthick • https://jagankarthick.tech/"
        __author_info_text_formatted = self.__formatter.coloredText(self.__formatter.boldText(__author_info_text), "green")
        print(f"\n{__banner_text} {__version_string}")
        print(__author_info_text_formatted)
        print(f"\n{__os_info_text} \n")
        print(__current_time_formatted + "\n")
        __helper_text_formatted = self.__formatter.coloredText(self.__formatter.boldText(" For more options, run 'help'"), "magenta")
        print(__helper_text_formatted + "\n\n")
    def printHelper(self):
        print("\n" + self.__formatter.coloredText(self.__helperText, "green") + "\n")
    def printVersion(self):
        print("\n" + self.__formatter.coloredText("Version : v" + str(self.__version), "yellow") + "\n")
    def printError(self, msg):
        print("\n" + self.__formatter.coloredText(self.__formatter.boldText(f"[ERROR] {msg}"), "red") + "\n")
    def printSuccess(self, msg):
        print("\n" + self.__formatter.coloredText(self.__formatter.boldText(f"[SUCCESS] {msg}"), "green") + "\n")
    def printInfo(self, msg):
        print("\n" + self.__formatter.coloredText(self.__formatter.boldText(f"[INFO] {msg}"), "cyan") + "\n")
    def printWarning(self, msg):
        print("\n" + self.__formatter.coloredText(self.__formatter.boldText(f"[WARNING] {msg}"), "yellow") + "\n")
    def printDebug(self, msg):
        print("\n" + self.__formatter.coloredText(self.__formatter.boldText(f"[DEBUG] {msg}"), "blue") + "\n")
    def printByeMsg(self):
        print("\n" + self.__formatter.coloredText(self.__formatter.boldText("👋 Thanks for using the tool. Have a great day!"), "green") + "\n")
    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def printTable(self, headers, data):
        print("\n")
        if not data:
            self.printWarning("No data available to display.")
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
        print("\n")
    def printModelResponse(self, response):
        print("\n")
        __formatted_response_text_top = self.__formatter.coloredText(self.__formatter.boldText("┌─[DevBuddy]"), "cyan")
        print(__formatted_response_text_top)
        for line in response.strip().split("\n"):
            print(self.__formatter.coloredText(f"│ {line}", "cyan"))
        print(self.__formatter.boldText(self.__formatter.coloredText("└────────────────────────────", "cyan")))
        print("\n")

class PermissionManager():
    def __init__(self, formatter:FormatText, header:Header):
        self.__header = header
        self.__formatter = formatter
    def askPermission(self, msg):
        print("\n")
        __msg_display = self.__formatter.boldText(f"[IMPORTANT] {msg} ") + "(" + self.__formatter.coloredText("YES", "green-bg") + "/" + self.__formatter.coloredText("NO", "red-bg") + ") : "
        __p = input(__msg_display).lower()
        if __p == "yes" or __p == "y":
            return True
        elif __p == "no" or __p == "n":
            return False
        else:
            self.__header.printError(f"Invalid input. Please enter 'yes' or 'no'.")
            return self.askPermission(msg)
    def checkPermission(self, msg):
        if self.askPermission(msg):
            self.__header.printSuccess(f"Permission granted for: {msg}")
            return True
        else:
            self.__header.printError(f"Permission denied for: {msg}")
            return False

class SessionManager():
    def __init__(self, formatter:FormatText, header:Header):
        self.__formatter = formatter
        self.__header = header
    def startSession(self, client):
        print("\n\n")
        client.processQuery(client.formatUserQuery("Note:This is the command from environment and not the user. Introduce yourself briefly also include dynamic content like some tech or coding related joke or something to make the user happy and excited."))
        print("\n\n")
        while True:
            __cmd = input("[You (DevBuddy) -> ] : ")
            if __cmd == "exit" or __cmd == "quit":
                __chat_history = client.generateChatHistory()
                return __chat_history
            resp = client.processQuery(client.formatUserQuery(__cmd))
            if resp[0] == False:
                #print(resp[1])
                self.__header.printError("Unable to process your request. Try again later.")

class CommandParser():
    def __init__(self, formatter:FormatText, header:Header, db:DBMS, permissions:PermissionManager):
        self.__formatter = formatter
        self.__header = header
        self.__db = db
        self.__permissions = permissions
        self.__commands_list = ["providers", "apikeys", "env", "projects"]
        self.__session_manager = SessionManager(self.__formatter, self.__header)
    def __parse_commands(self, commands):
        if len(commands) == 1:
            commands[0] = commands[0].lower()
            if commands[0] == "help":
                self.__header.printHelper()
            elif commands[0] == "version":
                self.__header.printVersion()
            elif commands[0] == "clear":
                self.__header.clearScreen()
            else:
                if commands[0] in self.__commands_list:
                    self.__header.printError(f"'{commands[0]}' requires additional arguments. Type 'help' to see how to use the commands.")
                else:
                    self.__header.printError("Command not found!")
        else:
            commands[0] = commands[0].lower()
            if commands[0] in self.__commands_list:
                if commands[0] == "providers":
                    __sub_c1 = commands[1].lower()
                    if __sub_c1 == "list":
                        __v, __errors, __res = self.__db.listProviders()
                        if __v:
                            __headers = ["Id", "Provider name"]
                            self.__header.printTable(__headers, __res)
                        else:
                            self.__header.printError("Unable to process your request. Please try again later.")
                elif commands[0] == "apikeys":
                    __sub_c1 = commands[1].lower()
                    if __sub_c1 == "list":
                        __v, __errors, __res = self.__db.listApiKeys()
                        if __v:
                            __headers = ["Id", "Provider Id", "API KEY", "Model name"]
                            self.__header.printTable(__headers, __res)
                        else:
                            self.__header.printError("Unable to process your request. Please try again later.")
                    else:
                        if __sub_c1 in ["delete", "add"]:
                            if __sub_c1 == "add":
                                if len(commands) == 5:
                                    __provider_id = commands[2]
                                    __key = commands[3]
                                    __model_name = commands[4]
                                    if __provider_id and __key and __model_name:
                                        __v, __errors, __res = self.__db.addApiKey(__provider_id, __key, __model_name)
                                        if __v:
                                            self.__header.printSuccess("API key added successfully!")
                                        else:
                                            self.__header.printError("Unable to process your request. Please try again later.")
                                    else:
                                        self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                                else:
                                    self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                            elif __sub_c1 == "delete":
                                if len(commands) == 3:
                                    __key_id = commands[2]
                                    if __key_id:
                                        if self.__db.check_apikey_exists(__key_id)[2] == True:
                                            __permission = self.__permissions.askPermission("Are you sure you want to delete this API key? This action cannot be undone.")
                                            if __permission:
                                                __v, __errors, __res = self.__db.deleteApiKey(__key_id)
                                                if __v:
                                                    self.__header.printSuccess("API key deleted successfully!")
                                                else:
                                                    self.__header.printError("Unable to process your request. Please try again later.")
                                            else:
                                                self.__header.printInfo("User canceled the deletion of the API KEY")
                                        else:
                                            self.__header.printError(f"API key with id '{__key_id}' does not exist.")
                                    else:
                                        self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                                else:
                                    self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                        else:
                            self.__header.printError(f"Subcommand '{commands[1]}' not found. Type 'help' for a list of valid subcommands.")
                elif commands[0] == "env":
                    __sub_c1 = commands[1].lower()
                    if __sub_c1 == "list":
                        __v, __errors, __res = self.__db.listEnvironments()
                        if __v:
                            __headers = ["Id", "Environment path"]
                            self.__header.printTable(__headers, __res)
                        else:
                            self.__header.printError("Unable to process your request. Please try again later.")
                    else:
                        if __sub_c1 in ["delete", "new"]:
                            if __sub_c1 == "new":
                                if len(commands) == 3:
                                    __path = commands[2]
                                    if __path:
                                        __v, __errors, __res = self.__db.createEnvironment(__path)
                                        if __v:
                                            self.__header.printSuccess("Environment created successfully!")
                                        else:
                                            self.__header.printError("Unable to process your request. Please try again later.")
                                    else:
                                        self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                                else:
                                    self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                            elif __sub_c1 == "delete":
                                if len(commands) == 3:
                                    __env_id = commands[2]
                                    if __env_id:
                                        if self.__db.checkEnvironmentExistance(__env_id)[2] == True:
                                            __permission = self.__permissions.askPermission("Are you sure you want to delete this Environment? This action cannot be undone.")
                                            if __permission:
                                                __v, __errors, __res = self.__db.deleteEnvironment(__env_id)
                                                if __v:
                                                    self.__header.printSuccess("Environment deleted successfully!")
                                                else:
                                                    self.__header.printError("Unable to process your request. Please try again later.")
                                            else:
                                                self.__header.printInfo("User canceled the deletion of the Environment")
                                        else:
                                            self.__header.printError(f"Environment with id '{__env_id}' does not exist.")
                                    else:
                                        self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                                else:
                                    self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                        else:
                            self.__header.printError(f"Subcommand '{commands[1]}' not found. Type 'help' for a list of valid subcommands.")
                elif commands[0] == "projects":
                    __sub_c1 = commands[1].lower()
                    if __sub_c1 == "list":
                        __v, __errors, __res = self.__db.listProjects()
                        if __v:
                            __headers = ["Id", "Environment Id", "API Key Id"]
                            self.__header.printTable(__headers, __res)
                        else:
                            self.__header.printError("Unable to process your request. Please try again later.")
                    else:
                        if __sub_c1 in ["delete", "new", "open"]:
                            if __sub_c1 == "new":
                                if len(commands) == 4:
                                    __env_id = commands[2]
                                    __key_id = commands[3]
                                    if __env_id and __key_id:
                                        if self.__db.checkEnvironmentExistance(__env_id)[2] == True:
                                            if self.__db.check_apikey_exists(__key_id)[2] == True:
                                                __v, __errors, __res = self.__db.createProject(__env_id, pickle.dumps([]), __key_id)
                                                if __v:
                                                    self.__header.printSuccess("Project created successfully!")
                                                else:
                                                    self.__header.printError("Unable to process your request. Please try again later.")
                                            else:
                                                self.__header.printError(f"API Key with id '{__key_id}' does not exist")
                                        else:
                                            self.__header.printError(f"Environment with id '{__env_id}' does not exist.")
                                    else:
                                        self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                                else:
                                    self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                            elif __sub_c1 == "open":
                                if len(commands) == 3:
                                    __project_id = commands[2]
                                    if __project_id:
                                        if self.__db.checkProjectExistance(__project_id)[2] == True:
                                            __v, __errors, __p_details = self.__db.getProject(__project_id)
                                            if __v:
                                                __env_id = __p_details[1]
                                                if self.__db.checkEnvironmentExistance(__env_id):
                                                    __key_id = __p_details[3]
                                                    if self.__db.check_apikey_exists(__key_id):
                                                        #__session = MODEL_MAPS[]
                                                        __v, __errors, __env_details = self.__db.getEnvironment(__env_id)
                                                        if __v:
                                                            __v, __errors, __api_details = self.__db.getApiKeyDetails(__key_id)
                                                            if __v:
                                                                __env_path = __env_details[1]
                                                                __api_key = __api_details[2]
                                                                __model_name = __api_details[3]
                                                                __provider_id = __api_details[1]
                                                                __env = Environment(__env_path, self.__header, self.__permissions)
                                                                __chat_history = pickle.loads(self.__db.getChatHistory(__project_id)[2][0])
                                                                __client = MODEL_MAPS[int(__provider_id)](__api_key, __model_name, __env, __chat_history)
                                                                self.__header.clearScreen()
                                                                self.__header.printInfo("Opening the project...")
                                                                time.sleep(2.5)
                                                                self.__header.printInfo("Starting session...")
                                                                time.sleep(2.5)
                                                                self.__header.clearScreen()
                                                                __updated_chat_history = self.__session_manager.startSession(__client)
                                                                self.__header.printInfo("Saving progress...")
                                                                self.__db.updateChatHistory(__project_id, pickle.dumps(__updated_chat_history))
                                                                self.__header.printSuccess("Progress saved successfully!")
                                                                time.sleep(2.5)
                                                                self.__header.clearScreen()
                                                            else:   
                                                                self.__header.printError("Unable to process your request. Please try again later.")
                                                        else:
                                                            self.__header.printError("Unable to process your request. Please try again later.")
                                                    else:
                                                        self.__header.printError(f"API key with id '{__key_id}' does not exist. Please update the API key.")
                                                else:
                                                    self.__header.printError(f"Environment with id '{__env}' does not exist. Please update the environment.")
                                            else:
                                                self.__header.printError("Unable to process your request. Please try again later.")
                                        else:
                                            self.__header.printError(f"Project with id '{__project_id}' does not exist.")
                                    else:
                                        self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                            elif __sub_c1 == "delete":
                                if len(commands) == 3:
                                    __project_id = commands[2]
                                    if __project_id:
                                        if self.__db.checkProjectExistance(__project_id)[2] == True:
                                            __permission = self.__permissions.askPermission("Are you sure you want to delete this Project? This action cannot be undone.")
                                            if __permission:
                                                __v, __errors, __res = self.__db.deleteProject(__project_id)
                                                if __v:
                                                    self.__header.printSuccess("Project deleted successfully!")
                                                else:
                                                    self.__header.printError("Unable to process your request. Please try again later.")
                                            else:
                                                self.__header.printInfo("User canceled the deletion of the Project")
                                        else:
                                            self.__header.printError(f"Project with id '{__project_id}' does not exist.")
                                    else:
                                        self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                                else:
                                    self.__header.printError("Missing required arguments. Type 'help' to see how to use the commands.")
                        else:
                            self.__header.printError(f"Subcommand '{commands[1]}' not found. Type 'help' for a list of valid subcommands.")
            else:
                self.__header.printError(f"'{commands[0]}' is not a recognized command. Type 'help' to see available commands.")
    def parseCommand(self, command):
        __commands_splitted = command.strip().split()
        if len(__commands_splitted) == 0:
            pass
        else:
            self.__parse_commands(__commands_splitted)
