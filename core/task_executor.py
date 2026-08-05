from agents.content_agent import ContentAgent
from agents.ui_agent import UIAgent
from agents.style_agent import StyleAgent


class TaskExecutor:
    def __init__(self, use_ai=True):
        self.use_ai = use_ai
        self.content_agent = ContentAgent()
        self.ui_agent = UIAgent()
        self.style_agent = StyleAgent()

    def execute(self, plan, user_prompt=""):
        content_data = {}

        if self.use_ai:
            try:
                content_data = self.content_agent.generate_content(
                    website_type=plan.website_type,
                    prompt=user_prompt
                )
            except Exception as error:
                print("\nContentAgent failed. Using local content fallback.")
                print("Error:", error)

        html_code = ""

        if self.use_ai:
            try:
                html_code = self.ui_agent.run(
                    task="full_website",
                    content_data=content_data,
                    pages=plan.sections,
                    website_type=plan.website_type,
                    user_prompt=user_prompt
                )
            except Exception as error:
                print("\nUIAgent failed. Using local HTML fallback.")
                print("Error:", error)

        if not html_code or not html_code.strip():
            html_code = self.local_full_html_fallback(
                plan.website_type,
                plan.sections,
                user_prompt
            )

        css_code = ""

        if self.use_ai:
            try:
                css_code = self.style_agent.run(
                    website_type=plan.website_type,
                    user_prompt=user_prompt,
                    html_code=html_code
                )
            except Exception as error:
                print("\nStyleAgent failed. Using local CSS fallback.")
                print("Error:", error)

        if not css_code or not css_code.strip():
            css_code = self.local_css_fallback()

        return {
            "ui": [html_code],
            "css": css_code
        }

    def local_full_html_fallback(self, website_type, sections, user_prompt=""):
        html_sections = []

        for section in sections:
            html_sections.append(
                self.local_section_fallback(section, website_type, user_prompt)
            )

        return "\n".join(html_sections)

    def local_section_fallback(self, section, website_type, user_prompt=""):
        if section == "navbar":
            name = self.extract_name(user_prompt)

            if website_type == "portfolio":
                brand = f"{name} Portfolio"
            else:
                brand = self.brand_name(website_type)

            return f"""
<nav class="navbar {website_type}-nav">
    <h2>{brand}</h2>
    <ul>
        {self.nav_links(website_type)}
    </ul>
</nav>
"""

        elif section == "hero":
            return self.hero_section(website_type, user_prompt)

        elif section == "about":
            return f"""
<section class="about">
    <h2>{self.about_title(website_type)}</h2>
    <p>{self.about_text(website_type, user_prompt)}</p>
</section>
"""

        elif section == "skills":
            return """
<section class="skills">
    <h2>Skills</h2>
    <div class="card-container">
        <div class="card">Python</div>
        <div class="card">HTML & CSS</div>
        <div class="card">JavaScript</div>
        <div class="card">AI Tools</div>
    </div>
</section>
"""

        elif section == "projects":
            return """
<section class="projects">
    <h2>Projects</h2>
    <div class="card-container">
        <div class="card">
            <h3>Multiagent Website Generator</h3>
            <p>A system that creates websites from text prompts.</p>
        </div>
        <div class="card">
            <h3>Portfolio Website</h3>
            <p>A clean personal portfolio to showcase skills and projects.</p>
        </div>
    </div>
</section>
"""

        elif section == "services":
            return """
<section class="services">
    <h2>Our Services</h2>
    <div class="card-container">
        <div class="card">
            <h3>Web Design</h3>
            <p>Modern and responsive website design.</p>
        </div>
        <div class="card">
            <h3>Development</h3>
            <p>Reliable web development solutions.</p>
        </div>
        <div class="card">
            <h3>Marketing</h3>
            <p>Grow your business with digital strategy.</p>
        </div>
    </div>
</section>
"""

        elif section == "menu":
            return """
<section class="menu-section" id="menu">
    <h2>Our Popular Menu</h2>
    <div class="card-container">
        <div class="card">
            <h3>Margherita Pizza</h3>
            <p>Classic pizza with fresh basil and mozzarella.</p>
            <strong>₹299</strong>
        </div>
        <div class="card">
            <h3>Paneer Burger</h3>
            <p>Spicy paneer patty with fresh vegetables.</p>
            <strong>₹199</strong>
        </div>
        <div class="card">
            <h3>Chocolate Dessert</h3>
            <p>Rich chocolate dessert for sweet cravings.</p>
            <strong>₹149</strong>
        </div>
    </div>
</section>
"""

        elif section == "featured_posts":
            return """
<section class="featured-posts">
    <h2>Featured Posts</h2>
    <div class="card-container">
        <div class="card">
            <h3>How AI Helps Web Development</h3>
            <p>A beginner-friendly article about AI and coding.</p>
        </div>
        <div class="card">
            <h3>Design Tips for Beginners</h3>
            <p>Simple ways to make websites look cleaner.</p>
        </div>
    </div>
</section>
"""

        elif section == "categories":
            return """
<section class="categories">
    <h2>Categories</h2>
    <div class="card-container">
        <div class="card">Technology</div>
        <div class="card">Lifestyle</div>
        <div class="card">Business</div>
    </div>
</section>
"""

        elif section == "newsletter":
            return """
<section class="newsletter">
    <h2>Join Our Newsletter</h2>
    <p>Subscribe to receive latest updates.</p>
    <input type="email" placeholder="Enter your email">
    <button>Subscribe</button>
</section>
"""

        elif section == "testimonials":
            return """
<section class="testimonials">
    <h2>Testimonials</h2>
    <p>"Amazing service and professional results."</p>
</section>
"""

        elif section == "contact":
            return f"""
<section class="contact" id="contact">
    <h2>{self.contact_title(website_type)}</h2>
    <p>Email: {self.contact_email(website_type)}</p>
    <p>Phone: +91 98765 43210</p>
</section>
"""

        elif section == "footer":
            return f"""
<footer>
    <p>&copy; 2026 {self.brand_name(website_type)}. All rights reserved.</p>
</footer>
"""

        else:
            return f"""
<section class="{section}">
    <h2>{section.title()}</h2>
    <p>This section was generated using fallback mode.</p>
</section>
"""

    def extract_name(self, user_prompt):
        words = user_prompt.replace(",", " ").replace(".", " ").split()
        trigger_words = ["for", "named", "called"]

        for index, word in enumerate(words):
            if word.lower() in trigger_words and index + 1 < len(words):
                possible_name = words[index + 1]

                if possible_name.isalpha():
                    return possible_name.title()

        return "Harsh"

    def brand_name(self, website_type):
        names = {
            "restaurant": "FoodVilla",
            "business": "GrowthCorp",
            "portfolio": "Harsh Portfolio",
            "blog": "DailyBlogs",
            "generic": "Generated Website"
        }

        return names.get(website_type, "Generated Website")

    def nav_links(self, website_type):
        links = {
            "restaurant": ["Home", "Menu", "About", "Reserve"],
            "business": ["Home", "Services", "About", "Clients", "Contact"],
            "portfolio": ["Home", "About", "Skills", "Projects", "Contact"],
            "blog": ["Home", "Posts", "Categories", "Newsletter"],
            "generic": ["Home", "About", "Services", "Contact"]
        }

        selected_links = links.get(website_type, links["generic"])
        return "".join([f"<li>{link}</li>" for link in selected_links])

    def hero_section(self, website_type, user_prompt=""):
        if website_type == "portfolio":
            name = self.extract_name(user_prompt)
            title = f"Hi, I'm {name}"
            subtitle = "A passionate web developer and AI enthusiast building clean, modern digital experiences."
            button = "View My Work"

        elif website_type == "restaurant":
            title = "Delicious Food, Freshly Served"
            subtitle = "Enjoy handcrafted meals made with fresh ingredients and rich flavors."
            button = "View Menu"

        elif website_type == "business":
            title = "We Help Businesses Grow Online"
            subtitle = "Professional digital solutions for startups, brands, and enterprises."
            button = "Get Consultation"

        elif website_type == "blog":
            title = "Stories, Ideas & Insights"
            subtitle = "Explore articles on technology, lifestyle, productivity, and creativity."
            button = "Read Latest Posts"

        else:
            title = "Welcome to Your Generated Website"
            subtitle = "This website was created using your multiagent website generator."
            button = "Get Started"

        return f"""
<section class="hero {website_type}-hero">
    <div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
        <a href="#contact" class="btn">{button}</a>
    </div>
</section>
"""

    def about_title(self, website_type):
        titles = {
            "restaurant": "About Our Restaurant",
            "business": "About Our Company",
            "portfolio": "About Me",
            "blog": "About This Blog",
            "generic": "About Us"
        }

        return titles.get(website_type, "About Us")

    def about_text(self, website_type, user_prompt=""):
        if website_type == "portfolio":
            name = self.extract_name(user_prompt)
            return f"{name} is a passionate web developer and AI enthusiast focused on building useful, clean, and modern web projects."

        texts = {
            "restaurant": "We serve freshly prepared meals inspired by traditional recipes and modern taste.",
            "business": "We help businesses improve their online presence through strategy, design, and development.",
            "blog": "A space for sharing practical ideas, personal experiences, tutorials, and helpful guides.",
            "generic": "This is a modern generated website built using a multiagent system."
        }

        return texts.get(website_type, texts["generic"])

    def contact_title(self, website_type):
        titles = {
            "restaurant": "Reserve a Table",
            "business": "Contact Us",
            "portfolio": "Contact Me",
            "blog": "Contact the Author",
            "generic": "Contact Us"
        }

        return titles.get(website_type, "Contact Us")

    def contact_email(self, website_type):
        emails = {
            "restaurant": "booking@foodvilla.com",
            "business": "contact@growthcorp.com",
            "portfolio": "harsh@example.com",
            "blog": "writer@example.com",
            "generic": "contact@example.com"
        }

        return emails.get(website_type, "contact@example.com")

    def local_css_fallback(self):
        return """
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    color: #222;
    background: #ffffff;
}

.navbar {
    color: white;
    padding: 18px 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.restaurant-nav {
    background: #7f1d1d;
}

.business-nav {
    background: #1e3a8a;
}

.portfolio-nav {
    background: #111827;
}

.blog-nav {
    background: #365314;
}

.generic-nav {
    background: #222;
}

.navbar h2 {
    margin: 0;
}

.navbar ul {
    list-style: none;
    display: flex;
    gap: 22px;
    margin: 0;
    padding: 0;
}

.hero {
    min-height: 420px;
    padding: 90px 50px;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
}

.hero h1 {
    font-size: 46px;
    margin-bottom: 15px;
}

.hero p {
    font-size: 19px;
    max-width: 700px;
    margin: 0 auto;
}

.restaurant-hero {
    background: #fee2e2;
}

.business-hero {
    background: #dbeafe;
}

.portfolio-hero {
    background: #e5e7eb;
}

.blog-hero {
    background: #ecfccb;
}

.generic-hero {
    background: #f4f4f4;
}

.btn,
button {
    display: inline-block;
    margin-top: 22px;
    background: #222;
    color: white;
    padding: 13px 28px;
    text-decoration: none;
    border: none;
    border-radius: 6px;
}

section {
    padding: 60px 50px;
    text-align: center;
}

section h2 {
    font-size: 32px;
    margin-bottom: 20px;
}

.card-container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 25px;
    margin-top: 25px;
}

.card {
    width: 260px;
    background: #f8f8f8;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}

.menu-section .card {
    background: #fff7ed;
}

.newsletter {
    background: #f4f4f4;
}

.newsletter input {
    padding: 12px;
    width: 280px;
    max-width: 90%;
}

footer {
    background: #222;
    color: white;
    text-align: center;
    padding: 22px;
}
"""