import os
import sys
import webbrowser

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from core.site_generator import generate_site


def main():
    user_prompt = input("Describe your website: ")
    generate_backend = input("Generate backend with database, auth, forms? (yes/no): ").lower() == "yes"

    result = generate_site(
        prompt=user_prompt,
        use_ai=True,
        save_files=True,
        generate_backend=generate_backend
    )

    print("\n===== WEBSITE GENERATED =====")
    print(f"Website Type: {result['website_type']}")
    print(f"Sections: {', '.join(result['sections'])}")
    print(f"\nWebsite saved at: {result['html_path']}")
    print(f"CSS saved at: {result['css_path']}")

    if generate_backend:
        print(f"\nBackend generated at: {result['backend_path']}")
        print("\nTo run the backend:")
        print("  python run_generated_backend.py")
        print("\nBackend features:")
        print("  - User authentication (JWT)")
        print("  - Form submission handling")
        print("  - Content management system")
        print("  - Admin dashboard")
        print("  - SQLAlchemy database models")

    html_path = os.path.abspath(result["html_path"])
    css_path = os.path.abspath(result["css_path"])

    with open(html_path, "r", encoding="utf-8") as file:
        generated_html = file.read()

    with open(css_path, "r", encoding="utf-8") as file:
        generated_css = file.read()

    preview_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Website Preview</title>

    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f4f4;
        }}

        .preview-toolbar {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background: #111827;
            color: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            z-index: 9999;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}

        .preview-toolbar h2 {{
            margin: 0;
            font-size: 18px;
        }}

        .fullscreen-btn {{
            background: #2563eb;
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
        }}

        .fullscreen-btn:hover {{
            background: #1d4ed8;
        }}

        #previewArea {{
            margin-top: 60px;
            min-height: calc(100vh - 60px);
            background: white;
            overflow: auto;
        }}

        #previewArea:fullscreen {{
            margin-top: 0;
            width: 100vw;
            height: 100vh;
            overflow: auto;
            background: white;
        }}

        {generated_css}
    </style>
</head>

<body>

    <div class="preview-toolbar">
        <h2>Generated Website Preview</h2>

        <button class="fullscreen-btn" onclick="openFullScreen()">
            Full Screen Preview
        </button>
    </div>

    <div id="previewArea">
        {generated_html}
    </div>

    <script>
        function openFullScreen() {{
            const preview = document.getElementById("previewArea");

            if (preview.requestFullscreen) {{
                preview.requestFullscreen();
            }} else if (preview.webkitRequestFullscreen) {{
                preview.webkitRequestFullscreen();
            }} else if (preview.msRequestFullscreen) {{
                preview.msRequestFullscreen();
            }}
        }}
    </script>

</body>
</html>
"""

    preview_path = os.path.join(PROJECT_ROOT, "output", "preview.html")

    with open(preview_path, "w", encoding="utf-8") as file:
        file.write(preview_html)

    print(f"\nPreview saved at: {preview_path}")

    webbrowser.open(os.path.abspath(preview_path))


if __name__ == "__main__":
    main()
