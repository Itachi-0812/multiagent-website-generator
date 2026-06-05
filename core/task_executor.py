from agents.ui_agent import UIAgent
from agents.content_agent import ContentAgent
from agents.style_agent import StyleAgent


class TaskExecutor:
    def __init__(self):
        self.ui_agent = UIAgent()
        self.content_agent = ContentAgent()
        self.style_agent = StyleAgent()

    def execute(self, plan):
        results = {
            "ui": [],
            "content": [],
            "backend": [],
            "css": ""
        }

        content_data = None

        for task in plan.tasks:
            if task.agent == "CONTENT_AGENT":
                content_data = self.content_agent.run(plan.user_prompt)
                results["content"].append(content_data)

            elif task.agent == "UI_AGENT":
                result = self.ui_agent.run(
                    task=task.task,
                    content_data=content_data,
                    pages=plan.pages,
                    website_type=plan.website_type,
                    user_prompt=plan.user_prompt
                )
                results["ui"].append(result)

        full_html = "\n".join(results["ui"])

        css = self.style_agent.run(
            website_type=plan.website_type,
            user_prompt=plan.user_prompt,
            html_code=full_html
        )

        results["css"] = css

        return results