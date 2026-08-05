from models.website_plan import WebsitePlan


class PlannerAgent:
    def create_plan(self, user_prompt: str) -> WebsitePlan:
        user_prompt = user_prompt.lower()

        if "portfolio" in user_prompt:
            return self._portfolio_plan()

        elif "restaurant" in user_prompt or "food" in user_prompt:
            return self._restaurant_plan()

        elif "blog" in user_prompt:
            return self._blog_plan()

        elif "business" in user_prompt or "company" in user_prompt:
            return self._business_plan()

        else:
            return self._generic_plan()

    def _portfolio_plan(self) -> WebsitePlan:
        return WebsitePlan(
            website_type="portfolio",
            sections=[
                "navbar",
                "hero",
                "about",
                "skills",
                "projects",
                "contact",
                "footer"
            ]
        )

    def _restaurant_plan(self) -> WebsitePlan:
        return WebsitePlan(
            website_type="restaurant",
            sections=[
                "navbar",
                "hero",
                "menu",
                "about",
                "contact",
                "footer"
            ]
        )

    def _blog_plan(self) -> WebsitePlan:
        return WebsitePlan(
            website_type="blog",
            sections=[
                "navbar",
                "hero",
                "featured_posts",
                "categories",
                "newsletter",
                "footer"
            ]
        )

    def _business_plan(self) -> WebsitePlan:
        return WebsitePlan(
            website_type="business",
            sections=[
                "navbar",
                "hero",
                "services",
                "about",
                "testimonials",
                "contact",
                "footer"
            ]
        )

    def _generic_plan(self) -> WebsitePlan:
        return WebsitePlan(
            website_type="generic",
            sections=[
                "navbar",
                "hero",
                "about",
                "services",
                "contact",
                "footer"
            ]
        )