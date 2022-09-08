from operator import truediv
from websocket import create_connection
import pywinauto
import os
import time
import sys
from pywinauto.application import Application
import logging
from datetime import datetime
import websockets
import websocket
import asyncio


def user_name():
    user_name = os.getlogin()
    if (user_name == "center"):
        user_name = "centre"
    return user_name


# def ws_send_log(message):
#     host='10.1.1.191'
#     port=6980
#     topic = user_name()
#     ws = create_connection(f"ws://{host}:{port}/{topic}")
#     print(ws.recv())
#     print("Sending log message")
#     ws.send(message)
#     print("Sent")
#     print("Receiving...")
#     result =  ws.recv()
#     print("Received '%s'" % result)
#     ws.close()

def produce(message):
    host='10.1.1.191'
    port=6980
    topic = user_name()
    ws = websocket.WebSocket()
    ws.connect(f"ws://{host}:{port}/{topic}")
    ws.send(message)
    #print(ws.recv())
    ws.close()


def ws_send_log(message):
    host='10.1.1.191'
    port=6980
    topic = user_name()
    #ws = create_connection(f"ws://{host}:{port}/{topic}")
    with websockets.connect(f"ws://{host}:{port}/{topic}") as ws:
        print("Sending log message")
        ws.send(message)
        print("Sent")
        print("Receiving...")
        result =  ws.recv()
        print("Received '%s'" % result)
        ws.close()



def main():
    num = 10
    application_path = os.path.join("C:", "\Program Files (x86)", "Turf Trax", "Going Stick")
    full_path = f'{application_path}\\GoingStickXP.exe'
    while True:
        try:
            try:
                app = Application(backend="uia").connect(path = full_path)
                message = "SUCCESS - Application Initialised"
                print(message)
                produce(message)
            except Exception as e1:
                message = "ERROR - Application Failure - pywinauto can not locate Application"
                print(message)
                produce(message)
                time.sleep(5)
                continue
            try:
                dlg = app.window(title_re="TurfTrax 1.11.5", class_name="WindowsForms10.Window.8.app.0.141b42a_r6_ad1")
                app.dlg["Start Download"].click()
                message = "SUCCESS - Button Activated"
                print(message)
                produce(message)
            except Exception as e2:
                message = "ERROR - Button NOT Initiated"
                print(message)
                produce(message)
                time.sleep(5)
                continue
        except Exception as e:
            message = "ERROR - Application Failure - NOT Initiated"
            print(message)
            produce(message)
            time.sleep(5)
            continue
        time.sleep(10)

if __name__ == "__main__":
    main()
