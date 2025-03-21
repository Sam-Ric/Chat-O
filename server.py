'''
    Chat-O
    Server Module
    by Sam-Ric
'''

import socket as s
import sys
import threading as t
import queue as q

'''
    Function to listen for incoming traffic and handle:
    - Connection requests
    - Disconnection requests
    - Incoming messages
'''
def ReceiveData(sock, addressList, messageQueue, localAddress, shutdown):
  while shutdown.is_set() == False:
    # Get data from the client
    data, incomingAddr = sock.recvfrom(1024)
    data = data.decode('utf-8')

    # Handle connection requests
    if data[0:4] == '[NC]':
      username = data[4:]
      reply = str.encode("Connection established")
      addressList += [incomingAddr]     # Add the new client to the addresses' list
      sock.sendto(reply, incomingAddr)  # Notify the client that the connection was successful
      msg = f"{localAddress[0]}\\[*] [NEW CONNECTION] {username}@{incomingAddr[0]} connected to the server"
      print(msg)

      # Notify the other clients about the new connection
      for elem in addressList:
        sock.sendto(str.encode(msg), elem)

    # Handle disconnection requests
    elif data == '!q':
      sock.close()
      sys.exit()

    # Handle incoming messages
    else:
      messageQueue.put(f"{incomingAddr}\\{data}")   # Store the message in the message queue


'''
    Function to send any messages in the message queue to all clients connected
    to the server.
'''
def SendData(sock, addressList, messageQueue, shutdown):
  while shutdown.is_set() == False:
    if messageQueue.empty() == False:
      data = messageQueue.get()
      temp = data.split("\\")
      for elem in addressList:
        if str(elem) != str(temp[0]):
          sock.sendto(str.encode(data), elem)


'''
    Server module's main function.
'''
def Server(localIP, localPort):
  print("[*] [ONLINE] Server status updated")
  localAddress = (localIP, localPort)

  # Create a UDP socket
  server = s.socket(s.AF_INET, s.SOCK_DGRAM)

  # Bind the server UDP socket
  server.bind(localAddress)

  # Initialize the list of connected clients
  addressList = []

  # Initialize the message queue
  messageQueue = q.SimpleQueue()

  # Enable multithreading
  shutdown = t.Event()
  receptionThread = t.Thread(target=ReceiveData, args=(server, addressList, messageQueue, localAddress, shutdown))
  sendingThread = t.Thread(target=SendData, args=(server, addressList, messageQueue, shutdown))

  try:
    receptionThread.start()
    sendingThread.start()

    receptionThread.join()
    sendingThread.join()

  except KeyboardInterrupt:
    print("\n[*] Ctrl+C detected. Shutting down...")
    shutdown.set()
    receptionThread.join()
    sendingThread.join()
    for elem in addressList:
      server.sendto(str.encode("Server shutting down"), elem)
    server.close()

  print("[*] [OFFLINE] Server status updated")

Server('127.0.0.1', 9000)