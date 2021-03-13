import socket, threading, random, time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 5050))

x = 50

has_first_player_connected = False

player_1 = None
player_2 = None

players = []

def handle_client(conn, addr, x):
      global has_first_player_connected
      print(f"Client connected on {conn}")
      connected = True

      if has_first_player_connected == False:
            #This code will run if this is the first player connecting
            #To the server
            conn.send(bytes("You Are Player 1".encode()))
            
            has_first_player_connected = True

            players.append(conn)

            is_player_1 = True
      else:
            #Player 2
            conn.send(bytes("You Are Player 2".encode()))

            players.append(conn)

            is_player_1 = False
            
      time.sleep(1)
      
      while connected:
            data = conn.recv(6000)
            
            if is_player_1:
                  try:
                        players[1].send(bytes(data))
                  except:
                        pass

            if not is_player_1:
                  try:
                        players[0].send(bytes(data))
                  except:
                        pass
            

      print(f"Client at {addr} has disconnected")
      conn.close()

def listen():
      server.listen()
      while True:
            conn, addr = server.accept()

            thread = threading.Thread(target = handle_client, args = (conn, addr, x))
            thread.start()

print("SERVER STARTING...")
listen()
