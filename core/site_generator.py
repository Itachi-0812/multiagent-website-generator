import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from agents.planner import PlannerAgent
from core.task_executor import TaskExecutor


def clean_code(code):
    if not code:
        return ""

    code = code.strip()

    code = code.replace("```html", "")
    code = code.replace("```css", "")
    code = code.replace("```python", "")
    code = code.replace("```", "")

    return code.strip()


def generate_site(prompt, use_ai=True, save_files=True):
    planner = PlannerAgent()
    executor = TaskExecutor(use_ai=use_ai)

    plan = planner.create_plan(prompt)
    result = executor.execute(plan, prompt)

    cleaned_ui = []

    for section_html in result["ui"]:
        cleaned_ui.append(clean_code(section_html))

    html_content = "\n".join(cleaned_ui)
    css_content = clean_code(result["css"])

    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Generated Website</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
{html_content}
</body>
</html>
"""

    output_dir = os.path.join(PROJECT_ROOT, "output")
    html_path = os.path.join(output_dir, "index.html")
    css_path = os.path.join(output_dir, "styles.css")

    if save_files:
        os.makedirs(output_dir, exist_ok=True)

        with open(html_path, "w", encoding="utf-8") as file:
            file.write(full_html)

        with open(css_path, "w", encoding="utf-8") as file:
            file.write(css_content)

    return {
        "website_type": plan.website_type,
        "sections": plan.sections,
        "html": html_content,
        "css": css_content,
        "full_html": full_html,
        "html_path": html_path,
        "css_path": css_path
    }