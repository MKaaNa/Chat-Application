---

# Chat Application

**Client Interface**

![Client Interface](images/client.png)



This project implements a basic chat application with server and client components. Users can exchange text messages and share files. The application demonstrates socket programming, multithreading, and includes a simple graphical user interface (GUI).

## Project Overview

The project consists of two main components:

1. **Server (`server.py`)**: A central server that manages user connections, handles incoming connections, and facilitates message broadcasting.
2. **Client (`client.py`)**: An application that allows users to connect to the server, participate in chat, and send files.

## Features

- **Real-Time Chat**: Users can send and receive text messages in real-time.
- **File Sharing**: Users can send and receive files.
- **Usernames**: Users specify a username before joining the chat.
- **Graphical User Interface (GUI)**: The client application provides a user-friendly interface.

## Technologies Used

- **Python**: The primary programming language used for the project.
- **Tkinter**: The Python library used for creating the GUI on the client side.
- **Socket**: The Python library used for network communication.
- **Threading**: The Python library used to handle multiple client connections simultaneously.

## Installation

### Prerequisites

- Python 3.x (Python 3.6 or later recommended)
- `tkinter` (comes with Python)
- `socket` and `threading` (part of Python standard library)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MKaaNa/chat-application.git
   cd chat-application
   ```

2. **Run the Server**

   To start the server, run the following command in your terminal or command prompt:

   ```bash
   python server.py
   ```

   The server will listen on port 3300 for incoming connections.

3. **Run the Client**

   To start the client, run the following command in your terminal or command prompt:

   ```bash
   python client.py
   ```

   The client application will prompt you to enter the server address. Provide the IP address of the server.

### Usage

1. **Start the Server**: Begin by starting the server.
2. **Start the Client**: Next, launch the client application and enter the server address.
3. **Chat**: In the client interface, type your messages and click the "Send" button.
4. **Send Files**: Click the "Send File" button to select and send a file.

## File Structure

- `server.py`: Server-side code.
- `client.py`: Client-side code.
- `README.md`: This file describing the project.

## Contributors

- [Kaan](https://github.com/MKaaNa): Project developer and maintainer.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for details.

---

**Notes**:
- Ensure you replace `https://github.com/MKaaNa/chat-application.git` with your actual GitHub repository URL.
- Create the `README.md` file in the root directory of your project.

This README file should help users understand and set up your project. If you need any additional assistance or modifications, feel free to ask!

---
