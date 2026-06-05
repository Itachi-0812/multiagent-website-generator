from schemas.plan_schemas import Plan, Task
from core.intent_classifier import IntentClassifier

import uuid


class PlannerAgent:

    def __init__(self):
        self.classifier = IntentClassifier()

    # ---------------- MAIN ENTRY ----------------
    def create_plan(self, prompt: str):

        intent = self.classifier.classify(prompt)
        website_type = intent["website_type"]

        structure = self._get_structure(website_type)
        tasks = self._build_tasks(structure)

        return Plan(
            website_type=website_type,
            pages=structure["pages"],
            components=structure["components"],
            tasks=tasks
        )

    # ---------------- STRUCTURE ----------------
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
                "components": ["Navbar", "Hero", "Menu Section", "Footer"]
            },

            "ecommerce": {
                "pages": ["Home", "Products", "Cart", "Checkout"],
                "components": ["Navbar", "Hero", "Product Grid", "Footer"]
            },

            "blog": {
                "pages": ["Home", "Articles", "About", "Contact"],
                "components": ["Navbar", "Hero", "Article Grid", "Footer"]
            }
        }

        return templates.get(website_type, {
            "pages": ["Home"],
            "components": ["Navbar", "Hero", "Footer"]
        })

    # ---------------- TASK BUILDER ----------------
    def _build_tasks(self, structure: dict):

        tasks = []

        # UI tasks
        for comp in structure["components"]:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="UI_AGENT",
                task=f"Generate {comp}",
                depends_on=[]
            ))

        components = structure["components"]

        # Content tasks
        if "Menu Section" in components:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate Restaurant Menu Content",
                depends_on=[]
            ))

        if "Product Grid" in components:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate Product Descriptions",
                depends_on=[]
            ))

        if "Article Grid" in components:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="CONTENT_AGENT",
                task="Generate Blog Articles",
                depends_on=[]
            ))

        # Backend tasks
        if "Cart" in components or "Checkout" in components:
            tasks.append(Task(
                id=str(uuid.uuid4()),
                agent="BACKEND_AGENT",
                task="Generate Cart + Checkout System",
                depends_on=[]
            ))

        return tasks