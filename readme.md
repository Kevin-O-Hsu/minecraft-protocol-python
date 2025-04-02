
# Minecraft Protocol Python

[![Discord](https://img.shields.io/badge/chat-discord-blue)](https://discord.gg/FkyNrjgpm5)  

## Overview

Minecraft Protocol Python provides a library to **parse and serialize Minecraft packets**, as well as support **authentication and encryption**. This library is designed to be **up-to-date with the Minecraft protocol** and focuses on version 1.21.4 for now, with future plans to expand to more versions.

## Features

- **Supports Minecraft PC version 1.21.4**

- **Core Features:**
  - Parses **all packets** and emits events with packet fields as Python objects.
  - **Send a packet** by supplying fields as a Python object.
  - **Client-Side**:  
    - Authentication and logging in
    - Encryption
    - Compression
    - Online and offline mode
    - Respond to keep-alive packets
    - Follow DNS service records (SRV)
    - Ping a server for status
  - **Server-Side**:  
    - Online/Offline mode
    - Encryption
    - Compression
    - Handshake
    - Keep-alive checking
    - Ping status

## Development Status

**Under development**  
This project is currently under development and is **not ready for production use** yet. Only Minecraft 1.21.4 is developing.

## Installation

```bash
pip install minecraft-protocol-python
```

## Usage Example

```
There is no usage example yet.
```

## License

GPL3.0 License. See [LICENSE](LICENSE) for details.

---

## Roadmap

- **Future updates:**
  - Support for newer Minecraft versions
  - More robust error handling
  - Improvements in packet parsing speed
  - Enhanced documentation and examples


