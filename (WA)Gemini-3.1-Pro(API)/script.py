
import urllib.request
import re
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.luogu.com.cn/problem/solution/SP34103', headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
    print('Length:', len(html))
    import urllib.parse
    html = urllib.parse.unquote(html)
    for m in re.finditer(r'a_n', html):
        start = max(0, m.start() - 100)
        end = min(len(html), m.end() + 100)
        print(html[start:end])
except Exception as e:
    print('Error:', e)

