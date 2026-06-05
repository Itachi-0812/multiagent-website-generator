class ReadmeAgent:
    def run(self, plan):
        pages = "\n".join([f"- {page}" for page in plan.pages])
        components = "\n".join([f"- {component}" for component in plan.components])

        return f"""
# Generated {plan.website_type.title()} Website

## User Prompt

{plan.user_prompt}

## Website Type

{plan.website_type}

## Pages Generated

{pages}

## Components Generated

{components}

## Agents Used

- Planner Agent
- Content Agent
- UI Agent
- Style Agent
- README Agent

## Output Files

- `index.html`
- `styles.css`
- `README.md`

## How to Run

Open `index.html` in any browser.

## Project Description

This website was generated using a multi-agent system. The Planner Agent created the website structure, the Content Agent prepared content data, the UI Agent generated HTML components, and the Style Agent generated CSS styling.
"""