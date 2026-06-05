import sys
import webbrowser
from agents.readme_agent import ReadmeAgent
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.planner import PlannerAgent
from core.task_executor import TaskExecutor


planner = PlannerAgent()
executor = TaskExecutor()
readme_agent = ReadmeAgent()

user_prompt = input("Describe your website: ")

plan = planner.create_plan(user_prompt)

print("\n===== PLAN =====")
print(plan.model_dump())

result = executor.execute(plan)

html_content = "\n".join(result["ui"])
css_content = result.get("css", "")

os.makedirs("output", exist_ok=True)

full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Website</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
{html_content}
</body>
</html>
"""

with open("output/index.html", "w", encoding="utf-8") as file:
    file.write(full_html)

print("\nWebsite saved at: output/index.html")

with open("output/styles.css", "w", encoding="utf-8") as file:
    file.write(css_content)

print("Styles saved at: output/styles.css")

readme_content = readme_agent.run(plan)

with open("output/README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)

print("README saved at: output/README.md")

print("\n===== GENERATED HTML =====\n")
print(html_content)

print("\n===== EXECUTION RESULT =====")
print(result)

website_path = os.path.abspath("output/index.html")
webbrowser.open(f"file://{website_path}")