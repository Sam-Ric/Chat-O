'''
    Chat-O
    Client Module
    by Sam-Ric
'''

import socket as s
import threading as t
import curses
import sys


'''
    Function to establish connection to the server.
    The client sends a request to the server and waits for the
    connection process to be completed.
'''
def ConnectToServer(sock, serverAddress):
  username = input("Username: ")    # Getting the user's desired username

  # Sending the connection request to the server
  msg = str.encode(f"[NC]{username}")
  sock.sendto(msg, serverAddress)

  # Waiting for the server's reply
  print("[*] Waiting for the server to reply...")
  msg = sock.recv(1024)   # -> blocking function

  # Notify the user that the client was successfully connected to the server
  print("[*] Connection established!")


'''
    Function to fetch any incoming traffic from the server,
    displaying it on the terminal.
'''
def ReceiveData(sock, shutdown):
  while shutdown.is_set() == False:
    data = sock.recv(1024)
    data = data.decode('utf-8')
    data = data.split("\\")
    src = data[0]
    msg = data[1]
    print(f'{src}\n ┗> {msg}')


'''
    Function to send a message to the server.
'''
def SendData(sock, serverAddress, shutdown):
  while shutdown.is_set() == False:
    msg = input()
    msg = str.encode(msg)
    sock.sendto(msg, serverAddress)


'''
    Updated application UI prototype (still in development)
'''
def ChatUI(stdscr):
   # Initialize curses
    curses.curs_set(1)  # Show cursor
    stdscr.nodelay(1)  # Non-blocking input
    stdscr.timeout(100)  # 100 ms refresh rate

    # Clear the screen and reset the color settings
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Set color pair (white text on black background)
    stdscr.bkgd(' ', curses.color_pair(1))  # Set background color (apply to entire screen)
    
    # Ensure the terminal does not have default selected text or colors
    stdscr.refresh()

    # Setup screen height and width
    height, width = stdscr.getmaxyx()

    # Create windows for chat (scrolling) and input bar (static)
    chat_win = curses.newwin(height - 3, width, 0, 0)  # Conversation area
    input_win = curses.newwin(3, width, height - 3, 0)  # Input area (bottom bar)
    input_win.clear()

    chat_win.scrollok(True)  # Enable scrolling in the chat window

    # Store messages in a list
    chat_messages = ["Welcome to the Chat App! Type to begin."]
    input_text = ""

    while True:
        # Refresh the chat window with the latest messages
        chat_win.clear()
        for i, msg in enumerate(chat_messages[-(height - 4):]):  # Adjust to fit screen
            chat_win.addstr(i, 0, msg)
        chat_win.refresh()

        # Display the input bar
        input_win.clear()
        input_win.addstr(1, 1, f"Input: {input_text}")
        input_win.refresh()

        # Get user input in the input bar
        key = stdscr.getch()

        if key == 10:  # Enter key pressed
            if input_text:
                chat_messages.append(f"You: {input_text}")
                input_text = ""
        elif key == 27:  # Escape key pressed (exit)
            break
        elif key == 263:  # Backspace key
            input_text = input_text[:-1]
        else:
            # Add typed character to the input string
            input_text += chr(key) if key >= 32 and key <= 126 else ""


'''
    Client module's main function.
'''
def Client(localIP, localPort):
  print("[*] [ONLINE] Client status updated")
  serverAddress = (localIP, localPort)

  # Create a UDP socket
  server = s.socket(s.AF_INET, s.SOCK_DGRAM)

  # Connect to the server
  ConnectToServer(server, serverAddress)

  # Enable multithreading
  shutdown = t.Event()
  receptionThread = t.Thread(target=ReceiveData, args=(server, shutdown))
  sendingThread = t.Thread(target=SendData, args=(server, serverAddress, shutdown))
  # UIThread = t.Thread(target=ChatUI, args=())

  try:
    receptionThread.start()
    sendingThread.start()

    receptionThread.join()
    sendingThread.join()

  except KeyboardInterrupt:
    print("\n[*] Ctrl+C detected. Shutting down...")
    shutdown.set()
    sys.exit()
    receptionThread.join()
    sendingThread.join()
    server.close()

  print("[*] [OFFLINE] Client status updated")

Client('127.0.0.1', 9000)