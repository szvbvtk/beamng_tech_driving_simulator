from pathlib import Path
import json

path = Path(__file__).parent.parent.resolve()
path = path.joinpath("server_config.json")

with open(path, "r") as server_config_file:
    server_config = json.load(server_config_file)
    tcp_host = server_config["host"]
    tcp_port = server_config["port"]

    print(tcp_host)