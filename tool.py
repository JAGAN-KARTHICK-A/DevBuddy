from utils import FormatText, Header, CommandParser, PermissionManager
from dbms import DBMS

db = DBMS()
formatter = FormatText()
header = Header("DevBuddy", formatter, 1.0)
permission_manager = PermissionManager(formatter, header)
parser = CommandParser(formatter, header, db, permission_manager)

header.printHeader()

while True:
    try:
        command = input("[You -> ]: ")
        if command == "exit":
            header.printByeMsg()
            break
        else:
            try:
                parser.parseCommand(command)
            except Exception as e:
                header.printError("Unable to process your request. Please try again later.")
                break
            except KeyboardInterrupt:
                header.printByeMsg()
                break
    except KeyboardInterrupt:
        header.printByeMsg()
        break