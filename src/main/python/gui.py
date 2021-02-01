from executer import Executer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from threading import Thread
from time import sleep
import json
from passwordStrength import PasswordStrengthChecker
import sys
import faulthandler
import atexit
from fbs_runtime.application_context.PyQt5 import ApplicationContext

faulthandler.enable()

class LoginForm(QWidget):
    def __init__(self, server_exec):
        super(LoginForm,self).__init__()
        self.pwc = PasswordStrengthChecker(strict=False)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.activateWindow()
        self.server_exec = server_exec
        self.setStyleSheet(open("style.qss", "r").read())
        self.title = "Login/Register"
        self.layout = QGridLayout()
        # Reused widgets
        label_login_name = QLabel("<font size='4'> Username </font>")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Please enter your username")
        self.layout.addWidget(label_login_name, 0, 0)
        self.layout.addWidget(self.username, 0, 1)
        label_login_password = QLabel("<font size='4'> Password </font>")
        self.password = QLineEdit()
        self.password.setPlaceholderText('Please enter your password')
        self.layout.addWidget(label_login_password, 1, 0)
        self.layout.addWidget(self.password, 1, 1)
        # tab 1
        button_login = QPushButton('login')
        button_login.pressed.connect(self.login)
        button_register = QPushButton('register')
        button_register.pressed.connect(self.register)
        self.layout.addWidget(button_login,2,1)
        self.layout.addWidget(button_register,2,0)
        self.setLayout(self.layout)

    def login(self):
        while True:
            r = self.server_exec.exec_(f"login {self.username.text()} {self.password.text()}")
            if r == False:
                continue
            msg = QMessageBox(self)
            msg.setText(r)
            if r == "You're logged in!":
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.close()
            else:
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            break

    def register(self):
        is_secure, rsp = self.pwc.is_secure(self.password.text())
        if is_secure:
            r = self.server_exec.exec_(f"reg {self.username.text()} {self.password.text()}")
            msg = QMessageBox(self)
            msg.setText(r)
            msg.exec_()
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText(rsp)
            msg.exec_()


