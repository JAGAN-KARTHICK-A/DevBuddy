import os

class Environment:
    def __init__(self, user_path, header, permissions):
        self.__system_path = os.path.dirname(os.path.abspath(__file__))
        self.workingPath = user_path
        self.__header = header
        self.__permissions = permissions
    def parseRequest(self, request):
        if request["type"] == "file-create":
            return self.__create_file(request["file_name"], request["file_extention"], request["file_content"], request["file_path"])
        elif request["type"] == "file-read":
            return self.__read_file(request["file_name"], request["file_extention"], request["file_path"])
        elif request["type"] == "file-delete":
            return self.__delete_file(request["file_name"], request["file_extention"], request["file_path"])
        elif request["type"] == "file-rename":
            return self.__rename_file(request["file_name"], request["new_file_name"], request["file_extention"], request["file_path"])
        elif request["type"] == "file-list":
            return self.__list_files(request["path"])
        elif request["type"] == "get_pwd":
            return self.__get_cwd()
        elif request["type"] == "shell_cmd":
            return self.__execute_shell_command(request["cmd"])
        elif request["type"] == "conv_user":
            return self.__convey_user(request["message"])
        else:
            return False,"Invalid command given",""
    def __create_file(self, filename, ext, content, path):
        try:
            __path = path + "\\" + filename + '.' + ext
            __val = self.__permissions.checkPermission(f"Please allow me to create this file : {__path}")
            if __val:
                __f = open(__path, 'w')
                __f.write(content)
                __f.close()
                return True,"",filename+"."+ext
            else:
                return False, "User denied permission to create this file", ""
        except Exception as e:
            return False,e,""
    def __read_file(self, filename, ext, path):
        self.__header.printInfo("Reading file : " + path + "\\" + filename + '.' + ext)
        try:
            __path = path + "\\" + filename + '.' + ext
            __f = open(__path, 'r')
            __d = __f.read()
            __f.close()
            return True,"",__d
        except Exception as e:
            return False,e,""
    def __delete_file(self, filename, ext, path):
        try:
            __path = path + "\\" + filename + '.' + ext
            __val = self.__permissions.checkPermission(f"Please allow me to delete this file : {__path}")
            if __val:
                os.remove(__path)
                return True,"",filename+"."+ext
            else:
                return False, "User denied permission to delete this file", ""
        except Exception as e:
            return False,e,""
    def __rename_file(self, filename, newname, ext, path):
        try:
            __path = path + "\\" + filename + '.' + ext
            __new_path = path + "\\" + newname + '.' + ext
            __val = self.__permissions.checkPermission(f"Please allow me to rename this file : {__path} to {__new_path}")
            if __val:
                os.rename(__path, __new_path)
                return True,"",newname+"."+ext
            else:
                return False, "User denied permission to rename this file", ""
        except Exception as e:
            return False,e,""
    def __list_files(self, path):
        try:
            __f = os.listdir(path)
            return True, "", __f
        except Exception as e:
            return False, e, ""
    def __get_cwd(self):
        return True, "", self.workingPath
    def __set_cwd(self, path):
        self.workingPath = path
        return self.workingPath
    def __execute_shell_command(self, cmd):
        try:
            __val = self.__permissions.checkPermission(f"Please allow me to execute this command : {cmd}")
            if __val:
                __p = os.system("cd " + self.workingPath + " && " + cmd)
                return True, "", __p
            else:
                return False, "User denied permission to run this command", ""
        except Exception as e:
            return False, e, ""
    def __convey_user(self, msg):
        #print(msg)
        self.__header.printModelResponse(msg)
        return True, "", ""

