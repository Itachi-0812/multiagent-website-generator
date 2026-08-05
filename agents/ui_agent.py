from llm_client import ask_gemini


class UIAgent:
    def run(self, task: str, content_data=None, pages=None, website_type="website", user_prompt=""):
        component_name = task.replace("Generate", "").strip()

        prompt = f"""
You are a professional frontend UI component generator.

Website Type:
{website_type}

User Request:
{user_prompt}

Component to Generate:
{component_name}

Website Pages:
{pages}

Content Data:
{content_data}

Generate ONLY the HTML for the component named: {component_name}

Strict rules:
- Return only HTML.
- Use Tailwind CSS utility classes directly inside class attributes.
- Do not generate separate CSS.
- Do not use simple custom class names like hero, navbar, card, menu-section, footer.
- Do not return markdown.
- Do not use ```html.
- Do not generate a full HTML document.
- Do not include <html>, <head>, or <body>.
- Do not generate unrelated components.
- Do not generate navbar/header unless the component is Navbar.
- Do not generate footer unless the component is Footer.
- Do not generate hero section unless the component is Hero.
- If the component is Menu Section, generate restaurant food menu cards only.
- If the component is Reservation Form, generate only a booking/reservation form.
- Use the exact business/website name from Content Data if available.
- Do not add words like "Restaurant Named" before the brand name.
- Use the current year 2026 in footer copyright.
- Use Indian Rupee prices if prices are needed.
- Use semantic HTML tags.
- Use modern responsive layout.
- Use attractive spacing, colors, rounded corners, shadows, hover effects, and responsive grids using Tailwind.
- Do not include JavaScript.
- Do not include CSS.
"""

        try:
            return ask_gemini(prompt)
        except Exception as error:
            print("\nGemini failed or quota exceeded. Using local fallback Tailwind UI.")
            print("Error:", error)

            return self.local_fallback(
                component_name=component_name,
                content_data=content_data,
                pages=pages,
                website_type=website_type
            )

    def local_fallback(self, component_name, content_data=None, pages=None, website_type="website"):
        if content_data is None:
            content_data = {}

        if pages is None:
            pages = ["Home", "Menu", "Reservation", "Contact"]

        name = content_data.get("name", "Sillyvibes")
        role = content_data.get("role", "Delicious Food, Fresh Ingredients, Unforgettable Taste")

        if component_name == "Navbar":
            links = ""
            for page in pages:
                links += f'<li><a class="text-gray-300 hover:text-white transition" href="#{page.lower()}">{page}</a></li>\n'

            return f"""
<nav class="bg-gray-950 text-white border-b border-gray-800 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <h2 class="text-2xl font-bold tracking-tight">{name}</h2>
        <ul class="hidden md:flex items-center gap-8">
            {links}
        </ul>
        <a href="#reservation" class="bg-amber-500 hover:bg-amber-600 text-gray-950 font-semibold px-5 py-2 rounded-full transition">
            Book Table
        </a>
    </div>
</nav>
"""

        elif component_name == "Hero":
            return f"""
<section class="min-h-[85vh] bg-gradient-to-br from-gray-950 via-gray-900 to-amber-950 text-white flex items-center">
    <div class="max-w-6xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-12 items-center">
        <div>
            <p class="text-amber-400 font-semibold mb-4 uppercase tracking-widest">Fresh • Tasty • Authentic</p>
            <h1 class="text-5xl md:text-7xl font-extrabold leading-tight mb-6">Welcome to {name}</h1>
            <p class="text-lg text-gray-300 mb-8 max-w-xl">{role}</p>
            <div class="flex flex-wrap gap-4">
                <a href="#menu" class="bg-amber-500 hover:bg-amber-600 text-gray-950 font-bold px-7 py-3 rounded-full transition">
                    View Menu
                </a>
                <a href="#reservation" class="border border-gray-600 hover:border-amber-400 text-white px-7 py-3 rounded-full transition">
                    Reserve Now
                </a>
            </div>
        </div>

        <div class="bg-white/10 border border-white/10 rounded-3xl p-6 shadow-2xl">
            <div class="aspect-square rounded-2xl bg-gradient-to-br from-amber-400 to-red-700 flex items-center justify-center">
                <p class="text-4xl font-black text-white text-center px-6">Delicious Food</p>
            </div>
        </div>
    </div>
</section>
"""

        elif component_name == "Menu Section":
            return """
<section class="bg-gray-50 py-20 px-6" id="menu">
    <div class="max-w-6xl mx-auto">
        <div class="text-center mb-14">
            <p class="text-amber-600 font-semibold uppercase tracking-widest">Our Specials</p>
            <h2 class="text-4xl md:text-5xl font-extrabold text-gray-950 mt-3">Our Menu</h2>
            <p class="text-gray-600 mt-4">Freshly prepared dishes with rich Indian flavours.</p>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white rounded-2xl p-6 shadow-lg hover:-translate-y-2 transition">
                <h3 class="text-xl font-bold text-gray-950 mb-3">Paneer Tikka</h3>
                <p class="text-gray-600 mb-5">Spicy grilled paneer served with fresh mint chutney.</p>
                <span class="text-2xl font-extrabold text-amber-600">₹249</span>
            </div>

            <div class="bg-white rounded-2xl p-6 shadow-lg hover:-translate-y-2 transition">
                <h3 class="text-xl font-bold text-gray-950 mb-3">Butter Naan & Curry</h3>
                <p class="text-gray-600 mb-5">Fresh naan served with rich creamy curry.</p>
                <span class="text-2xl font-extrabold text-amber-600">₹199</span>
            </div>

            <div class="bg-white rounded-2xl p-6 shadow-lg hover:-translate-y-2 transition">
                <h3 class="text-xl font-bold text-gray-950 mb-3">Veg Biryani</h3>
                <p class="text-gray-600 mb-5">Flavourful rice cooked with vegetables and Indian spices.</p>
                <span class="text-2xl font-extrabold text-amber-600">₹299</span>
            </div>

            <div class="bg-white rounded-2xl p-6 shadow-lg hover:-translate-y-2 transition">
                <h3 class="text-xl font-bold text-gray-950 mb-3">Chocolate Brownie</h3>
                <p class="text-gray-600 mb-5">Warm brownie served with vanilla ice cream.</p>
                <span class="text-2xl font-extrabold text-amber-600">₹149</span>
            </div>
        </div>
    </div>
</section>
"""

        elif component_name == "Reservation Form":
            return """
<section class="bg-gray-950 text-white py-20 px-6" id="reservation">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-12">
            <p class="text-amber-400 font-semibold uppercase tracking-widest">Book Now</p>
            <h2 class="text-4xl md:text-5xl font-extrabold mt-3">Book a Table</h2>
            <p class="text-gray-400 mt-4">Reserve your table and enjoy a memorable dining experience.</p>
        </div>

        <form class="bg-gray-900 border border-gray-800 rounded-3xl p-8 grid md:grid-cols-2 gap-5 shadow-2xl">
            <input class="bg-gray-950 border border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-amber-400" type="text" placeholder="Full Name" required>
            <input class="bg-gray-950 border border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-amber-400" type="email" placeholder="Email Address" required>
            <input class="bg-gray-950 border border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-amber-400" type="tel" placeholder="Phone Number" required>
            <input class="bg-gray-950 border border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-amber-400" type="date" required>
            <input class="bg-gray-950 border border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-amber-400" type="time" required>
            <input class="bg-gray-950 border border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-amber-400" type="number" placeholder="Number of Guests" min="1" required>
            <textarea class="md:col-span-2 bg-gray-950 border border-gray-700 rounded-xl px-4 py-3 outline-none focus:border-amber-400" placeholder="Special Request"></textarea>
            <button class="md:col-span-2 bg-amber-500 hover:bg-amber-600 text-gray-950 font-bold py-3 rounded-xl transition" type="submit">
                Confirm Reservation
            </button>
        </form>
    </div>
</section>
"""

        elif component_name == "Footer":
            return f"""
<footer class="bg-black text-white py-10 px-6">
    <div class="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div>
            <h3 class="text-2xl font-bold">{name}</h3>
            <p class="text-gray-400 mt-1">{role}</p>
        </div>
        <p class="text-gray-500">© 2026 {name}. All rights reserved.</p>
    </div>
</footer>
"""

        elif component_name == "Projects Grid":
            return """
<section class="bg-gray-50 py-20 px-6">
    <div class="max-w-6xl mx-auto">
        <h2 class="text-4xl font-extrabold text-gray-950 mb-8">Projects</h2>
        <div class="grid md:grid-cols-3 gap-6">
            <div class="bg-white rounded-2xl p-6 shadow-lg">
                <h3 class="text-xl font-bold text-gray-950">Sample Project</h3>
                <p class="text-gray-600 mt-3">A beautiful project generated by the multiagent system.</p>
            </div>
        </div>
    </div>
</section>
"""

        elif component_name == "Article Grid":
            return """
<section class="bg-white py-20 px-6">
    <div class="max-w-6xl mx-auto">
        <h2 class="text-4xl font-extrabold text-gray-950 mb-8">Latest Articles</h2>
        <div class="grid md:grid-cols-3 gap-6">
            <article class="bg-gray-50 rounded-2xl p-6 shadow">
                <h3 class="text-xl font-bold text-gray-950">How AI is Changing Web Development</h3>
                <p class="text-gray-600 mt-3">A quick article about AI-powered website generation.</p>
            </article>
        </div>
    </div>
</section>
"""

        elif component_name == "Features":
            return """
<section class="bg-gray-950 text-white py-20 px-6">
    <div class="max-w-6xl mx-auto">
        <h2 class="text-4xl font-extrabold mb-8">Features</h2>
        <div class="grid md:grid-cols-3 gap-6">
            <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6">
                <h3 class="text-xl font-bold">Fast</h3>
                <p class="text-gray-400 mt-3">Generate websites quickly using AI agents.</p>
            </div>
        </div>
    </div>
</section>
"""

        elif component_name == "Pricing":
            return """
<section class="bg-gray-50 py-20 px-6">
    <div class="max-w-6xl mx-auto">
        <h2 class="text-4xl font-extrabold text-gray-950 mb-8">Pricing</h2>
        <div class="bg-white rounded-2xl p-8 shadow-lg max-w-sm">
            <h3 class="text-2xl font-bold text-gray-950">Starter</h3>
            <p class="text-4xl font-extrabold text-amber-600 mt-4">₹499/month</p>
        </div>
    </div>
</section>
"""

        elif component_name == "Product Grid":
            return """
<section class="bg-white py-20 px-6">
    <div class="max-w-6xl mx-auto">
        <h2 class="text-4xl font-extrabold text-gray-950 mb-8">Products</h2>
        <div class="grid md:grid-cols-3 gap-6">
            <div class="bg-gray-50 rounded-2xl p-6 shadow">
                <h3 class="text-xl font-bold text-gray-950">Sample Product</h3>
                <p class="text-amber-600 font-extrabold text-2xl mt-3">₹999</p>
                <button class="mt-5 bg-gray-950 text-white px-5 py-2 rounded-full">Add to Cart</button>
            </div>
        </div>
    </div>
</section>
"""

        elif component_name == "Cart":
            return """
<section class="bg-gray-50 py-20 px-6">
    <div class="max-w-4xl mx-auto bg-white rounded-3xl p-8 shadow-lg">
        <h2 class="text-4xl font-extrabold text-gray-950">Your Cart</h2>
        <p class="text-gray-600 mt-4">Your selected products will appear here.</p>
        <button class="mt-6 bg-gray-950 text-white px-6 py-3 rounded-full">Checkout</button>
    </div>
</section>
"""

        elif component_name == "Checkout":
            return """
<section class="bg-white py-20 px-6">
    <div class="max-w-4xl mx-auto bg-gray-50 rounded-3xl p-8 shadow">
        <h2 class="text-4xl font-extrabold text-gray-950">Checkout</h2>
        <p class="text-gray-600 mt-4">Enter your delivery and payment details.</p>
        <button class="mt-6 bg-amber-500 text-gray-950 font-bold px-6 py-3 rounded-full">Place Order</button>
    </div>
</section>
"""

        return ""