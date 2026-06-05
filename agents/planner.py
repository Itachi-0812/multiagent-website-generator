from schemas.plan_schemas import Plan, Task
from core.intent_classifier import IntentClassifier
import uuid


class PlannerAgent:
    def __init__(self):
        self.classifier = IntentClassifier()

    def create_plan(self, prompt: str):
        intent = self.classifier.classify(prompt)
        website_type = intent["website_type"]

        structure = self._get_structure(website_type)
        tasks = self._build_tasks(structure, website_type)

        return Plan(
            website_type=website_type,
            pages=structure["pages"],
            components=structure["components"],
            tasks=tasks,
            user_prompt=prompt
        )

    def _get_structure(self, website_type: str):
        templates = {
            "portfolio": {
                "pages": ["Home", "Projects", "Contact"],
                "components": ["Navbar", "Hero", "Projects Grid", "Footer"]
            },
            "saas": {
                "pages": ["Home", "Pricing", "Contact"],
                "components": ["Navbar", "Hero", "Features", "Pricing", "Footer"]
            },
            "restaurant": {
                "pages": ["Home", "Menu", "Reservation", "Contact"],
                "components": ["Navbar", "Hero", "Menu Section", "Reservation Form", "Footer"]
            },
            "ecommerce": {
                "pages": ["Home", "Products", "Cart", "Checkout"],
                "components": ["Navbar", "Hero", "Product Grid", "Cart", "Checkout", "Footer"]
            },
            "blog": {
                "pages": ["Home", "Articles", "About", "Contact"],
                "components": ["Navbar", "Hero", "Article Grid", "Footer"]
            },
            "gym": {
                "pages": ["Home", "Programs", "Trainers", "Contact"],
                "components": ["Navbar", "Hero", "Programs Section", "Trainer Section", "Footer"]
            },
        }

        return templates.get(website_type, {
            "pages": ["Home"],
            "components": ["Navbar", "Hero", "Footer"]
        })

    def _build_tasks(self, structure: dict, website_type: str):
        tasks = []

        for comp in structure["components"]:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="UI_AGENT",
                task=f"Generate {comp}",
                depends_on=[]
            ))

        # Content tasks based on website type
        if website_type == "portfolio":
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate portfolio project descriptions",
                depends_on=[]
            ))

        elif website_type == "restaurant":
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate restaurant menu items and descriptions",
                depends_on=[]
            ))

        elif website_type == "blog":
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate blog article titles and summaries",
                depends_on=[]
            ))

        elif website_type == "saas":
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate SaaS feature descriptions and pricing content",
                depends_on=[]
            ))

        elif website_type == "ecommerce":
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate product names, descriptions, and categories",
                depends_on=[]
            ))

        elif website_type == "gym":
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate gym programs, trainer bios, and fitness content",
                depends_on=[]
            ))

        return tasks