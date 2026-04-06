# Evaluation Set — Meeting Notes to Action Items

---

### Case 1 — Normal Case (Standard Weekly Standup)

**Input:**
> Weekly team sync — April 5, 2026
> Attendees: Sarah (PM), James (Dev), Lisa (Design)
>
> Sarah mentioned that the login page redesign needs to be finalized by April 10. Lisa will handle the mockups. James will review the API integration by April 8 and flag any blockers. Sarah will send the updated project timeline to the client by end of day Friday.

**Expected output should:**
Extract three clearly defined action items with correct owners (Lisa, James, Sarah) and deadlines. Output should be structured and ready to share with no extra commentary.

---

### Case 2 — Normal Case (Product Review Meeting)

**Input:**
> Product review meeting — April 3, 2026
> Attendees: Tom (CPO), Anna (Dev Lead), Kevin (QA)
>
> The team agreed to delay the v2.0 launch by one week to allow more QA time. Kevin will prepare a full regression test report by April 9. Anna needs to fix the checkout bug before April 7. Tom will update the roadmap slide deck and share it with stakeholders before the next board meeting on April 12.

**Expected output should:**
Identify three action items with clear owners and deadlines. Also note the launch delay decision as context. Should not confuse decisions with tasks.

---

### Case 3 — Edge Case (Very Short Notes)

**Input:**
> Quick sync April 4.
> Jake will look into the server issue.
> Follow up next week.

**Expected output should:**
Extract one action item (Jake — investigate server issue). Recognize that the deadline is vague ("next week") and either note it as unconfirmed or leave it blank rather than inventing a specific date.

---

### Case 4 — Edge Case (Long and Scattered Notes, No Named Owners)

**Input:**
> All-hands meeting — April 2, 2026
> We talked about a lot of things. Marketing said they want a new campaign but didn't say who would lead it. Engineering brought up technical debt but nobody committed to anything specific. Someone mentioned updating the onboarding docs. HR said they are looking into the new benefits policy. Finance gave a quarterly update. There were some concerns about the Q2 budget but no decisions were made. The meeting ran over by 20 minutes.

**Expected output should:**
Identify only clearly actionable items (e.g., update onboarding docs, HR follow up on benefits policy). Must not fabricate owners for tasks where no one was named. Should flag that several topics require follow-up or owner assignment.

---

### Case 5 — High-Risk Case (Vague Commitments, Likely to Hallucinate)

**Input:**
> Informal chat after the sprint demo — April 1, 2026
> We probably should do something about the dashboard performance at some point. John kind of mentioned he might look into caching but wasn't sure. Someone said maybe we could revisit the UI next quarter. There was some discussion about whether to migrate to a new database but no one really agreed on anything. It would be nice to have a decision by end of month, maybe.

**Expected output should:**
Recognize that no firm commitments were made. Should not convert uncertain language ("probably," "might," "kind of," "maybe") into definitive action items. A good output either returns a minimal list with strong uncertainty flags, or explicitly states that no actionable items were confirmed and human review is required.