class ChatWindow(QWidget):
    def __init__(self, server_exec):
        super(ChatWindow, self).__init__()
        self.server_exec = server_exec
        self.last_sender = ""
        self.setWindowTitle("EncryptiiChat")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.loginWindow = LoginForm(self.server_exec)
        self.loginWindow.show()
        self.MQ = []
        self.text_area = QTextEdit(self)
        self.text_area.setFocusPolicy(Qt.NoFocus)
        self.text_area.setReadOnly(True)
        self.text_area.setAcceptRichText(True)
        self.text_area.setAutoFormatting(QTextEdit.AutoAll)
        self.message = QLineEdit(self)
        self.message.setPlaceholderText("Enter your message")
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.text_area,0,0,1,3)
        self.to_user = QComboBox(self)
        self.match_button = QPushButton("Match")
        self.match_button.pressed.connect(self.match)
        self.layout.addWidget(self.to_user,2,0)
        self.layout.addWidget(self.match_button,2,1)
        self.layout.addWidget(self.message,2,2)
        self.colors_layout = QHBoxLayout(self)
        self.yellow_button = QPushButton("")
        self.yellow_button.setStyleSheet("background-color:#FFCD48")
        self.orange_button = QPushButton("")
        self.orange_button.setStyleSheet("background-color:#F28437")
        self.red_button = QPushButton("")
        self.red_button.setStyleSheet("background-color:#DE4557")
        self.purple_button = QPushButton("")
        self.purple_button.setStyleSheet("background-color:#B940E5")
        self.blue_button = QPushButton("")
        self.blue_button.setStyleSheet("background-color:#55A5FD")
        self.light_blue_button = QPushButton("")
        self.light_blue_button.setStyleSheet("background-color:#1AD3FB")
        self.green_button = QPushButton("")
        self.green_button.setStyleSheet("background-color:#A4DB47")
        self.colors_layout.addWidget(self.yellow_button)
        self.colors_layout.addWidget(self.orange_button)
        self.colors_layout.addWidget(self.red_button)
        self.colors_layout.addWidget(self.purple_button)
        self.colors_layout.addWidget(self.blue_button)
        self.colors_layout.addWidget(self.light_blue_button)
        self.colors_layout.addWidget(self.green_button)
        self.init_colors()
        self.layout.addLayout(self.colors_layout,1,0,1,3)
        self.layout.setColumnStretch(2,4)
        self.layout.setColumnStretch(1,1)
        self.layout.setColumnStretch(0,2)
        self.setLayout(self.layout)
        self.message.returnPressed.connect(self.send_message_thread)
        self.thread = Thread(target=self.fetch_new_messages, daemon=True)
        self.thread.start()

    def init_colors(self):
        with open("colorsconfig.json","r") as f:
            color_data = json.load(f)
        self.yellow_button.setText(color_data["yellow"]["about"])
        self.yellow_button.pressed.connect(lambda:self.send_color_thread("yellow"))
        self.orange_button.setText(color_data["orange"]["about"])
        self.orange_button.pressed.connect(lambda:self.send_color_thread("orange"))
        self.red_button.setText(color_data["red"]["about"])
        self.red_button.pressed.connect(lambda:self.send_color_thread("red"))
        self.blue_button.setText(color_data["blue"]["about"])
        self.blue_button.pressed.connect(lambda:self.send_color_thread("blue"))
        self.light_blue_button.setText(color_data["light-blue"]["about"])
        self.light_blue_button.pressed.connect(lambda:self.send_color_thread("light-blue"))
        self.green_button.setText(color_data["green"]["about"])
        self.green_button.pressed.connect(lambda:self.send_color_thread("green"))
        self.purple_button.setText(color_data["purple"]["about"])
        self.purple_button.pressed.connect(lambda:self.send_color_thread("purple"))
        self.color_data = color_data
        self.orig_color_data = color_data

    def send_message_thread(self):
        if self.server_exec.not_logged_in():
            print("log in first!")
            self.not_logged_in_popup()
            self.loginWindow.show()
            return
        if self.to_user.count() == 0:
            self.not_matched_popup()
            return
        sendThread = Thread(target=self.send_message)
        sendThread.start()

    def match(self):
        while True:
            res = self.server_exec.exec_("match")
            if res!= False:
                target_alias, my_alias = res
                break
        self.to_user.addItem(target_alias)
        index = self.to_user.findText(target_alias,Qt.MatchFixedString)
        self.to_user.setCurrentIndex(index)

    def get_mg(self,color):
        return f"{self.color_data[color]['details']}"

    def suggest(self,msg):
        msg = msg.lower()
        for rsp in self.color_data['responses']:
            if rsp in msg:
                self.color_data['yellow']['details'] = self.color_data['responses'][rsp]['details']
                self.yellow_button.setText(self.color_data['responses'][rsp]['about'])
                return self.color_data['responses'][rsp]
        return False

    def send_color_thread(self,color):
        if self.server_exec.not_logged_in():
            print("log in first!")
            self.not_logged_in_popup()
            self.loginWindow.show()
            return
        if self.to_user.count() == 0:
            self.not_matched_popup()
            return
        sendThread = Thread(target=self.send_color(color))
        sendThread.start()

    def send_color(self,color):
        html_resp = f"<span style=\"color:#ffffff\">[to <i>{self.to_user.currentText()}</i>]:{self.get_mg(color)}</span>"
        tc = self.text_area.textCursor()
        form = tc.charFormat()
        form.setForeground(Qt.green)
        tc.setCharFormat(form)
        tc.insertHtml(html_resp)
        self.text_area.append("")
        self.message.clear()
        while True:
            r = self.server_exec.exec_(f"send {self.to_user.currentText()} {self.get_mg(color)}")
            if not r:
                continue
            print(f"{self.server_exec.username}:sent!")
            sleep(0.1)
            break

    def send_message(self):
        html_resp = f"<span style=\"color:#ffffff\">[to <i>{self.to_user.currentText()}</i>]:{self.message.text()}</span>"
        tc = self.text_area.textCursor()
        form = tc.charFormat()
        form.setForeground(Qt.green)
        tc.setCharFormat(form)
        tc.insertHtml(html_resp)
        self.text_area.append("")
        send_msg = self.message.text()
        self.message.clear()
        self.message.setPlaceholderText("Sending...")
        self.message.setFocusPolicy(Qt.NoFocus)
        while True:
            r = self.server_exec.exec_(f"send {self.to_user.currentText()} {send_msg}")
            if r == False:
                continue
            self.message.setPlaceholderText("Enter your message")
            self.message.setFocusPolicy(Qt.ClickFocus)
            print(f"{self.server_exec.username}:sent:{send_msg}")
            sleep(0.1)
            break

    def not_logged_in_popup(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Not logged in!")
        msg.setText("Please log in to send a message")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

    def not_matched_popup(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Matched")
        msg.setText("Please hit the match button to match with someone")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

    def get_cur_sender(self,msg):
        for i in range(len(msg)):
            if msg[i:i+1] == ']':
                un = msg[1:i].split(":")[0]
                mg = msg[i+2:]
                break
        return un, mg

    def display_new_messages(self):
        while len(self.MQ):
            new_msg = self.MQ.pop(0)
            self.cur_sender,cur_msg = self.get_cur_sender(new_msg)
            index = self.to_user.findText(self.cur_sender)
            if index == -1:
                self.to_user.addItem(self.cur_sender)
                new_index = self.to_user.findText(self.cur_sender)
                self.to_user.setCurrentIndex(new_index)
            if self.last_sender != self.cur_sender:
                print(self.cur_sender)
                self.text_area.textCursor().insertHtml(f"<h3 style=\"color:#ffff00\">sender: {self.cur_sender}</h3>")
                self.text_area.append("")
            self.text_area.textCursor().insertHtml(f"<span style=\"color:#ffffff\">{cur_msg}</span>")
            self.suggest(cur_msg)
            self.text_area.append("")
            self.last_sender = self.cur_sender

    def fetch_new_messages(self):
        while True:
            if self.server_exec.not_logged_in():
                sleep(0.5)
                continue
            try:
                new_message = self.server_exec.exec_("getMsg")
                if type(new_message) == list:
                    for msg in new_message:
                        decoded_msg = msg.decode()
                        print(decoded_msg)
                        self.MQ.append(decoded_msg)
                sleep(0.5)
            except:
                continue

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Chat application")
        with open("config.json") as f:
            cfg = json.load(f)
            server = cfg['server']
            port = int(cfg['port'])
        print(server,port)
        self.server_exec = Executer((server, port))
        atexit.register(self.server_exec.on_exit)
        self.setStyleSheet(open("style.qss", "r").read())
        self.mainWidget = ChatWindow(self.server_exec)
        self.setCentralWidget(self.mainWidget)
        
    def closeEvent(self, event):
        print("close")
        while True:
            try:
                rsp = self.server_exec.exec_("offline")
                if rsp!=False:
                    print(rsp)
                    break
            except:
                continue

def window():
    appctxt = ApplicationContext()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    timer = QTimer()
    timer.timeout.connect(win.mainWidget.display_new_messages)
    timer.start(1000)
    app.exec_()
    exit_code = appctxt.app.exec_()

window()
