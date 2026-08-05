"use client";

import { useState } from "react";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function generateWebsite() {
    if (!prompt.trim()) {
      setError("Please enter a website prompt first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/generate-website", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
        }),
      });

      if (!response.ok) {
        throw new Error("Backend request failed.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Could not connect to backend. Make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  }

  function copyToClipboard(text, type) {
    navigator.clipboard.writeText(text);
    alert(`${type} copied successfully!`);
  }

  function clearResult() {
    setPrompt("");
    setResult(null);
    setError("");
  }

  const previewContent = result
  ? `
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>${result.css || ""}</style>
      </head>
      <body>
        ${result.html}
      </body>
    </html>
  `
  : "";

  return (
    <main className="min-h-screen bg-gray-950 text-white px-6 py-10">
      <section className="max-w-6xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Multiagent Website Generator
          </h1>
          <p className="text-gray-400 text-lg">
            Enter a website idea and generate a complete UI using your multiagent backend.
          </p>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-xl mb-8">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Describe your website
          </label>

          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Example: Create a modern restaurant website with hero section, menu, about, gallery and contact form"
            className="w-full h-36 p-4 rounded-xl bg-gray-950 border border-gray-700 text-white outline-none focus:border-blue-500 resize-none"
          />

          {error && <p className="text-red-400 mt-3">{error}</p>}

          <button
            onClick={generateWebsite}
            disabled={loading}
            className="mt-5 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 font-semibold transition"
          >
            {loading ? "Generating..." : "Generate Website"}
          </button>
        </div>

        {result && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <section className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold">Generated Details</h2>

                <button
                  onClick={clearResult}
                  className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-700 text-sm font-semibold"
                >
                  Clear
                </button>
              </div>

              <div className="mb-5">
                <p className="text-gray-400 text-sm">Website Type</p>
                <p className="text-lg font-semibold">{result.website_type}</p>
              </div>

              <div className="mb-5">
                <p className="text-gray-400 text-sm">Sections</p>
                <div className="flex flex-wrap gap-2 mt-2">
                  {result.sections.map((section, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 rounded-full bg-blue-600/20 text-blue-300 text-sm"
                    >
                      {section}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mb-5">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-gray-400 text-sm">Generated HTML</p>

                  <button
                    onClick={() => copyToClipboard(result.html, "HTML")}
                    className="px-3 py-1 rounded-lg bg-gray-800 hover:bg-gray-700 text-xs font-semibold"
                  >
                    Copy HTML
                  </button>
                </div>

                <pre className="bg-gray-950 border border-gray-800 p-4 rounded-xl overflow-auto text-sm max-h-64">
                  {result.html}
                </pre>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <p className="text-gray-400 text-sm">Generated CSS</p>

                  <button
                    onClick={() => copyToClipboard(result.css, "CSS")}
                    className="px-3 py-1 rounded-lg bg-gray-800 hover:bg-gray-700 text-xs font-semibold"
                  >
                    Copy CSS
                  </button>
                </div>

                <pre className="bg-gray-950 border border-gray-800 p-4 rounded-xl overflow-auto text-sm max-h-64">
                  {result.css}
                </pre>
              </div>
            </section>

            <section className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
              <h2 className="text-2xl font-bold mb-4">Live Preview</h2>

              <iframe
                title="Generated Website Preview"
                srcDoc={previewContent}
                className="w-full h-[650px] bg-white rounded-xl border border-gray-700"
              />
            </section>
          </div>
        )}
      </section>
    </main>
  );
}