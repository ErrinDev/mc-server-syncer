# Minecraft Server Syncer

A central coordination server for synchronizing data across multiple Minecraft servers.

## Overview

Minecraft Server Syncer acts as a centralized database wrapper that enables seamless data synchronization between different Minecraft servers. This allows players to maintain consistent progress, inventories, achievements, and other data across a network of Minecraft servers.

## Features

- **Central Database Management**: Coordinates a shared database for multiple Minecraft servers
- **Data Synchronization**: Keeps player data consistent across different servers
- **Interactive CLI**: Command-line interface for managing the synchronization service
- **Future HTTP API**: Will support RESTful API access for integration with other services (in development)

## Requirements

- Python 3.6+
- MySQL/MariaDB database
- Required Python packages:
  - dotenv
  - pymysql
  - pyyaml

## Setup

1. Clone this repository
2. Create a `.env` file with the following variables:
   ```
   DB_HOST=your_database_host
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_NAME=your_database_name
   ```
3. Configure your tables in `config.yml`
4. Run `python main.py` to start the service

## CLI Commands

The interactive CLI provides the following commands:

- `help` - Shows available commands
- `status` - Checks database connection status
- `tables` - Lists tables and row counts
- `exit`/`quit`/`stop` - Exits the program

## Configuration

Edit `config.yml` to configure the tables that should be synchronized across servers:

```yaml
tables:
  - users
  - servers
  - sync_logs
  - permissions
```

## Future Plans

- RESTful HTTP API for remote integration
- Pre built server agents

## License

MIT License, see LICENSE file for more info
