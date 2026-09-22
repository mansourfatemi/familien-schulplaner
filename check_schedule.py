with open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html.bak_history_20260916', encoding='utf-8') as f:
    html = f.read()

# Find all references to Stundenplan
import re
for m in re.finditer(r'.{0,80}[Ss]tundenplan.{0,80}', html):
    print(repr(m.group()))
    print()
