## Stack architecture

This application is made up of 3 Docker containers :

|   Service   |     Software     | Port  |              Description              |
| :---------: | :--------------: | :---: | :-----------------------------------: |
|   Web app   |   Flask 3.1.0    | 12345 |   Python webserver running the app    |
|     DB      |   MariaDB 10.6   | 3306  |               Database                |
| DB frontend | phpMyAdmin 5.2.2 | 12346 | Web interface for database management |

## Deployment

### Prerequisites

Docker Engine up and running. See https://docs.docker.com/engine/install/ if needed.

### How to install
Clone the repo
```bash
git clone https://github.com/colpiche/dev-simulation.git
```

Cd into it :
```bash
cd dev-simulation
```

Deploy the stack
```bash
docker compose up -d
```

### How to use
To access the webapp, open your browser and go to :

```bash
http://ip-of-your-server:12345/
```