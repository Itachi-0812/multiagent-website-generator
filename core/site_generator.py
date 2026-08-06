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


def generate_site(prompt, use_ai=True, save_files=True, generate_backend=False):
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

    backend_data = None
    if generate_backend:
        from agents.backend_generator import BackendGenerator
        backend_gen = BackendGenerator()
        backend_data = backend_gen.generate_backend(
            website_type=plan.website_type,
            website_name=extract_website_name(prompt),
            sections=plan.sections
        )

        if save_files:
            backend_output_dir = os.path.join(PROJECT_ROOT, "output", "backend")
            os.makedirs(backend_output_dir, exist_ok=True)

            with open(os.path.join(backend_output_dir, "main.py"), "w", encoding="utf-8") as file:
                file.write(backend_data["main_app"])

            with open(os.path.join(backend_output_dir, "models.py"), "w", encoding="utf-8") as file:
                file.write(backend_data["models"])

            with open(os.path.join(backend_output_dir, "admin.html"), "w", encoding="utf-8") as file:
                file.write(backend_data["admin_dashboard"])

            with open(os.path.join(backend_output_dir, "requirements.txt"), "w", encoding="utf-8") as file:
                file.write(backend_data["requirements"])

            with open(os.path.join(backend_output_dir, ".env.example"), "w", encoding="utf-8") as file:
                file.write(backend_data["env_template"])

    result = {
        "website_type": plan.website_type,
        "sections": plan.sections,
        "html": html_content,
        "css": css_content,
        "full_html": full_html,
        "html_path": html_path,
        "css_path": css_path
    }

    if backend_data:
        result["backend"] = backend_data
        result["backend_path"] = os.path.join(output_dir, "backend")

    return result


def extract_website_name(prompt):
    words = prompt.split()
    if len(words) > 2:
        return " ".join(words[:3]).title()
    return "Generated Website"