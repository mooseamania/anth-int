# Applied AI Architect: prep guide

Two separate interviews, both screen-share: (A) the FinTechCo Claude Code presentation, 40 min of a 50-min slot, and (B) the Customer Solutioning interview, where you tell a real engagement story. Part A is built out below. Part B is a framework at the end, because it needs your story.

**What I could and couldn't do:** I read the instructions and the text of the template deck, but I can't open or edit your Google Slides. The slide copy below is written to paste into your copy of the template. Keep its layout and fonts, and reuse its Ramp and Fortune 500 case slides as-is.

---

## 1. The point of view (say this in the first 60 seconds)

> "You asked three things: how it works, why it's worth it, and how to evaluate it. I'll answer each, show it working on something that looks like your world, and leave you with a pilot you could start in two weeks, with measures you can defend to your board."

Your audience, and what each needs to hear:

| Who | Worry | What wins them |
|---|---|---|
| CTO (security, compliance, skeptic) | Unproven, data leaving, audit | Runs in your cloud (Bedrock / Vertex), permissions you control, nothing changes without approval, a pilot with stop criteria, named enterprise references |
| Head of Digital Transformation (champion) | Proving it to others, adoption | Measurement framework, a quick visible win, a rollout playbook |

Both of them: "What does it cost me, what do I get, how do I know?"

## 2. Run of show (40 min)

| Min | Segment | Notes |
|---|---|---|
| 0-2 | Frame + agenda | State the three questions back to them |
| 2-9 | How it works + why Claude Code | Slides 2-5 |
| 9-12 | Fit for your three teams | Slide 6 |
| 12-24 | **Live demo** | Section 5. Hard stop at 24:00 |
| 24-30 | Measuring impact + ROI | Slides 7-8. Bridge from the demo's business view |
| 30-35 | Evaluation + rollout plan | Slides 9-10 |
| 35-38 | Next steps + ask | Slide 11 |
| 38-40 | Buffer / questions | If you are behind at minute 30, cut slide 5 and the second half of the demo recap, never the plan |

Say your timing out loud once ("I'll keep us to time, and we'll finish with a plan"). It signals you run real meetings.

## 3. Slide-by-slide (11 slides, paste into the template)

**1. Title**: *Claude Code at FinTechCo: how it works, why it pays off, how to prove it.*

**2. What Claude Code is**: Agentic tool that works in your terminal, IDE or GitHub. You delegate multi-step work; it reads code, edits files, runs tests and commands. Transparent: it shows its work and asks approval before changes. (Adapt template slides "Introducing" and "Optimized for Claude".)

**3. Built for regulated enterprises** *(this is your CTO slide, give it room)*
- Deploy through your own cloud: Amazon Bedrock or Google Vertex AI, as well as Anthropic API. You already run AWS and GCP, so no new vendor path for data.
- Centrally managed permissions and corporate proxy support; per-project allow/deny rules for commands and files.
- Queries go to the model via API; no separate code index held by an intermediary (from the template).
- Human approval for changes by default; every action is visible.
- **Verify before the interview** and cite exactly: current security certifications and data-retention terms at Anthropic's trust center, and which admin/audit controls your plan includes. Don't state specifics you haven't checked.

**4. Why it's different** *(frame as what to test, not as attacks on others)*: Works across the whole task (explore, plan, edit, test, commit) rather than line completion; understands the full codebase and its history; extensible with your own skills, hooks and MCP connections; one tool across Python, TypeScript, Java, Go, shell, notebooks. Close with: "Here's how you'd test each of these claims in your own evaluation" and put the test on the slide.

**5. Across the lifecycle** (template slide: Discover, Design, Build, Deploy, Support).

**6. Fit for your three teams**

| Team | First uses | Why it fits |
|---|---|---|
| 120 software engineers (Python/TS/Java) | Legacy code comprehension, test generation, refactors, PR drafts | Largest group, fastest visible win; demo shows this |
| 40 data scientists | Notebook to pipeline, EDA, model documentation, dashboards | Matches the template's data-science quotes; reduces repetitive work |
| 20 SREs (Python/shell/Go) | Incident triage, runbook drafts, scripts with tests | Small team, high leverage per hour |

