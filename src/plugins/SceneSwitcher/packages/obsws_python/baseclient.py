import base64
import hashlib
import json
import logging
from pathlib import Path
from random import randint

import websocket

from .error import OBSSDKError


class ObsClient:
    logger = logging.getLogger("baseclient.obsclient")

    def __init__(self, **kwargs):
        defaultkwargs = {"host": "localhost", "port": 4455, "password": "", "subs": 0}
        if not any(key in kwargs for key in ("host", "port", "password")):
            kwargs |= self._conn_from_toml()
        kwargs = defaultkwargs | kwargs
        for attr, val in kwargs.items():
            setattr(self, attr, val)

        self.logger.info(
            "Connecting with parameters: host='{host}' port={port} password='{password}' subs={subs}".format(
                **self.__dict__
            )
        )

        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws://{self.host}:{self.port}")
        self.server_hello = json.loads(self.ws.recv())

    def _conn_from_toml(self) -> dict:
        try:
            import tomllib
        except ModuleNotFoundError:
            import tomli as tomllib
        conn = {}
        filepath = Path.cwd() / "config.toml"
        if filepath.exists():
            with open(filepath, "rb") as f:
                conn = tomllib.load(f)
        return conn["connection"] if "connection" in conn else conn

    def authenticate(self):
        payload = {
            "op": 1,
            "d": {
                "rpcVersion": 1,
                "eventSubscriptions": self.subs,
            },
        }

        if "authentication" in self.server_hello["d"]:
            if not self.password:
                raise OBSSDKError("authentication enabled but no password provided")
            secret = base64.b64encode(
                hashlib.sha256(
                    (
                        self.password + self.server_hello["d"]["authentication"]["salt"]
                    ).encode()
                ).digest()
            )

            auth = base64.b64encode(
                hashlib.sha256(
                    (
                        secret.decode()
                        + self.server_hello["d"]["authentication"]["challenge"]
                    ).encode()
                ).digest()
            ).decode()

            payload["d"]["authentication"] = auth

        self.ws.send(json.dumps(payload))
        try:
            response = json.loads(self.ws.recv())
            return response["op"] == 2
        except json.decoder.JSONDecodeError:
            raise OBSSDKError("failed to identify client with the server")

    def req(self, req_type, req_data=None):
        payload = {
            "op": 6,
            "d": {"requestType": req_type, "requestId": randint(1, 1000)},
        }
        if req_data:
            payload["d"]["requestData"] = req_data
        self.logger.debug(f"Sending request {payload}")
        self.ws.send(json.dumps(payload))
        response = json.loads(self.ws.recv())
        self.logger.debug(f"Response received {response}")
        return response["d"]
