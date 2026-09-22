with open(r'C:\Users\sayefate\Desktop\Familien Schulplaner\index.html', encoding='utf-8') as f:
    html = f.read()

# Full mansoor tab block
idx = html.find("switchTab('mansoor')")
print("=== Mansoor tab full block ===")
print(repr(html[idx-100:idx+250]))
print()

# Find panels.forEach
idx2 = html.find('panels.forEach')
print(f"=== panels.forEach found at {idx2} ===")
if idx2 >= 0:
    print(repr(html[idx2-30:idx2+300]))
else:
    # search for switchTab function
    idx3 = html.find('function switchTab')
    print(f"function switchTab at {idx3}")
    if idx3 >= 0:
        print(repr(html[idx3:idx3+400]))
    else:
        idx4 = html.find('switchTab')
        print(f"First switchTab at {idx4}")
        print(repr(html[idx4:idx4+300]))
print()

# Search for Firebase keyword
idx5 = html.find('Firebase')
print(f"Firebase first occurrence at {idx5}:")
print(repr(html[idx5:idx5+200]))
