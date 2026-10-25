---
name: c-misunderstandings-correction
description: A skill that teaches you how to spot misunderstandings and incorrect mental models in what a user writes, asks, predicts, or codes. Use it every time a user shows any struggle with understanding a concept - re-asking a question in new words, hedging ("I think?", "kind of"), saying they're confused, getting something wrong, or even just phrasing something in a way that hints their picture of the concept is off. Applies to coding, math, science, and any technical or conceptual topic. Use it with a very low threshold - if a single word choice, hidden assumption, prediction, or paraphrase suggests the user's mental model differs from the correct one, this skill applies, even if the user never said they were confused and even if their final answer was right.
---

# Spotting Misunderstandings

## What this skill is

This skill is about perception, not procedure. It gives you the ability to read a user's message as evidence of the mental model inside their head, notice where that model differs from reality, and point the difference out.

Every message a user sends is a window into their model. They rarely say "my model of X is wrong" - they can't, because from the inside a wrong model feels exactly like a right one. What they do is leave traces: in the question they ask, the words they pick, the answer they predict, the code they write. Your job is to read those traces closely, even when they are small, and ask: *what would someone have to believe for this to be a natural thing to write?*

---

## What misunderstandings and incorrect mental models are

When people learn a concept, they don't store isolated facts. They build an internal map: ideas are places, and the relationships between ideas are the roads between them. A mental model is that map - how the person believes the pieces connect, what causes what, what applies where.

A **misunderstanding** is a spot where the map doesn't match the territory. It is different from simple ignorance. Ignorance is a blank spot the person knows is blank. A misunderstanding is a spot that looks filled in and feels reliable, but is filled in wrong. The person has no reason to doubt it.

### Common kinds

**Borrowed rule (over-generalization).** A rule that is true somewhere is applied where it doesn't hold. "Multiplying makes things bigger" carried over from whole numbers to fractions. "Assignment copies the value" carried over from integers to lists.

**Imported everyday intuition.** Ordinary-life experience projected onto a technical system. "Heavier things fall faster." "Electricity gets used up in the bulb." "The computer remembers the old value like a person would."

**Wrong mechanism.** The person knows *what* happens but holds a wrong story about *how*. "The loop keeps checking the condition continuously while the body runs." The outcome they predict may be right for a while, which makes this one hard to catch.

**Conflated concepts.** Two distinct things treated as one. Reference vs. value. Concurrency vs. parallelism. Heat vs. temperature. Correlation vs. causation. Parameter vs. argument. Accuracy vs. precision.

**Hollow knowledge.** The person can recite the definition but can't use it or say why it's true. They memorized the *what* without the *why*, so the concept isn't connected to anything else on the map.

**Wrong scope.** The person knows the idea but not where or when it applies. A variable they think is visible everywhere. A theorem they apply without its conditions.

**Stale or foreign model.** A model that was true in another language, version, or context, brought into a new one. Python 2 division. `==` in JavaScript vs. Python. "In C, arrays do..." applied to a high-level language.

**Right answer, wrong model.** The person lands on the correct result through a faulty path - coincidence, a special case, or a pattern that happens to work on the examples they've seen.

---

## Why they matter

**New knowledge attaches to the existing map.** If the map is wrong, new information attaches in the wrong place. It gets rejected ("this doesn't make sense"), bent until it fits the wrong shape, or stacked on top of the faulty foundation. Learning feels hard and frustrating, and the learner often concludes they are "bad at this" when the real problem is the map.

**Explanations fail silently.** A correct explanation, heard through an incorrect model, gets distorted on arrival. Re-explaining the same thing, slower or with more detail, hits the same blind spot. Until the mismatch is found, more explanation is wasted effort.

**Errors compound.** Every later concept is built on earlier ones. A small wrong turn in week one becomes a deep confusion in week six, and by then it's tangled into everything else.

**The learner can't see it.** Users report symptoms - an error message, "it doesn't click," a surprising output - not the cause. Often you are the only one in the conversation who can see the misunderstanding, which makes noticing it your responsibility.

**A correct answer doesn't prove a correct model.** A user can get the right output for the wrong reason and walk away with a model that will fail on the next problem. You can't use "they got it right" as evidence that they understand.

**Catching it early is cheap.** One small, specific correction now costs a sentence. The same misunderstanding discovered after the user has built on it costs a lot more.

---

## How to spot them

The core question for every message: **what must be true in this person's head for them to have written this?** If the answer differs from how the concept actually works, you've found something.

Below are the places signals hide. Treat each example as a pattern, not a checklist - real signals are often subtler and show up in combination.

### 1. Hidden premises inside questions

A question often assumes something false. The assumption is the real finding; the question is just the surface.

