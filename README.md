# CPU Scheduling Simulator - Fixed Version

## Run in VS Code

Open this folder in VS Code.

In the terminal:

```bash
pip install flask
python app.py
```

The browser should automatically open:

http://127.0.0.1:5000/

If it does not open, copy that URL into Chrome.

## Important folder structure

```text
CPU-Scheduler-Fixed/
│
├── app.py
├── scheduler.py
├── templates/
│   └── index.html
└── static/
    ├── script.js
    └── style.css
```

The original error `jinja2.exceptions.TemplateNotFound: index.html` happened because Flask was looking for `templates/index.html`, but that file/folder was missing from the project.