**7. Proof from peers** (template slides: Ramp, Fortune 500 modernization). Present these as vendor-reported customer results, not guarantees. Ramp is the best fit (fintech, fast shipping).

**8. Measuring impact** *(your differentiator: they said this is their main concern)*
Three layers, each with a baseline taken before the pilot:
1. **Adoption**: weekly active users, sessions per user, % of PRs with Claude involvement.
2. **Delivery**: PR cycle time, lead time for change, deploy frequency, change-failure rate, time to restore, test coverage on touched code.
3. **Business**: capacity redirected to new products, mobile feature lead time, incidents resolved faster, plus engineer satisfaction survey.
Rule: compare pilot teams against matched control teams; measure quality alongside speed so nobody can claim speed came at the cost of safety.

**9. ROI framing**: Show the formula, not a made-up number. *Value = engineers x loaded cost x time reclaimed + revenue from faster shipping - tooling cost.* Then show the break-even: "At what % time reclaimed does this pay for itself?" (use the sliders in `business-impact.html`; with the default assumptions the capacity value is a large multiple of tooling cost, but those are placeholders; say so). Get their own baseline in week 1.

**10. Evaluation plan: 6 weeks, three phases**

| Phase | Weeks | What | Exit criterion |
|---|---|---|---|
| Prepare | 0-1 | Security review, Bedrock/Vertex access, permissions policy, baseline metrics, pick teams | Security sign-off; baselines captured |
| Pilot | 2-5 | ~30 people: 15 engineers, 8 data scientists, 5 SREs plus 2 champions; 3 use cases per team; matched control group; weekly office hours | Pre-agreed targets hit on delivery metrics with no quality regression |
| Decide | 6 | Scorecard to execs: results, risks, cost, rollout recommendation | Go / adjust / no-go |

Starting use cases: **Engineers**: understand and map a legacy service; generate tests for an untested module. **Data scientists**: convert an approved notebook into a pipeline with a draft model card. **SREs**: triage 3 past incidents read-only, compare with actual timelines; draft runbook updates.

**11. Rollout timeline and next steps**: Weeks 7-12: expand in waves (engineering by team, then data science, SRE), shared CLAUDE.md and skills library, admin policy, internal champions network. Ask: (1) security review kickoff within a week, (2) name the pilot teams and a sponsor, (3) agree the scorecard, (4) hold a follow-up in 10 days. End on time.

## 4. Business view bridge: making BI compelling to non-technical people

The demo's "so what" is mobile adoption, told in four plain-language steps (it's on the top of `outputs/business-impact.html`):
1. Cut the monolith along its natural seams so the **mobile layer stops waiting on everything else**.
2. That lets mobile ship **weekly instead of monthly** (assumption; their number goes in the sliders).
3. Customers see better onboarding and fewer friction points **sooner**.
4. Adoption and payment volume follow.

Talk track for the non-technical exec: "Today a mobile improvement waits in line behind every other change. Claude Code found the 18 places where that coupling lives and drafted the plan to separate them. That's the business case: not lines of code, but how long a good idea waits."

Rules for the BI moment: lead with the customer outcome, then the metric, then the technique. One chart. Label assumptions out loud. Never quote the model's dollar figures as predictions.

## 5. Live demo runbook (12 min, hard stop)

**Setup (do the night before and 30 min before):** `cd legacy-payments-monolith`, `claude` starts cleanly, API key set, CLAUDE.md present, skills visible (`/skills` or ask what skills are available), `outputs/` pre-generated as your fallback, `graph.html` and `business-impact.html` open in tabs, font size large, notifications off.

**Story:** "This is a stand-in for a decade-old payments monolith. Mobile is stuck on its release train. Let's find out why, and what to do about it."

