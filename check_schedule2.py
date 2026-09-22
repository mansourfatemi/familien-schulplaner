with open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html', encoding='utf-8') as f:
    html = f.read()

import re
# find all Stundenplan occurrences with more context
for m in re.finditer(r'Stundenplan', html):
    start = max(0, m.start()-120)
    end   = min(len(html), m.end()+200)
    print(repr(html[start:end]))
    print("---")
