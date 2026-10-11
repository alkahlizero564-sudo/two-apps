import json, os, re

u = os.environ.get("SB_URL", "").strip().rstrip("/")
k = os.environ.get("SB_KEY", "").strip()
p = "www/index.html"
s = open(p, encoding="utf-8").read()

if u and k:
    j = lambda v: json.dumps(v).replace("<", "\\u003c")
    tag = "<script>window.SUPABASE_URL=" + j(u) + ";window.SUPABASE_KEY=" + j(k) + ";</script>"
    m = re.search(r"<head(?:\s[^>]*)?>", s, re.I)
    if m:
        s = s[:m.end()] + tag + s[m.end():]
    else:
        d = re.match(r"\s*<!doctype[^>]*>", s, re.I)
        s = (s[:d.end()] + tag + s[d.end():]) if d else tag + s
    open(p, "w", encoding="utf-8").write(s)
    print("Supabase variables injected")
else:
    print("No Supabase secrets found, skipping")
