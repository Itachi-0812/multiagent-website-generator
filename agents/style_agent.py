from llm_client import ask_gemini


class StyleAgent:
    def run(self, website_type="website", user_prompt="", html_code=""):
        prompt = f"""
You are a professional CSS styling agent.

Website Type:
{website_type}

User Request:
{user_prompt}

HTML Code:
{html_code}

Generate modern responsive CSS for this website.

Rules:
- Return only CSS.
- Do not return markdown.
- Do not use ```css.
- Use clean spacing.
- Make navbar, hero, cards, forms, buttons, and footer look modern.
- Use responsive design.
- Use a professional color palette.
"""

        try:
            return ask_gemini(prompt)

        except Exception as error:
            print("\nGemini failed or quota exceeded. Using local fallback CSS.")
            print("Error:", error)

            return self.local_fallback_css(website_type)

    def local_fallback_css(self, website_type="website"):
        return """
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: #f8f5f0;
    color: #222;
    line-height: 1.6;
}

.navbar {
    background: #111;
    color: white;
    padding: 18px 8%;
}

.navbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.navbar ul,
.navbar-links {
    display: flex;
    gap: 24px;
    list-style: none;
}

.navbar a {
    color: white;
    text-decoration: none;
    font-weight: 600;
}

.hero,
.hero-section {
    min-height: 70vh;
    padding: 80px 8%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, #ffecd2, #fcb69f);
}

.hero h1,
.hero-title {
    font-size: 48px;
    margin-bottom: 16px;
}

.hero p,
.hero-description {
    font-size: 20px;
    margin-bottom: 24px;
}

.btn,
.button,
.form-button {
    display: inline-block;
    background: #d35400;
    color: white;
    padding: 12px 24px;
    border-radius: 30px;
    border: none;
    text-decoration: none;
    cursor: pointer;
    font-weight: bold;
}

.menu-section,
.reservation-section,
.reservation-form-section,
.projects,
.articles,
.features,
.pricing,
.products,
.cart,
.checkout {
    padding: 70px 8%;
}

.menu-section h2,
.reservation-section h2,
.form-title,
.section-title {
    text-align: center;
    font-size: 36px;
    margin-bottom: 16px;
}

.section-description,
.form-description {
    text-align: center;
    margin-bottom: 40px;
    color: #555;
}

.menu-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 24px;
}

.menu-card,
.project-card,
.article-card,
.feature-card,
.pricing-card,
.product-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.menu-card img {
    width: 100%;
    border-radius: 14px;
    margin-bottom: 16px;
}

.menu-card h3,
.menu-item-title {
    margin-bottom: 10px;
}

.menu-card span,
.menu-item-price {
    display: inline-block;
    margin-top: 12px;
    color: #d35400;
    font-weight: bold;
}

.reservation-form,
form {
    max-width: 650px;
    margin: 0 auto;
    background: white;
    padding: 32px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.form-group {
    margin-bottom: 18px;
}

input,
select,
textarea {
    width: 100%;
    padding: 13px;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 15px;
}

label {
    display: block;
    margin-bottom: 6px;
    font-weight: bold;
}

.footer {
    background: #111;
    color: white;
    padding: 40px 8%;
    text-align: center;
}

.footer a {
    color: white;
}

.footer-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
}

@media (max-width: 768px) {
    .navbar-container {
        flex-direction: column;
        gap: 16px;
    }

    .navbar ul,
    .navbar-links {
        flex-direction: column;
        text-align: center;
    }

    .hero h1,
    .hero-title {
        font-size: 34px;
    }
}
"""
