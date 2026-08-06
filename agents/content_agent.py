import re


class ContentAgent:

    FOR_PATTERN = re.compile(r"\bfor\b")

    def _text_after_for(self, prompt_lower):
        match = self.FOR_PATTERN.search(prompt_lower)

        if not match:
            return None

        return prompt_lower[match.end():].strip()

    def generate_content(self, website_type: str, prompt: str):
        prompt_lower = prompt.lower()
        after_for = self._text_after_for(prompt_lower)

        if website_type == "gym":
            name = "Elite Fitness Gym"

            if after_for:
                name = after_for.title()

            return {
                "name": name,
                "role": "Transform Your Body, Transform Your Life",
                "project_title": "Strength Training",
                "project_description": "Personal training, cardio, strength workouts, and fitness coaching."
            }

        if website_type == "portfolio":
            name = "Portfolio Owner"
            role = "Software Developer"

            if after_for:
                parts = after_for.split()

                if len(parts) >= 1:
                    name = parts[0].capitalize()

                if len(parts) >= 2:
                    role = " ".join(parts[1:]).title()

            return {
                "name": name,
                "role": role,
                "project_title": "Multi-Agent Website Generator",
                "project_description": "An AI-powered system that generates websites from natural language prompts."
            }

        if website_type == "restaurant":
            name = "Spice Garden Restaurant"

            if after_for:
                name = after_for.title()

            return {
                "name": name,
                "role": "Delicious Food, Fresh Ingredients, Unforgettable Taste",
                "project_title": "Signature Menu",
                "project_description": "Enjoy chef-special dishes, family meals, desserts, and refreshing drinks."
            }

        if website_type == "blog":
            name = "Tech Daily Blog"

            if after_for:
                name = after_for.title()

            return {
                "name": name,
                "role": "Fresh Articles, Insights, and Stories",
                "project_title": "Latest Articles",
                "project_description": "Read trending posts, tutorials, guides, and expert opinions."
            }

        if website_type == "saas":
            name = "TaskFlow AI"

            if after_for:
                name = after_for.title()

            return {
                "name": name,
                "role": "Automate Your Workflow With Smart AI Tools",
                "project_title": "Powerful Features",
                "project_description": "Manage tasks, automate workflows, track analytics, and improve productivity."
            }

        if website_type == "ecommerce":
            name = "SneakerHub"

            if after_for:
                name = after_for.title()

            return {
                "name": name,
                "role": "Shop The Latest Products At Amazing Prices",
                "project_title": "Featured Products",
                "project_description": "Explore our best-selling products and exclusive offers."
            }

        return {
            "name": "Website Owner",
            "role": "Professional",
            "project_title": "Generated Project",
            "project_description": "Generated website content."
        }

    def run(self, task: str):
        return f"[CONTENT GENERATED] {task}"
