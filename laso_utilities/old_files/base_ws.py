import websocket

websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("ws://10.1.1.191:6980/centre")
ws.send("Hello, Server")
#print(ws.recv())
ws.close()
