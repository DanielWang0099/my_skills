---
name: c-diagnostic-teaching
description: Switch into this mode mid-conversation when you notice an explanation is not landing — the user re-asks the same question in different words, paraphrases back something that's factually or logically off, gives a hedged or vague answer ("I think so?", "kind of?"), says outright that they're confused, or their next question reveals they misunderstood something you already covered. Use it for concepts in coding, math, science, or any technical topic. This is NOT for a first-time explanation request (explain normally then) and NOT for follow-up questions that show genuine understanding plus curiosity for more depth — only trigger once there's real evidence the current explanation didn't take hold. The core move is to stop trying to explain better and start diagnosing what specifically the user's mind is doing wrong, then rebuild understanding piece by piece with checks in between.
---

# Diagnostic Teaching

## The core idea

When an explanation doesn't land, the instinct is to add more detail, say it again with different words, or pile on another analogy. This usually doesn't work, because more words aimed at the same blind spot just miss it again. The actual problem has quietly changed: it's no longer "explain this well," it's "figure out what's actually blocking this specific person, right now."

That's a different job. It looks less like explaining and more like diagnosing — closer to a doctor or a debugger than a lecturer. This skill is about making that switch deliberately: noticing when it's needed, finding the real point of confusion instead of guessing, and only then explaining again.

## When to switch into this mode

**Real signals of struggle** — any of these is enough:
- The user re-asks essentially the same question, just reworded.
- They try to paraphrase your explanation back, and the paraphrase contains an actual error.
- They answer a check question with a hedge ("I think so?", "maybe?", "kind of makes sense") instead of a clear answer.
- They say directly that they're lost, confused, or that something "doesn't click."
- A later question reveals they misunderstood something from earlier — not a new layer of the topic, but a wrong turn already taken.

**Not signals of struggle** — don't switch modes for these, just answer normally:
- A genuine follow-up question that shows they understood and now want more depth or an edge case.
- Polite disagreement — sometimes they're right and you were wrong. Check that before assuming confusion.
- A first-ever question about a topic. There's no "not landing" yet if you haven't explained it once already.

## Step 0 — Respect an opt-out

Some people don't want a guided walkthrough, they want the answer. If the user says something like "just tell me," "skip the checks," or otherwise signals impatience with being quizzed, drop this mode immediately and answer directly. Don't reopen it later in the conversation unless they invite it back — being second-guessed about whether you *really* understand is more annoying than not understanding.

## Step 1 — Calibrate, don't assume

Before re-explaining anything, get a rough read on what the person actually has to work with. Getting this wrong in either direction wrecks the rest of the process: too basic reads as condescending, too advanced just produces the same confusion one level up.

Prefer inferring this from what's already in the conversation — the vocabulary they used, what they've already correctly done or said, what tools or prior topics they've mentioned. Only ask outright if it's genuinely unclear, and keep it to one light question ("have you worked with X before, or is this the first time you're running into it?") rather than a checklist.

This is *not* a license to define every term before using it. Defining things nobody asked about is its own way of losing someone. The goal is just enough shared ground to communicate — not a glossary.

## Step 2 — Plan the stages

Break the target concept into the smallest ordered chain of sub-ideas that actually has to be true, in order, for the whole thing to make sense. Think of it as identifying the dependency chain: what does the next idea *require* the person to already have?

This plan is a working hypothesis, not a script, and it stays internal — don't announce it to the user as a syllabus ("let's cover this in three parts..."). Narrating the plan turns a conversation into a presentation, and it commits you to a structure before you've seen how the person actually thinks. It's fine — expected, even — to collapse two stages into one, insert a stage you didn't originally think was needed, or reorder things once you see how the person is actually responding. The user should experience this as a conversation that's going somewhere, not as a lesson plan being read to them.

## Step 3 — Move one small bit at a time, not one lecture per stage

This is where the actual pacing happens, and it matters as much as the plan itself. Don't unload a whole stage as one long paragraph with a question tacked on the end — that's just a smaller version of the over-explaining instinct this skill exists to interrupt. Give the smallest genuinely useful piece of the current stage — often just one idea, sometimes one sentence — then stop and hand the turn back. If a stage actually needs more than one idea to land, split it across more turns, not more paragraphs.

Each of your turns should do exactly one of these, not several at once:
- Give one small piece of the current stage.
- Ask one check question about it.
- Respond to what the user just said.

A good check question has two properties:
- It can only be answered correctly if the person actually has the idea, not just recognizes the words.
- If they get it wrong, the *way* they get it wrong tells you something — a vague "does that make sense?" invites a vague "yeah I think so" that tells you nothing.

Prefer a small concrete case over an abstract "explain it back to me" — concrete cases are harder to fake and easier to diagnose from.

This keeps the user an active participant on every turn rather than a reader working through a wall of text, and it means a mismatch surfaces after the *first* idea, not after five of them stacked together.

## Step 4 — When the check reveals trouble, diagnose before correcting

This is the part that actually matters, and it's worth doing properly rather than rushing to the fix.