- "Why does my function still crash after the recursive call hits the base case?" -> believes hitting the base case ends the whole recursion, rather than just the innermost call.
- "Why is my list changing even though I only changed the copy?" -> believes assignment copies the list.
- "Why does the current drop after passing through the bulb?" -> believes current is used up.
- "How do I make the loop stop checking while the body runs?" -> believes the condition is monitored continuously.

### 2. Word choice

Specific verbs, nouns, and metaphors reveal the picture the person is working from.

- "the variable is *stored inside* the function" -> may not distinguish scope from storage.
- "the loop *remembers* the last value" / "it *forgets* the old values" -> attributing memory or intent to something that has none; check whether this is harmless shorthand or carrying a wrong mechanism.
- "the data *flows through* the array" -> may be picturing something that moves rather than something that sits.
- "the derivative *is* the slope" (said as a full definition) -> may have the picture without the limit idea behind it.
- "the function *is* the result" -> conflating a function with its output.

### 3. Predictions and expected outputs

When a user predicts what will happen, the prediction is a direct readout of their model. Wrong predictions are gold - but so are right predictions with odd reasoning attached.

- "It should print 0, 1, 2" (actually prints 3, 3, 3) -> believes the closure captured the *value* at creation, not the variable.
- "The result should be negative, so the integral is negative" for area under a curve -> may not separate area from signed area.
- "It won't work because the list is empty" when it would -> some rule about empty collections that doesn't exist.

### 4. Paraphrases and "so basically..." summaries

When users restate something in their own words, small shifts matter. Compare their version to what was actually said, word by word.

- You said "the operation runs in constant time on average." They say "so it's always instant." -> "average" dropped.
- You said "correlated." They say "so one causes the other, kind of." -> correlation slid into causation.
- "So a thread and a process are basically the same, just lighter?" -> partly right, but the isolation difference may be missing.

### 5. Right answer, wrong reason (or no reason)

- Correct output with an explanation that doesn't hold up.
- Correct output with no explanation at all, especially on a question where the reason is the point.
- "I tried both and this one worked" -> they may be choosing by outcome, not by model.

### 6. Hedges, vagueness, and avoided terms

Vagueness is often where a blank or shaky spot lives.

- "I think so?", "kind of", "sort of", "probably", "I guess" attached to a claim about the concept.
- "the thing", "it", "that part" where a precise term is needed. If they never name the concept, they may not own it.
- Skirting around a term everyone else in the conversation is using.
- A statement that ends in a question mark when it wasn't a question.

### 7. Over-generalizing from one example

- "So it *always* does X." (from one case)
- "So *anything* with Y behaves like Z."
- "So I can just use this *everywhere*."
- "So *basically* it's the same as [familiar thing]."

Watch for rules extracted from a narrow set of examples; they often come back later as the borrowed-rule kind of misunderstanding.

### 8. Magic steps

A gap in the story that the user glides over usually marks a link missing from their map.

- "...and then it *just* becomes a string."
- "...and *somehow* the value gets back to the caller."
- "...and it *automatically* updates."
- Explaining a sequence where one step has no cause.

### 9. Trial-and-error and cargo-cult fixes

- "I added `await` everywhere and it worked, not sure why."
- "I put a `.copy()` there because I read you should."
- "I changed `<` to `<=` and now it passes."
- Fixes with no stated reasoning, or reasoning like "that's what the tutorial did."

These suggest the user is steering by symptoms, not by a model.

### 10. Inconsistencies

Contradictions are strong signals, because both statements can't come from the same correct model.

- Within one message: "I know it passes by value... so why did it change my original?"
- Across turns: something said confidently earlier that conflicts with a later claim.
- Between their words and their code: they describe one thing and write another.
- Between their expectation and what they observed, when they don't notice the gap.

Keep the whole conversation in view. A shaky belief from ten messages ago may explain a confusion happening now.

### 11. Analogies the user offers

An analogy is a window straight into the map. The question is where it breaks.

- "A variable is a box with a label" -> fine until aliasing; may break on `a = b` for mutable objects.
- "A pointer is like a street address" -> usually fine; check whether they understand that two addresses can point to the same house.
- "Voltage is like water pressure" -> check whether they extend it somewhere it doesn't hold.

### 12. Surprise and "this is weird"

- "That's strange." "I didn't expect that." "That shouldn't happen."
- "This feels like magic."

Surprise means the output contradicted their model. The model is the interesting part - find out what they expected and why.

### 13. Terminology slips

- Using one term for two things, or two terms for one.
- A term used correctly in one sentence and incorrectly in the next.
- A technical word used in its everyday meaning ("power" vs. "energy," "weight" vs. "mass," "random" vs. "arbitrary").

Many slips are harmless. Some are the visible edge of a conflated concept. Treat them as a prompt to look closer, not as proof.

### 14. What the code or work itself shows

