# -*- coding: utf-8 -*-
# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
import json
import mcrcon
import os
# import platform
import PySimpleGUI as sg
import re
# import sys
# import threading
import yaml


class Json:
    def __init__(self):
        self._folder = r"./lang"

    def get(self, lang: str):
        file = fr"{self._folder}/{lang}.json"
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                request = json.load(f)
                f.close()
        else:
            sg.theme(config.get("theme"))
            sg.popup_error(f"The language file doesn't exists: {lang}")
            with open(fr"{self._folder}/en.json", "r", encoding="utf-8") as f:
                request = json.load(f)
                f.close()
        return request


"""
class System:
    def __init__(self):
        self.sg = None
        self.system_detect()

    def system_detect(self):
        operation_system = platform.system()
        if operation_system == "Windows":
            if sys.getwindowsversion().build >= 22000:
                import PySimpleGUIWx as sg
            else:
                import PySimpleGUI as sg
        else:
            import PySimpleGUI as sg
        self.sg = sg

    def get_sg(self):
        return self.sg
"""


class Config:
    def __init__(self):
        self._filename = "config.yml"
        if not os.path.exists(self._filename):
            d = {
                "font": "Segoe UI",
                "code-font": "Consolas",
                "font-size": 11,
                "theme": "SystemDefaultForReal",
                "lang": "en",
                "host": "",
                "port": 25575,
                "version": 2.0
            }
            with open(self._filename, "w", encoding="utf-8") as f:
                yaml.dump(d, f)
                f.write("# Official supported languages: en, zh_cn, zh_tw\n")
                f.write("# You can also add your language to ./lang/ or make a pull request to me")
                f.close()
            del d

        with open(self._filename, "r") as f:
            self.config = yaml.safe_load(f)
            f.close()

    def get(self, option):
        try:
            result = self.config[option]
        except:
            result = None
        return result

    def write(self, option, value):
        self.config[option] = value
        with open(self._filename, "w+", encoding="utf-8") as f:
            yaml.dump(self.config, f)
            f.write("# Official supported languages: en, zh_tw\n")
            f.write("# You can also add your language to ./lang/ or make a pull request to me")
            f.close()


class UI:
    def __init__(self, module, remote, t: str, f: tuple, c: tuple):
        self._sg = module
        # self._title = {"login": "Minecraft RCON login", "manager": "Minecraft RCON Manager"}
        self._sg.theme(t)
        self._font = f
        self._code = c
        self._login_layout = None
        self._manager_layout = None
        self._login_window = None
        self._manager_window = None
        self._rcon = remote
        self.mloop = None
        self.sloop = None
        self._host = None
        self._port = None

    def make_window(self, window_type):
        self._host = config.get("host")
        self._port = str(config.get("port"))

        if window_type == "login":
            self._login_layout = [
                [sg.Text(f"{lang['login.host']}: ", font=self._font),
                 sg.InputText(key="-host-", font=self._font)],

                [sg.Text(f"{lang['login.port']}: ", font=self._font),
                 sg.InputText(key="-port-", default_text="", font=self._font)],

                [sg.Text(f"{lang['login.password']}: ", font=self._font),
                 sg.InputText(key="-password-", password_char="\u25cf", font=self._font)],

                [sg.Button(lang['login.connect'],
                           key="-connect-",
                           enable_events=True,
                           bind_return_key=True,
                           font=self._font
                           ),
                 sg.Button(lang['login.clear'], key="-clear-", font=self._font)],
            ]

            self._login_window = self._sg.Window(lang['login.title'],
                                                 self._login_layout,
                                                 finalize=True)
            # self.mloop = threading.Thread(target=self.mainloop)
            # self.mloop.start()
            self.mainloop()
        elif window_type == "manager":
            self._manager_layout = [
                [sg.Output(size=(80, 20), font=self._code)],

                [sg.Text(lang['manager.command'], font=self._font),
                 sg.InputText(key="-command-", font=self._code, focus=True, size=(70, 1))],

                [sg.Button(lang['manager.send'],
                           key="-send-",
                           enable_events=True,
                           bind_return_key=True,
                           font=self._font
                           ),
                 sg.Button(lang['manager.up'], key="-up-"),
                 sg.Button(lang['manager.down'], key="-down-")],
            ]

            self._manager_window = self._sg.Window(lang['manager.title'],
                                                   self._manager_layout,
                                                   finalize=True
                                                   )
            # self.sloop = threading.Thread(target=self.subloop)
            # self.sloop.start()
            self.subloop()

    def mainloop(self):
        window = self._login_window
        sg = self._sg
        window["-host-"].update(self._host)
        window["-port-"].update(self._port)
        while True:
            event, value = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "-connect-":
                try:
                    host = value["-host-"]
                    password = value["-password-"]
                    port = int(value["-port-"])
                    rcon.connect(host, password, port)
                except Exception as e:
                    sg.popup_error(f"{lang['global.error']}: {e}!")
                    window["-host-"].update(self._host)
                    window["-port-"].update(self._port)
                    window["-password-"].update("")
                else:
                    config.write("host", host)
                    config.write("port", port)
                    self.make_window("manager")
                    break
            if event == "-clear-":
                window["-host-"].update("")
                window["-port-"].update("25575")
                window["-password-"].update("")
                config.write("host", "")
                config.write("port", 25575)
        window.close()
        self._login_window = None

    def subloop(self):
        window = self._manager_window
        self._login_window.close()
        self._login_window = None
        sg = self._sg
        ucl = []
        line = 0
        while True:
            event, value = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "-send-":
                try:
                    command = value["-command-"]
                    if command == "exit":
                        break
                    elif command == "":
                        continue
                    else:
                        rcon.command(command)
                except Exception as e:
                    sg.popup_error(f"{lang['global.error']}: {e}!")
                else:
                    window["-command-"].update("")
                    ucl.append(value["-command-"])
                    line = len(ucl)
            if event == "-up-":
                try:
                    line -= 1
                    window["-command-"].update(ucl[line])
                except:
                    pass
            if event == "-down-":
                try:
                    line += 1
                    window["-command-"].update(ucl[line])
                except:
                    window["-command-"].update("")
        window.close()
        rcon.disconnect()
        self.make_window("login")


class MCRcon:
    def __init__(self):
        self._mcr = None
        self._pattern = r"§([a-zA-Z0-9])"

    def connect(self, host, password, port):
        self._mcr = mcrcon.MCRcon(host, password, port)
        self._mcr.connect()

    def command(self, command):
        resp = self._mcr.command(command)
        # print(f"[INFO] Send command: {command}")
        print(f"> {command}")
        resp = str(resp)
        splits = command.split(" ")
        if splits[0] == "say":
            message = ""
            for i in range(len(splits)):
                if i == 0:
                    continue
                else:
                    message = message + " " + splits[i]
            print(f"[Rcon] {message}")
        resp = re.sub(self._pattern, "", resp)
        print(resp)

    def disconnect(self):
        self._mcr.disconnect()


if __name__ == "__main__":
    # system = System()
    # sg = system.get_sg()

    config = Config()
    jsn = Json()
    font = (str(config.get("font")), int(config.get("font-size")))
    code = (str(config.get("code-font")), int(config.get("font-size")))
    theme = config.get("theme")
    lang = jsn.get(config.get("lang"))

    rcon = MCRcon()

    ui = UI(sg, rcon, theme, font, code)
    ui.make_window("login")
