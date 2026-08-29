import os

target_dir = r"C:\Users\euntaewoo\Desktop\이미지번역워크스페이스"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if '1.5' in content:
        # README.md specific replacement
        content = content.replace('', '')
        
        # General replacements to purge 1.5 and replace with 3.1
        content = content.replace('gemini-3.1-pro-preview', 'gemini-3.1-pro-preview')
        content = content.replace('gemini-3.1-flash-image', 'gemini-3.1-flash-image')
        content = content.replace('gemini-3.1', 'gemini-3.1')
        content = content.replace('3.1-pro-preview', '3.1-pro-preview')
        content = content.replace('3.1-flash-image', '3.1-flash-image')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

for root, _, files in os.walk(target_dir):
    for file in files:
        if file.endswith('.md') or file.endswith('.py'):
            process_file(os.path.join(root, file))