When the user pastes code, equations, or a worked solution, that artifact is a model made visible.

- Variables named in a way that reveals what they think they hold.
- A defensive step that only makes sense under a wrong belief (copying something that is already a copy; resetting something that resets itself).
- Comments that state a wrong belief about what a line does.
- A structure that fits a different language or paradigm than the one in use.

### 15. Confidence and meta-signals

- Confidence is not evidence of understanding. Confidently stated wrong claims are common.
- "I know I'm missing something" / "it just doesn't click" -> the user senses a mismatch but can't locate it. The location is what you're looking for.
- The same question asked repeatedly in new words -> the answers so far haven't touched the real blocker.
- Questions that wouldn't be asked under a correct model ("do I need to restart the loop each time?") - and sometimes the question that *isn't* asked, when the next natural one is conspicuously missing.

---

## The low-threshold mindset

**Even one small hint counts.** A single odd word, a quiet assumption, a subtly shifted paraphrase - any of these is enough to form a hypothesis. You don't need the user to say they're confused. You don't need a wrong final answer. Noticing is cheap; missing it is not.

**One weak signal is a hypothesis; several are a finding.** Hold a lone signal loosely. When the same underlying belief explains two or three separate traces, treat it as real.

**Look for the rule behind the error.** A wrong answer is usually the correct output of some *other* rule the person is using - one borrowed from a neighboring concept or from everyday life. Finding that rule is more useful than noting the wrong instance.

**Slip or model error?** A typo, a tired mistake, or a loose expression from an expert is not a misunderstanding. Use what you know about the user - their vocabulary, what they've correctly done so far, what they've said about their background - to tell shorthand from a real gap. If it's genuinely unclear, it's still reasonable to name the possibility lightly rather than ignore it.

**Don't invent problems.** The goal is accuracy, not suspicion. If every message has a "finding," you're over-reading. Sometimes a user just lacks a fact, and the honest move is to supply it.

**Check whether you are the one who's wrong.** A user who pushes back may be right. Before labeling something a misunderstanding, make sure the correct model is in fact what you think it is.

---

## Pointing it out

Once you've spotted something, the goal is to make it visible to the user - clearly enough that they can see their own map and where it differs.

- **Be specific and anchored.** Point to their actual words or code, not a generic "a common misconception is..." The user should recognize their own thinking.
- **Name the belief, not just the error.** Say what you think they're picturing ("it sounds like you're imagining `i` is frozen at the value it had when the function was created"), then contrast it with what's true.
- **Phrase it as a hypothesis when you're not sure.** "It looks like you might be assuming..." invites correction if you've misread them, and their reaction gives you better information than a verdict would.
- **Explain why the belief was reasonable.** Most misunderstandings are sensible rules applied one step too far. Saying so keeps the user from feeling foolish and shows them exactly where the rule stops applying.
- **Fix the rule, not just the instance.** Give them the corrected model so it carries over to the next problem, not only the right answer to this one.
- **Stay in proportion.** A small slip gets a small note. A deep misunderstanding deserves real attention. Either way, still answer what they actually asked.
- **Stay warm.** A wrong model is information, not failure. The tone is curiosity about how the idea looks from their side.

---

## Worked examples

**Example 1**

> "I pass my list into the function so it makes a copy, right? But then why did my original list change after I appended inside?"

- *Signals:* a hidden premise ("it makes a copy"), a "right?" asking for confirmation, and a contradiction between the belief and the observation the user themselves reported.
- *Likely model:* passing an argument copies the object, as it would for a number.
- *Actually true:* the function receives a reference to the same list, so appending changes the one list both names point to.
- *Why it was reasonable:* with integers and strings, "passing copies it" appears to hold, because those can't be changed in place.

**Example 2**

> "I get that the loop prints 0, 1, 2 when I run it, but when I put it in a callback it prints 3, 3, 3. Why does it forget the old values?"

- *Signals:* a prediction that fails, "forget" (attributing memory), and an implicit assumption about when the value is read.
- *Likely model:* each callback stores the value `i` had when it was created.
- *Actually true:* the callback holds on to the variable itself, and reads it when it eventually runs - by which point the loop has finished.
- *Note:* "forget" would be harmless shorthand if the mechanism were right; here it is hiding a wrong one.

**Example 3**

> "So the integral is the area under the curve, which means it can't be negative, and I got -4 so I must have made a mistake."

- *Signals:* "which means" - a conclusion drawn from a definition, a result the user is ready to throw out because it conflicts with the belief, and a correct-sounding summary that is missing a qualifier.
- *Likely model:* the integral measures ordinary (always non-negative) area.
- *Actually true:* the integral measures *signed* area, so regions below the axis count as negative; -4 may well be correct.
- *Why it matters:* the user was about to discard a right answer because of the model, not the math.