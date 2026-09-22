with open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html', encoding='utf-8') as f:
    html = f.read()

# Find mansoor tab context
idx = html.find('data-child="mansoor"')
print("=== mansoor tab context ===")
print(repr(html[idx-10:idx+250]))
print()

# Find the tabs closing div
idx2 = html.find('switchTab(\'mansoor\')')
print("=== switchTab mansoor context ===")
print(repr(html[idx2-10:idx2+200]))
print()

# Find Firebase Integration comment
idx3 = html.find('<!-- Firebase Integration -->')
print("=== Firebase Integration context ===")
print(repr(html[idx3-50:idx3+50]))
print()

# Find switchTab function body
idx4 = html.find('panels.forEach(p => p.classList.remove')
print("=== switchTab body context ===")
print(repr(html[idx4-10:idx4+300]))
