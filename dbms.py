import sqlite3
import os

class DBMS():
    def __init__(self):
        self.CONN = None
        self.CURSOR = None
        self.__init_db()
    def __insert_providers(self):
        self.CURSOR.execute("SELECT COUNT(*) FROM providers")
        __count = self.CURSOR.fetchone()[0]
        if __count == 0:
            self.CURSOR.execute("INSERT INTO providers (name) VALUES (?)", ("Gemini",))
            self.CONN.commit()
    def __init_db(self):
        if not os.path.exists('./data.db'):
            __f = open("./data.db", "w")
            __f.write("")
            __f.close()
        self.CONN = sqlite3.connect("./data.db")
        self.CURSOR = self.CONN.cursor()
        self.CURSOR.execute("PRAGMA foreign_keys = ON;")
        self.CONN.commit()
        self.CURSOR.execute("""CREATE TABLE IF NOT EXISTS environments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path VARCHAR NOT NULL
        )""")
        self.CURSOR.execute("""CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR NOT NULL
        )""")
        self.CURSOR.execute("""CREATE TABLE IF NOT EXISTS apikeys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider INTEGER NOT NULL,
            key VARCHAR NOT NULL COLLATE BINARY,
            modelName VARCHAR NOT NULL COLLATE BINARY,
            FOREIGN KEY (provider) REFERENCES providers(id) ON DELETE CASCADE
        )""")
        self.CURSOR.execute("""CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            env INTEGER NOT NULL,
            history BLOB,
            api_key_id INTEGER NOT NULL,
            FOREIGN KEY (env) REFERENCES environments(id) ON DELETE CASCADE,
            FOREIGN KEY (api_key_id) REFERENCES apikeys(id) ON DELETE CASCADE
        )""")
        self.CONN.commit()
        self.__insert_providers()
    def __list_providers(self):
        self.CURSOR.execute("SELECT * FROM providers")
        return self.CURSOR.fetchall()
    def __get_apikey(self, provider_id):
        self.CURSOR.execute("SELECT * FROM apikeys WHERE provider = ?", (provider_id,))
        return self.CURSOR.fetchall()
    def __list_apikeys(self):
        self.CURSOR.execute("SELECT * FROM apikeys")
        return self.CURSOR.fetchall()
    def __insert_apiKey(self, provider_id, key, model_name):
        self.CURSOR.execute("INSERT INTO apikeys (provider, key, modelName) VALUES (?, ?, ?)", (provider_id, key, model_name))
        self.CONN.commit()
    def __delete_apikey(self, id):
        self.CURSOR.execute("DELETE FROM apikeys WHERE id = ?", (id,))
        self.CONN.commit()
    def __create_env(self, path):
        self.CURSOR.execute("INSERT INTO environments (path) VALUES (?)", (path,))
        self.CONN.commit()
    def __create_project(self, env, history, api_key_id):
        self.CURSOR.execute("INSERT INTO projects (env, history, api_key_id) VALUES (?, ?, ?)", (env, history, api_key_id))
        self.CONN.commit()
    def __list_environments(self):
        self.CURSOR.execute("SELECT * FROM environments")
        return self.CURSOR.fetchall()
    def __list_projects(self):
        self.CURSOR.execute("SELECT id, env, api_key_id FROM projects")
        return self.CURSOR.fetchall()
    def __delete_project(self, id):
        self.CURSOR.execute("DELETE FROM projects WHERE id = ?", (id,))
        self.CONN.commit()
    def __delete_env(self, id):
        self.CURSOR.execute("DELETE FROM environments WHERE id = ?", (id,))
        self.CONN.commit()
    def __get_project(self, id):
        self.CURSOR.execute("SELECT * FROM projects WHERE id = ?", (id,))
        return self.CURSOR.fetchone()
    def __get_env(self, id):
        self.CURSOR.execute("SELECT * FROM environments WHERE id = ?", (id,))
        return self.CURSOR.fetchone()
    def __get_apiKey_from_id(self, id):
        self.CURSOR.execute("SELECT * FROM apikeys WHERE id = ?", (id,))
        return self.CURSOR.fetchone()
    def __check_folder_exist_or_not(self, folder):
        return os.path.exists(folder)
    def __check_env_exists(self, id):
        __env = self.__get_env(id)
        if __env:
            return True
        return False
    def __check_apikey_exists(self, id):
        __api_key = self.__get_apiKey_from_id(id)
        if __api_key:
            return True
        return False
    def __check_project_exists(self, id):
        __env = self.__get_project(id)
        if __env:
            return True
        return False
    def __get_chatHistory(self, pid):
        self.CURSOR.execute("SELECT history FROM projects WHERE id=?", (pid,))
        return self.CURSOR.fetchone()
    def __update_chatHistory(self, pid, history):
        self.CURSOR.execute("UPDATE projects SET history=? WHERE id=?", (history, pid))
        self.CONN.commit()
    def createEnvironment(self, path):
        try:
            self.__create_env(path)
            return True, "", ""
        except Exception as e:
            return False, e, ""
    def createProject(self, env, history, api_key_id):
        try:
            self.__create_project(env, history, api_key_id)
            return True, "", ""
        except Exception as e:
            return False, e, ""
    def listEnvironments(self):
        try:
            return True, "", self.__list_environments()
        except Exception as e:
            return False, e, ""
    def listProjects(self):
        try:
            return True, "", self.__list_projects()
        except Exception as e:
            return False, e, ""
    def deleteEnvironment(self, id):
        try:
            self.__delete_env(id)
            return True, "", ""
        except Exception as e:
            return False, e, ""
    def deleteProject(self, id):
        try:
            self.__delete_project(id)
            return True, "", ""
        except Exception as e:
            return False, e, ""
    def getEnvironment(self, id):
        try:
            return True, "", self.__get_env(id)
        except Exception as e:
            return False, e, ""
    def getProject(self, id):
        try:
            return True, "", self.__get_project(id)
        except Exception as e:
            return False, e, ""
    def getApiKeyDetails(self, id):
        try:
            return True, "", self.__get_apiKey_from_id(id)
        except Exception as e:
            return False, e, ""
    def validateEnvironment(self, id):
        try:
            if self.__check_env_exists(id):
                env = self.__get_env(id)
                if self.__check_folder_exist_or_not(env[1]):
                    return True, "", ""
            return False, "Environment does not exist", ""
        except Exception as e:
            return False, e, ""
    def checkEnvironmentExistance(self, id):
        try:
            return True, "",self.__check_env_exists(id)
        except Exception as e:
            return False, e, ""
    def checkProjectExistance(self, id):
        try:
            return True, "",self.__check_project_exists(id)
        except Exception as e:
            return False, e, ""
    def check_apikey_exists(self, id):
        try:
            return True, "",self.__check_apikey_exists(id)
        except Exception as e:
            return False, e, ""
    def listProviders(self):
        try:
            return True, "", self.__list_providers()
        except Exception as e:
            return False, e, ""
    def getApiKey(self, provider_id):
        try:
            return True, "", self.__get_apikey(provider_id)
        except Exception as e:
            return False, e, ""
    def addApiKey(self, provider_id, key, model_name):
        try:
            self.__insert_apiKey(provider_id, key, model_name)
            return True, "", ""
        except Exception as e:
            return False, e, ""
    def deleteApiKey(self, id):
        try:
            self.__delete_apikey(id)
            return True, "", ""
        except Exception as e:
            return False, e, ""
    def listApiKeys(self):
        try:
            return True, "", self.__list_apikeys()
        except Exception as e:
            return False, e, ""
    def getChatHistory(self, id):
        try:
            return True, "", self.__get_chatHistory(id)
        except Exception as e:
            return False, e, ""
    def updateChatHistory(self, id, history):
        try:
            self.__update_chatHistory(id, history)
            return True, "", ""
        except Exception as e:
            return False, e, ""
    def __del__(self):
        self.CONN.close()