
"""
Meeting Notes to Action Items — Initial Version (v0)
This file records the original prompt before any revisions.
Usage:
  python app_v0_initial.py                        # runs all eval cases
  python app_v0_initial.py --notes "your notes"   # run a single custom input
"""

import argparse
import google.generativeai as genai

# ── Configuration ────────────────────────────────────────────────────────────

API_KEY = "AIzaSyBR4U4Tr5Sqr0vW7W8_tqdQzC7a3KA4xLM"
MODEL   = "gemini-2.0-flash"

SYSTEM_PROMPT = """
You are a professional meeting assistant. Your job is to read raw meeting notes
and extract a clean, structured action item list.

For each action item, output exactly this format:
- [ ] Task: <what needs to be done>
  Owner: <person responsible, or "Unassigned" if not mentioned>
  Due: <deadline, or "Not specified" if not mentioned>

Rules:
- Only include items that represent a clear, committed action.
- Do NOT invent owners or deadlines that are not stated.
- If the notes contain only vague or uncertain language, say:
  "No confirmed action items found. Human review recommended."
- Do not add commentary outside the action item list.
"""

# ── Eval cases ───────────────────────────────────────────────────────────────

EVAL_CASES = [
    {
        "id": "Case 1 — Normal (Weekly Standup)",
        "notes": (
            "Weekly team sync — April 5, 2026\n"
            "Attendees: Sarah (PM), James (Dev), Lisa (Design)\n\n"
            "Sarah mentioned that the login page redesign needs to be finalized by April 10. "
            "Lisa will handle the mockups. James will review the API integration by April 8 "
            "and flag any blockers. Sarah will send the updated project timeline to the client "
            "by end of day Friday."
        ),
    },
    {
        "id": "Case 2 — Normal (Product Review)",
        "notes": (
            "Product review meeting — April 3, 2026\n"
            "Attendees: Tom (CPO), Anna (Dev Lead), Kevin (QA)\n\n"
            "The team agreed to delay the v2.0 launch by one week to allow more QA time. "
            "Kevin will prepare a full regression test report by April 9. Anna needs to fix "
            "the checkout bug before April 7. Tom will update the roadmap slide deck and share "
            "it with stakeholders before the board meeting on April 12."
        ),
    },
    {
        "id": "Case 3 — Edge (Very Short Notes)",
        "notes": (
            "Quick sync April 4.\n"
            "Jake will look into the server issue.\n"
            "Follow up next week."
        ),
    },
    {
        "id": "Case 4 — Edge (Scattered, No Owners)",
        "notes": (
            "All-hands meeting — April 2, 2026\n\n"
            "We talked about a lot of things. Marketing said they want a new campaign but "
            "didn't say who would lead it. Engineering brought up technical debt but nobody "
            "committed to anything specific. Someone mentioned updating the onboarding docs. "
            "HR said they are looking into the new benefits policy. Finance gave a quarterly "
            "update. There were some concerns about the Q2 budget but no decisions were made."
        ),
    },
    {
        "id": "Case 5 — High-Risk (Vague Commitments)",
        "notes": (
            "Informal chat after the sprint demo — April 1, 2026\n\n"
            "We probably should do something about the dashboard performance at some point. "
            "John kind of mentioned he might look into caching but wasn't sure. Someone said "
            "maybe we could revisit the UI next quarter. There was some discussion about "
            "whether to migrate to a new database but no one really agreed on anything."
        ),
    },
]

# ── Core function ─────────────────────────────────────────────────────────────

def extract_action_items(notes: str) -> str:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=SYSTEM_PROMPT,
    )
    response = model.generate_content(notes)
    return response.text.strip()

# ── CLI entry point ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Meeting Notes → Action Items (Initial Version)")
    parser.add_argument("--notes", type=str, default=None,
                        help="Meeting notes as a string. If omitted, runs all eval cases.")
    args = parser.parse_args()

    output_lines = []

    if args.notes:
        cases = [{"id": "Custom Input", "notes": args.notes}]
    else:
        cases = EVAL_CASES

    for case in cases:
        header = f"{'='*60}\n{case['id']}\n{'='*60}"
        print(header)
        output_lines.append(header)

        print("INPUT:")
        print(case["notes"])
        output_lines.append("INPUT:\n" + case["notes"])

        print("\nOUTPUT:")
        result = extract_action_items(case["notes"])
        print(result)
        output_lines.append("\nOUTPUT:\n" + result)

        separator = "\n"
        print(separator)
        output_lines.append(separator)

    output_path = "output_v0.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    main()
