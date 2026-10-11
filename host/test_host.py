import struct, json, subprocess

p = subprocess.Popen(
    [r"C:\proyectos\url-logger\host\url_logger.bat"],
    stdin=subprocess.PIPE,
)
for url in ["https://example.com", "https://www.mozilla.org"]:
    data = json.dumps({"time": "prueba", "url": url}).encode("utf-8")
    p.stdin.write(struct.pack("=I", len(data)) + data)
p.stdin.close()  # simula el cierre de Firefox
p.wait()
print("El host terminó con código", p.returncode)