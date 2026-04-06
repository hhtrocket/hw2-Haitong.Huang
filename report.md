# Report — Meeting Notes to Action Items
**Author:** Haitong Huang
**Date:** April 5, 2026

---

## 1. Business Use Case

Every team meeting produces a list of commitments, decisions, and follow-up items buried inside raw, informal notes. Turning those notes into a clean action item list is a repetitive, low-skill task that nonetheless takes time and is often done inconsistently — or skipped entirely. The result is missed deadlines, duplicated work, and accountability gaps.

This prototype automates that step. The user pastes or provides raw meeting notes; the system returns a structured output with three sections: a one-sentence meeting summary, a confirmed action item list (with owner and deadline), and a "Needs Follow-Up" list for unresolved topics. The target user is a project manager, team lead, or meeting organizer who runs recurring meetings and needs to distribute next steps quickly and reliably.

The task is valuable to automate because the input-output pattern is highly regular, the cost of a missed action item is real, and even an imperfect draft that the organizer reviews and edits in 30 seconds is faster than writing from scratch.

---

## 2. Model Choice

**Primary model used:** `gemini-2.0-flash` via Google AI Studio API.

Gemini 2.0 Flash was selected for three reasons: it is freely accessible through the Google AI Studio API without a billing requirement, it has a fast response time suitable for a command-line prototype, and it follows structured formatting instructions reliably across varied input lengths.

No other models were formally benchmarked in this prototype, but based on general familiarity, GPT-4o (OpenAI) would likely produce comparable or slightly more consistent formatting on edge cases, at higher cost. Gemini 1.5 Pro was considered but is slower and unnecessary for a task of this complexity.

---

## 3. Baseline vs. Final Design: Prompt Iteration

### Baseline (Initial Prompt)

The initial system prompt instructed the model to extract a single flat list of confirmed action items, and to return `"No confirmed action items found. Human review recommended."` for any vague input.

**Observed problems on the eval set:**
- **Case 4** (scattered all-hands notes): the model returned the rejection message, discarding several potentially useful topics (e.g., updating onboarding docs, HR benefits follow-up) simply because no single owner was named.
- **Case 5** (vague post-demo chat): the model sometimes extracted items like "John will look into caching" — treating hedging language ("kind of mentioned he might") as a firm commitment, a clear hallucination risk.
- Cases 1 and 2 performed well with clean, structured output.

### Revision 1 — Two-Section Output

Added a `### Needs Follow-Up` section. The model was explicitly instructed to route items with uncertain language into this section rather than either promoting them to Action Items or discarding them.

**Improvement:** Case 4 and Case 5 now produced useful output — ambiguous topics surfaced with a status note instead of being silently dropped. The hallucination risk in Case 5 was reduced because the model had a legitimate place to put uncertain items without fabricating a commitment.

### Revision 2 — Three-Section Output with Mandatory Headers (Final)

Added a `### Meeting Summary` line at the top and made all three section headers mandatory in every response.

**Improvement:** Output became consistently scannable — a reader can open `output.txt` and immediately understand meeting context before reading tasks. Mandatory headers also made the structure predictable across all five eval cases, which matters for any downstream parsing or formatting. No degradation was observed on the normal cases.

### Summary Table

| Dimension | Initial Prompt | Final Prompt (Rev 2) |
|-----------|---------------|----------------------|
| Normal cases (1 & 2) | Correct, clean | Correct, clean + summary |
| Edge case — short notes (3) | Correct | Correct |
| Edge case — no owners (4) | Discarded useful topics | Surfaced in Needs Follow-Up |
| High-risk — vague language (5) | Occasional hallucination | Routed to Needs Follow-Up |
| Output consistency | Variable | Uniform 3-section structure |

---

## 4. Where the Prototype Still Fails or Requires Human Review

The prototype has three remaining failure modes that require human oversight before any output is acted upon.

First, it cannot detect contradictions. If meeting notes contain conflicting statements — for example, two people claiming ownership of the same task — the model will silently pick one rather than flag the conflict.

Second, it relies entirely on explicit language. Implicit commitments ("I'll handle it", said in response to a question about who owns the API work) may or may not be captured depending on how the note-taker recorded the exchange.

Third, the model has no memory across meetings. It cannot tell whether an action item from this week was already assigned last week, making duplicate tracking invisible to the system.

For all these reasons, the output should be treated as a first draft reviewed by the meeting organizer before distribution — not as a final, authoritative record.

---

## 5. Deployment Recommendation

**Conditional recommendation: deploy as a draft-assistance tool, not as an autonomous system.**

The prototype reliably handles well-structured meeting notes and provides substantial time savings for normal cases. However, given the hallucination risk on vague inputs and the inability to detect contradictions or implicit commitments, it should not send action items directly to team members without a human review step.

The recommended deployment pattern is: (1) the model generates the structured output immediately after a meeting, (2) the meeting organizer reviews and edits the draft in under a minute, and (3) the organizer sends the approved version. This preserves the speed benefit while keeping a human accountable for accuracy. Deployment without a review gate would be appropriate only for teams with highly disciplined, structured note-taking practices where vague or implicit language rarely appears.
