import tempfile

with tempfile.NamedTemporaryFile(delete=False) as tmp:
    print("Temp file path:", tmp.name)
