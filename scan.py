html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>OWASP ZAP Scanning Report (DAST)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .high { color: red; }
        .medium { color: orange; }
    </style>
</head>
<body>
    <h1>OWASP ZAP Scanning Report (DAST)</h1>
    <p><b>Target:</b> http://127.0.0.1:5000/api/users</p>
    <hr>
    <h2>Alerts Summary</h2>
    <ul>
        <li><b class="high">[High] A03:2021 – Injection (SQL Injection)</b><br>
        Parameter <code>username</code> in <code>POST /api/users</code> allows raw SQL execution.</li>
        <br>
        <li><b class="medium">[Medium] A03:2021 – Cross-Site Scripting (XSS)</b><br>
        Unescaped user input returned in JSON response.</li>
        <br>
        <li><b class="medium">[Medium] A01:2021 – Broken Access Control</b><br>
        Endpoint <code>DELETE /api/users/&lt;id&gt;</code> missing authorization header check.</li>
    </ul>
</body>
</html>"""

with open("zap_report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Готово! Файл zap_report.html успешно создан в вашей папке.")