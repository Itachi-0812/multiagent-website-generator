import os
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from core.site_generator import generate_site


app = FastAPI(
    title="Multiagent Website Generator API",
    description="API for generating websites using a multiagent system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WebsiteRequest(BaseModel):
    prompt: str


class WebsiteResponse(BaseModel):
    website_type: str
    sections: list[str]
    html: str
    css: str


def build_premium_prompt(user_prompt: str) -> str:
    return f"""
You are a senior frontend engineer and award-winning UI/UX designer.

Generate a complete, premium, production-quality website based on the user's description.

User website description:
"{user_prompt}"

MAIN GOAL:
Create a visually rich, professional, detailed website that looks like a real business website.
Do not generate a basic/simple landing page unless the user specifically asks for a simple website.

WEBSITE STRUCTURE REQUIREMENTS:
The website must include multiple meaningful sections such as:

1. Navbar
   - Brand/logo text
   - Navigation links
   - CTA button

2. Hero section
   - Strong headline
   - Supporting subheadline
   - Primary CTA button
   - Secondary CTA button
   - Visual element/card/mockup/gradient panel

3. Features or Services section
   - At least 4 to 6 cards
   - Icons or visual markers
   - Short useful descriptions

4. About or Explanation section
   - Explain what the website/business/product does
   - Use clean two-column layout if suitable

5. Process / How it Works section
   - Step-by-step flow
   - At least 3 steps

6. Benefits section
   - Show why users should choose this
   - Use cards, badges, or highlighted stats

7. Testimonials / Social Proof section
   - Add realistic testimonials
   - Add names/roles if suitable

8. Pricing / Packages section
   - Include if relevant to the user's request
   - Add at least 3 pricing cards if suitable

9. FAQ section
   - At least 4 frequently asked questions

10. Strong CTA section
   - Final conversion-focused section

11. Footer
   - Brand name
   - Useful links
   - Contact/social style links

DESIGN REQUIREMENTS:
- Premium SaaS/startup/business style
- Modern typography
- Strong visual hierarchy
- Beautiful spacing
- Responsive layout
- Cards with shadows/borders
- Gradients where suitable
- Hover effects
- Smooth transitions
- Badges, stats, icons, and visual elements
- No boring plain white beginner layout
- No Lorem Ipsum
- Use realistic content related to the user's prompt
- Make it feel complete and production-ready

TECHNICAL REQUIREMENTS:
- Return proper HTML and CSS according to the existing project structure.
- Keep HTML and CSS clean and organized.
- Use semantic HTML.
- Use responsive CSS.
- Do not include explanations outside the generated website code.
- Do not make the website too short.
- Generate a complete full-page website.

IMPORTANT:
The final website should feel like a real business website, not a demo, not a beginner template, and not a simple one-section landing page.
"""


@app.get("/")
def home():
    return {
        "message": "Multiagent Website Generator API is running"
    }


@app.post("/generate-website", response_model=WebsiteResponse)
def generate_website(request: WebsiteRequest):
    final_prompt = build_premium_prompt(request.prompt)

    result = generate_site(
        prompt=final_prompt,
        use_ai=True,
        save_files=False
    )

    return WebsiteResponse(
        website_type=result["website_type"],
        sections=result["sections"],
        html=result["html"],
        css=result["css"]
    )


@app.post("/generate-and-preview", response_model=WebsiteResponse)
def generate_and_preview(request: WebsiteRequest):
    final_prompt = build_premium_prompt(request.prompt)

    result = generate_site(
        prompt=final_prompt,
        use_ai=True,
        save_files=True
    )

    return WebsiteResponse(
        website_type=result["website_type"],
        sections=result["sections"],
        html=result["html"],
        css=result["css"]
    )


@app.get("/preview", response_class=HTMLResponse)
def preview_website():
    html_path = os.path.join(PROJECT_ROOT, "output", "index.html")

    if not os.path.exists(html_path):
        return """
        <h1>No preview available</h1>
        <p>Generate a website first using POST /generate-and-preview.</p>
        """

    with open(html_path, "r", encoding="utf-8") as file:
        return file.read()


@app.get("/preview-css", response_class=HTMLResponse)
def preview_css():
    css_path = os.path.join(PROJECT_ROOT, "output", "styles.css")

    if not os.path.exists(css_path):
        return ""

    with open(css_path, "r", encoding="utf-8") as file:
        css_content = file.read()

    return HTMLResponse(
        content=css_content,
        media_type="text/css"
    )


@app.get("/styles.css", response_class=HTMLResponse)
def styles_css():
    css_path = os.path.join(PROJECT_ROOT, "output", "styles.css")

    if not os.path.exists(css_path):
        return ""

    with open(css_path, "r", encoding="utf-8") as file:
        css_content = file.read()

    return HTMLResponse(
        content=css_content,
        media_type="text/css"
    )