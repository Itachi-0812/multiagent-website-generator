from llm_client import ask_gemini


class StyleAgent:
    def run(self, website_type="website", user_prompt="", html_code=""):
        prompt = f"""
You are a professional CSS and Tailwind CSS expert specializing in responsive web design.

Website Type: {website_type}
User Request: {user_prompt}

Generated HTML Code:
{html_code}

Your task:
Generate ONLY high-quality, production-ready CSS that complements the above HTML.

CSS Requirements:
- Use modern CSS3 features (flexbox, grid, transitions, animations)
- Ensure fully responsive design (mobile-first approach)
- Include smooth animations and hover effects
- Add custom color schemes appropriate for the website type
- Include media queries for responsive breakdowns (mobile, tablet, desktop)
- Use CSS variables for colors and spacing for easy customization
- Do NOT include Tailwind @apply directives or any Tailwind configuration
- Do NOT include HTML or any explanation
- Focus on enhancing the visual appeal and responsiveness
- Add custom animations, transitions, and interactive effects
- Ensure excellent typography and spacing
- Include dark mode support if appropriate

Return ONLY valid CSS code, no markdown, no explanation, no backticks.
"""

        try:
            return ask_gemini(prompt)
        except Exception as error:
            print("\nGemini CSS generation failed. Using local fallback.")
            print("Error:", error)
            return self.local_fallback_css(website_type)

    def local_fallback_css(self, website_type="website"):
        return """
/* Global Styles */
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --text-dark: #111827;
    --text-light: #6b7280;
    --bg-light: #f9fafb;
    --bg-white: #ffffff;
    --border-color: #e5e7eb;
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-dark);
    background-color: var(--bg-white);
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
}

h1 { font-size: 3rem; }
h2 { font-size: 2.25rem; }
h3 { font-size: 1.875rem; }
h4 { font-size: 1.5rem; }
h5 { font-size: 1.25rem; }
h6 { font-size: 1rem; }

p {
    margin-bottom: 1rem;
    color: var(--text-light);
}

/* Links */
a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover {
    color: var(--secondary-color);
}

/* Buttons */
button, .btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

button:hover, .btn:hover {
    background-color: var(--secondary-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

/* Sections */
section {
    padding: 4rem 2rem;
    max-width: 100%;
}

/* Cards */
.card {
    background: var(--bg-white);
    border: 1px solid var(--border-color);
    border-radius: 0.75rem;
    padding: 1.5rem;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

/* Grid & Flexbox */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.grid {
    display: grid;
    gap: 2rem;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.flex {
    display: flex;
    gap: 1rem;
}

.flex-col {
    flex-direction: column;
}

.flex-center {
    justify-content: center;
    align-items: center;
}

/* Responsive */
@media (max-width: 768px) {
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.25rem; }

    section {
        padding: 2rem 1rem;
    }

    .container {
        padding: 0 1rem;
    }

    .grid {
        grid-template-columns: 1fr;
    }
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.animate-fade-in {
    animation: fadeIn 0.6s ease-out forwards;
}

.animate-slide-in {
    animation: slideInLeft 0.6s ease-out forwards;
}
"""