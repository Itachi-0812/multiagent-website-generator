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
        color_scheme = self._get_color_scheme(website_type)

        return f"""
/* Tailwind-Compatible Responsive CSS */
:root {{
    --primary: {color_scheme['primary']};
    --primary-dark: {color_scheme['primary_dark']};
    --secondary: {color_scheme['secondary']};
    --accent: {color_scheme['accent']};
    --text-900: #111827;
    --text-700: #374151;
    --text-600: #4b5563;
    --text-500: #6b7280;
    --text-400: #9ca3af;
    --bg-50: #f9fafb;
    --bg-100: #f3f4f6;
    --bg-50-rgb: 249, 250, 251;
    --white: #ffffff;
    --border: #e5e7eb;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-700);
    background-color: var(--white);
    overflow-x: hidden;
}}

/* Typography */
h1 {{
    font-size: clamp(1.875rem, 5vw, 3.75rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
    color: var(--text-900);
}}

h2 {{
    font-size: clamp(1.5rem, 4vw, 2.25rem);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1.25rem;
    color: var(--text-900);
}}

h3 {{
    font-size: clamp(1.25rem, 3vw, 1.875rem);
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 1rem;
    color: var(--text-900);
}}

h4 {{
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    color: var(--text-900);
}}

h5, h6 {{
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-900);
}}

p {{
    margin-bottom: 1rem;
    color: var(--text-600);
    line-height: 1.75;
}}

strong {{
    color: var(--text-900);
    font-weight: 600;
}}

/* Links */
a {{
    color: var(--primary);
    text-decoration: none;
    transition: color 0.2s ease;
}}

a:hover {{
    color: var(--primary-dark);
}}

a:focus {{
    outline: 2px solid var(--primary);
    outline-offset: 2px;
}}

/* Buttons */
button, [type="submit"], [type="button"], .btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 1.5rem;
    background-color: var(--primary);
    color: white;
    border: 2px solid var(--primary);
    border-radius: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
    gap: 0.5rem;
}}

button:hover, [type="submit"]:hover, [type="button"]:hover, .btn:hover {{
    background-color: var(--primary-dark);
    border-color: var(--primary-dark);
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}}

button:active, [type="submit"]:active {{
    transform: translateY(0);
}}

button:disabled {{
    opacity: 0.5;
    cursor: not-allowed;
}}

button.btn-secondary {{
    background-color: var(--bg-100);
    color: var(--text-900);
    border-color: var(--border);
}}

button.btn-secondary:hover {{
    background-color: var(--bg-50);
    border-color: var(--primary);
}}

/* Forms */
input, textarea, select {{
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    background-color: var(--white);
    color: var(--text-900);
    transition: var(--transition);
    font-family: inherit;
}}

input:focus, textarea:focus, select:focus {{
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}}

textarea {{
    resize: vertical;
}}

label {{
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--text-900);
}}

/* Layout */
.container {{
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 1.5rem;
}}

section {{
    padding: 3rem 0;
}}

section.hero {{
    padding: 5rem 0 3rem;
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.05) 0%, rgba(79, 70, 229, 0.05) 100%);
}}

/* Grid & Flexbox */
.grid {{
    display: grid;
    gap: 2rem;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}}

.grid-2 {{
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}}

.grid-3 {{
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}}

.flex {{
    display: flex;
    gap: 1rem;
}}

.flex-col {{
    flex-direction: column;
}}

.flex-center {{
    justify-content: center;
    align-items: center;
}}

.flex-between {{
    justify-content: space-between;
    align-items: center;
}}

.gap-1 {{ gap: 0.25rem; }}
.gap-2 {{ gap: 0.5rem; }}
.gap-3 {{ gap: 0.75rem; }}
.gap-4 {{ gap: 1rem; }}
.gap-6 {{ gap: 1.5rem; }}
.gap-8 {{ gap: 2rem; }}

/* Cards */
.card {{
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 1.5rem;
    transition: var(--transition);
    box-shadow: var(--shadow-sm);
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary);
}}

.card-header {{
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}}

.card-body {{
    margin-bottom: 1rem;
}}

.card-footer {{
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}}

/* Navbar */
nav {{
    background: var(--white);
    border-bottom: 1px solid var(--border);
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 50;
    box-shadow: var(--shadow-sm);
}}

nav .container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

nav a {{
    color: var(--text-700);
    font-weight: 500;
    margin: 0 1rem;
    transition: color 0.2s;
}}

nav a:hover {{
    color: var(--primary);
}}

/* Features/Services Grid */
.feature-grid {{
    display: grid;
    gap: 2rem;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    margin-top: 2rem;
}}

.feature-card {{
    text-align: center;
    padding: 2rem;
}}

.feature-icon {{
    width: 3rem;
    height: 3rem;
    background: rgba(37, 99, 235, 0.1);
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    font-size: 1.5rem;
}}

/* Animations */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes slideInUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes slideInLeft {{
    from {{ opacity: 0; transform: translateX(-30px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

@keyframes slideInRight {{
    from {{ opacity: 0; transform: translateX(30px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.5; }}
}}

.animate-fade-in {{
    animation: fadeIn 0.6s ease-out forwards;
}}

.animate-slide-up {{
    animation: slideInUp 0.6s ease-out forwards;
}}

.animate-pulse {{
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}}

/* Utilities */
.text-center {{ text-align: center; }}
.text-left {{ text-align: left; }}
.text-right {{ text-align: right; }}

.mt-1 {{ margin-top: 0.25rem; }}
.mt-2 {{ margin-top: 0.5rem; }}
.mt-4 {{ margin-top: 1rem; }}
.mt-6 {{ margin-top: 1.5rem; }}
.mt-8 {{ margin-top: 2rem; }}

.mb-1 {{ margin-bottom: 0.25rem; }}
.mb-2 {{ margin-bottom: 0.5rem; }}
.mb-4 {{ margin-bottom: 1rem; }}
.mb-6 {{ margin-bottom: 1.5rem; }}
.mb-8 {{ margin-bottom: 2rem; }}

.px-2 {{ padding-left: 0.5rem; padding-right: 0.5rem; }}
.px-4 {{ padding-left: 1rem; padding-right: 1rem; }}
.px-6 {{ padding-left: 1.5rem; padding-right: 1.5rem; }}

.py-2 {{ padding-top: 0.5rem; padding-bottom: 0.5rem; }}
.py-4 {{ padding-top: 1rem; padding-bottom: 1rem; }}
.py-6 {{ padding-top: 1.5rem; padding-bottom: 1.5rem; }}

.rounded {{ border-radius: 0.375rem; }}
.rounded-lg {{ border-radius: 0.5rem; }}
.rounded-xl {{ border-radius: 0.75rem; }}
.rounded-full {{ border-radius: 9999px; }}

.shadow {{ box-shadow: var(--shadow-sm); }}
.shadow-md {{ box-shadow: var(--shadow-md); }}
.shadow-lg {{ box-shadow: var(--shadow-lg); }}
.shadow-xl {{ box-shadow: var(--shadow-xl); }}

.opacity-75 {{ opacity: 0.75; }}
.opacity-50 {{ opacity: 0.5; }}

/* Responsive */
@media (max-width: 1024px) {{
    section {{
        padding: 2.5rem 0;
    }}

    h1 {{ font-size: 2.25rem; }}
    h2 {{ font-size: 1.875rem; }}
    h3 {{ font-size: 1.5rem; }}
}}

@media (max-width: 768px) {{
    .container {{
        padding: 0 1rem;
    }}

    section {{
        padding: 2rem 0;
    }}

    section.hero {{
        padding: 3rem 0 2rem;
    }}

    h1 {{ font-size: 1.875rem; }}
    h2 {{ font-size: 1.5rem; }}
    h3 {{ font-size: 1.25rem; }}

    .grid, .grid-2, .grid-3 {{
        grid-template-columns: 1fr;
    }}

    .flex {{
        flex-direction: column;
    }}

    nav .container {{
        flex-direction: column;
        gap: 1rem;
    }}

    nav a {{
        margin: 0.25rem 0;
    }}
}}

@media (max-width: 480px) {{
    .container {{
        padding: 0 0.75rem;
    }}

    h1 {{ font-size: 1.5rem; }}
    h2 {{ font-size: 1.25rem; }}
    h3 {{ font-size: 1.125rem; }}

    button, .btn {{
        width: 100%;
    }}

    .grid {{
        gap: 1rem;
    }}
}}
"""

    def _get_color_scheme(self, website_type):
        schemes = {{
            "portfolio": {{
                "primary": "#2563eb",
                "primary_dark": "#1d4ed8",
                "secondary": "#1e40af",
                "accent": "#3b82f6"
            }},
            "restaurant": {{
                "primary": "#dc2626",
                "primary_dark": "#b91c1c",
                "secondary": "#991b1b",
                "accent": "#f87171"
            }},
            "business": {{
                "primary": "#0369a1",
                "primary_dark": "#0c4a6e",
                "secondary": "#1e40af",
                "accent": "#06b6d4"
            }},
            "blog": {{
                "primary": "#7c3aed",
                "primary_dark": "#6d28d9",
                "secondary": "#5b21b6",
                "accent": "#a78bfa"
            }},
            "saas": {{
                "primary": "#2563eb",
                "primary_dark": "#1d4ed8",
                "secondary": "#1e40af",
                "accent": "#60a5fa"
            }},
            "ecommerce": {{
                "primary": "#db2777",
                "primary_dark": "#be185d",
                "secondary": "#9d174d",
                "accent": "#ec4899"
            }},
            "generic": {{
                "primary": "#3b82f6",
                "primary_dark": "#1d4ed8",
                "secondary": "#1e40af",
                "accent": "#60a5fa"
            }}
        }}

        return schemes.get(website_type, schemes["generic"])