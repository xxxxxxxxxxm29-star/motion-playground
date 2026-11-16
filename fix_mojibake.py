import pathlib, sys

p = pathlib.Path("auth_app.py")
p.with_suffix(".py.bak").write_bytes(p.read_bytes())

t = p.read_bytes().decode("utf-8-sig")

try:
    fixed = t.encode("cp1251").decode("utf-8")
except Exception as e:
    print(f"SKIP (file might already be correct): {e}")
    sys.exit(0)

p.write_text(fixed, encoding="utf-8", newline="\n")
print("FIXED: encoding restored")