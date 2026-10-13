with open('/etc/nginx/sites-enabled/innercurrent', 'r', encoding='utf-8') as f:
    text = f.read()

rule = """    location ~* \\.html$ {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        expires 0;
    }

"""

if 'location ~* \\.html$' not in text:
    text = text.replace('location / {', rule + '    location / {')
    with open('/etc/nginx/sites-enabled/innercurrent', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Nginx configuration updated.")
else:
    print("Already configured.")