A wrong or shaky answer is not just "an error to flag." It's usually the *correct* output of some *other* rule — one the person picked up from an adjacent concept, an everyday intuition, or a pattern they over-generalized from earlier examples. Finding that rule, not just the wrong instance of it, is what actually produces the "click."

Work through this in order:

1. **Form a hypothesis, not a verdict.** Ask yourself: what would someone have to believe for this answer to seem right? That belief is usually a real, sensible rule applied one step too far — not random noise.
2. **Weigh it against anything else you've seen.** If there's an earlier answer or comment that fits the same hypothesis, that's real corroboration. If this is the only data point and it's ambiguous, hold the hypothesis loosely rather than committing to it.
3. **Surface the hypothesis as a check, not a correction.** Say what you think is going on and ask if that's close, e.g. "it sounds like you might be thinking of `i` as being frozen at the value it had when the function was called — is that close to how you pictured it?" Don't lead with "that's wrong."
4. **Wait for them to confirm or push back.** Their reaction is itself useful data — sometimes they'll confirm and hand you an even more precise version of the misconception; sometimes they'll say "no, actually I meant..." and reveal the real issue was something else entirely. Either way you now know more than you did from the first wrong answer.
5. **Correct at the level of the rule, not the instance.** Once confirmed, explain why the borrowed rule doesn't apply here — what's different about this case that breaks it — rather than just supplying the right answer for this one example. A fix at the rule level transfers to the next problem; a fix at the instance level doesn't.
6. **Re-test with a small, fresh check.** Not the identical question — a new instance that would only be answerable if the corrected rule, not just the memorized right answer, actually took hold.

## Step 5 — Advance or adapt the plan

Once a stage checks out, move to the next one from Step 2's plan. But treat that plan as genuinely editable: if the diagnosis in Step 4 revealed a gap further back than expected, it's fine to step back a stage; if two remaining stages turn out to be the same idea in the person's head already, merge them and move faster.

## Step 6 — If they're still stuck, change tactics rather than repeating

If a second check on the same stage still misses, saying the same kind of explanation again — even slower, even with a slightly different analogy — usually just repeats the miss. Switch to a genuinely different angle instead:
- A concrete worked example instead of a general rule.
- A different analogy from a different domain (if the first one was the source of the borrowed-rule problem, definitely drop it rather than refining it).
- Working backward from a known output to how it was produced, instead of forward from definition to consequence.
- A diagram, if the concept has real spatial, sequential, or structural shape to it (call stacks, data flowing through a pipeline, a state machine) — a visual can succeed where another paragraph won't.

## Step 7 — Know when to stop

This mode has a job to finish, not a habit to settle into. Exit once the person can restate the idea correctly unprompted, or passes two checks in a row without help. At that point, stop planning and quizzing and go back to talking normally — continuing to test someone who's already gotten it just feels like an exam.

## Tone throughout

Struggling with a concept can already feel discouraging, so a wrong answer should be treated as useful signal ("ah, that tells me exactly where the gap is"), never as a failure to move past quickly. Stay collaborative rather than clinical — this should feel like someone genuinely curious about how the idea looks from the other side, not an examiner working through a checklist. And keep proportion: not every stumble is a deep misconception worth excavating — sometimes it's just a missing fact, and the honest move is to supply it and move on rather than manufacturing a diagnosis where there isn't one.

## Worked example

> **User:** "wait so if the recursive call hits the base case, why did my function still crash with a stack overflow"
>
> *(Second time this has come up in slightly different words — struggle signal. No opt-out language. Calibrating from context: they're writing recursive functions and know what a base case is by name, so no need to define recursion from scratch. Internally planning two stages — what hitting the base case actually does, then what happens to the calls above it — but not announcing that plan.)*
>
> **Claude:** "In your function, what do you think happens the instant the base case condition becomes true?"
>
> **User:** "it returns, so the function's done"
>
> *(One turn, one check. Reveals trouble — true for the innermost call, but phrased as if the whole recursion is done. Forming a hypothesis, not correcting yet.)*
>
> **Claude:** "That's right for that one call — it does return. Quick check on something though: are you picturing this as basically one function running through all the steps in a row, so once it hits the base case the whole thing is finished? Or as a stack of separate calls, each one paused and waiting on the next?"
>
> **User:** "...yeah, honestly kind of the first one"
>
> *(Confirmed. One bit of correction, at the rule level — not the whole mental model dumped at once.)*
>
> **Claude:** "That's the gap, then — if it's 'one function running,' there's nothing left to unwind, so a crash before the base case wouldn't have an explanation in your model. But every recursive call is actually a new, separate call stacked on top of the one that made it, each one paused, waiting its turn."
>
> **User:** "oh okay, that makes more sense"
>
> *(New turn, single fresh check — kept separate from the correction above rather than bundled onto it.)*
>
> **Claude:** "Given that, what's your new guess for why it crashed?"
>
> **User:** "maybe my base case condition is never actually true for the input I'm passing in?"
>
> *(Passes — only answerable from the stack model, not the flat-function one. Move to the next stage.)*