| Min | Do | Say |
|---|---|---|
| 0-2 | Prompt 1 (plan mode): *"Explore this repo. Explain what it does, how modules depend on each other, and where the riskiest coupling is. Use tools/analyze_deps.py to measure rather than guess."* | "It reads the code and runs our analyzer; watch it cite numbers: 12 modules, 42 import edges, one circular dependency (fraud <-> payments), 3 shared tables." |
| 2-4 | Prompt 2: *"Propose service boundaries. For each, list the calls that become APIs and flag data ownership problems. Regenerate the graph with tools/build_viz.py."* Open `graph.html`, tick "shared data tables". | "Orange lines are what would become network calls. The red loop is what we fix first." Let the CTO ask about it. |
| 4-7 | Prompt 3: *"Create EKS manifests for this split: one Deployment and Service per boundary, default-deny network policies derived from the call graph, only mobile-bff internet-facing, batch jobs on a separate node group."* Show `deploy/eks/` diffs. | "Notice the network policies come from the analysis, so least privilege is a result, not an afterthought." Mention manifests are drafts for your platform team to review. |
| 7-9 | Prompt 4: *"Break the fraud <-> payments cycle with the smallest safe change. Write characterization tests first."* Use the `safe-refactor` skill by name. Show tests pass, rerun analyzer: cycles 1 -> 0. | "It writes the safety net first, and the skill encodes your team's rules. Skills are how you scale good practice across 180 people." |
| 9-11 | Switch to `business-impact.html`. Walk the four-step story, drag the release slider from 12 to 48, then the time-reclaimed slider. | Business bridge, section 4. |
| 11-12 | Permissions moment: show the approval prompt on a file edit or command, and the settings that restrict it. | "Nothing runs without a rule or your approval." Then return to slides. |

**If it goes wrong:** say so calmly, switch to the pre-generated `outputs/`, and keep narrating. Handling a failure well is part of what's being tested. Don't run the full refactor live if time is short; show the tests and the before/after metric from a branch you prepared.

**Data scientist and SRE coverage without extra demo time:** Show the three skill names on a slide after the demo, and say what each does in one sentence.

## 6. Questions to expect (and honest answers)

- **"Where does our code go?"** Explain deployment via Bedrock/Vertex in their own cloud accounts, what the tool sends (the context needed for the task), and offer a security deep-dive with specific documents. Don't improvise certifications.
- **"Can it break production?"** Not unless permitted. Approval by default, allow/deny lists, read-only modes, branch + PR + human review + CI remain the gate. Recommend the pilot starts without production credentials.
- **"Model makes mistakes."** Yes. That's why the plan measures change-failure rate and keeps code review. Characterization tests first.
- **"Why not just pick whichever tool is cheapest?"** The tool cost is small versus engineer cost; evaluate on measured outcomes with the same tasks and the same scorecard. Offer to run the evaluation against any tool.
- **"Will this replace engineers?"** Honest answer: the pilot targets capacity redirected to the product roadmap, and it's your call how to use it. Don't promise headcount outcomes.
- **"What does it cost?"** Don't invent pricing; give the structure (per-seat vs usage via cloud provider), say you'll bring a cost model sized to the pilot, and ask for expected usage.
- **"How long to roll out?"** Pilot in 6 weeks; wave rollout over the following ~6 weeks; consistent with their "few months" goal.
- **"Which regulations?"** Don't give legal advice. Say their compliance team signs off, name the controls (audit logs, access, data handling) you'll document for them.

## 7. Customer Solutioning interview (separate session)

Prepare ~3 slides; anonymize.

1. **Customer challenge**: who (industry, size), the business problem in one sentence, why it was hard (constraints: security, legacy, politics), what was at stake, success criteria agreed with the customer.
2. **Technical solution**: one architecture diagram. Label what you designed versus what already existed, data flow, key decisions and **the alternatives you rejected and why**.
3. **Business outcome**: numbers with before/after, timeline, what you'd do differently, what it unlocked next.

Spoken structure (6-8 min, then Q&A): context -> your role -> engagement strategy (stakeholders, how you earned trust, how you handled resistance) -> architecture -> outcome -> reflection. Prepare one story where something went wrong and what you did.

**Send me**: the engagement you want to use, your role, the architecture in rough words, and the results. I'll build the three slides and the talk track.

## 8. Pre-flight checklist

- [ ] Google Meet screen share tested, both interviews, correct window not the whole desktop
- [ ] Claude Code installed, API key works (test one small prompt the day before; credits are limited, $25)
- [ ] Demo repo copied to a clean directory; dry run end-to-end twice with a timer
- [ ] Tabs pre-opened: graph, business view, deck. Terminal font large
- [ ] Deck copied from the template, 11 slides max, speaker notes with minute marks
- [ ] Security facts verified at primary sources; no unverified numbers on slides
- [ ] Thought of 3 questions for the 5 minutes at the end about Anthropic
