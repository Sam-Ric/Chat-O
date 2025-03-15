# ➤ Python UDP Chat v1.0

Simple CLI chatting application, working within a local network.

This project contains the following elements:

- ### Server module

  Responsible for managing the traffic from the clients within the local network, having two main functions:

  - Connecting clients

  - Receiving traffic from a client and redirecting it to the other clients connected to the server

  > ***Note:*** At the moment, a message's source is displayed as the host's IP address and port. In the future, a translation mechanism will be implemented to display the message authors using the respective usernames.

- ### Client module

  Element that allows users to interact with each other.
  
  The user can see messages from other users connected to the server and can also send messages to those users by typing the desired text on the terminal.

<br>

## 📋 To Be Implemented

- UI improvements (static input bar and dynamic chat history)

- Add support for external devices (current version only works within the local host 127.0.0.1)

<br>

## 📝 Changelog

#### 15/03/2025 - v1.0

- Started the repository

- Prototype of both the client and the server modules (exclusively supports local hosts)
