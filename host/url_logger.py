#!/usr/bin/env python3
import sys, struct, json, os

# Archivo donde se guardan las URLs. Cámbialo si prefieres otra ruta.
LOG_FILE = r"C:\proyectos\url-logger\urls.txt"


def read_message():
    """Lee un mensaje del protocolo de Native Messaging (4 bytes de longitud + JSON)."""
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) < 4:
        return None  # Firefox cerró la conexión: hay que salir
    length = struct.unpack("=I", raw_length)[0]
    data = sys.stdin.buffer.read(length)
    if len(data) < length:
        return None
    return json.loads(data.decode("utf-8"))


def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    while True:
        try:
            msg = read_message()
        except (ValueError, struct.error):
            continue  # mensaje mal formado: lo ignoramos y seguimos
        if msg is None:
            break
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f'{msg["time"]}\t{msg["url"]}\n')
        except (OSError, KeyError):
            pass  # no queremos que un fallo puntual mate el proceso


if __name__ == "__main__":
    main()