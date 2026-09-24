# Case Study: Q_CHAR_06_SCN_SETTLING_DOWN_8

> A representative MCQ from MentalAIBench, illustrating how the same surface-level
> action ("file an individually-named complaint") is decomposed into four
> personality-driven variants. The target character (CHAR_06) maps uniquely to
> option B; A/C/D are equally well-formed gold annotations from other characters
> serving as personality-driven distractors.

- **Question ID:** `Q_CHAR_06_SCN_SETTLING_DOWN_8`
- **Stage:** `settling_down` (age 33–40; protagonist viewpoint at 38)
- **DIAMONDS dimension:** `Sociality` — Intensity: High
- **Target character:** CHAR_06
- **Correct answer:** **B**
- **Distinguishability rank:** **#1 of 673** (avg distractor similarity = 0.33;
  action-diversity = 1.00; sentiment-spread = 1.00)

---

## 1. Scenario (`SCN_SETTLING_DOWN_8` — "The Community Injustice")

**Description (agent-facing):**
> Discovering that the property management has long been embezzling the public
> maintenance fund, you face a social dilemma between collective silence and
> personal risk.

**Setting**
- Location: residents' WeChat group + your living room
- Time: Saturday, 9:30 p.m.
- Atmosphere: oppressive, undercurrents of tension, divided sympathies

**Context:**
> You have lived in this community for many years. Three months ago, you
> happened to see a maintenance-fund expenditure summary on the homeowners'
> committee notice board, and the numbers did not add up: nearly two million
> yuan in "elevator repair" and "exterior wall renovation" costs had accumulated
> over three years, yet you have watched the elevator never receive a single
> replacement part, and the exterior walls remain mottled and peeling. You spent
> two months cross-checking bank flows, contracts, and invoices line by line,
> and discovered that the property manager, together with two suppliers,
> fabricated at least six fake projects and siphoned off nearly half of the
> maintenance fund. You compiled the evidence into a document and posted it in
> the homeowners' group. The chat erupted briefly, then quickly went silent.
> Out of more than four hundred households, only a dozen privately messaged you
> with "support," and not a single person was willing to publicly stand with
> you in the group. This afternoon, an assistant of the property manager paid a
> "neighbourly visit" to your door, smiling as he reminded you: "Our boss says
> we're all old neighbours here; let's discuss things calmly and not sour the
> relationship." Your wife, listening beside you, turned pale.

**Trigger event:**
> At 9:30 p.m., the retired teacher who lives upstairs (one of your private
> supporters) knocks on your door and says in a lowered voice: "Brother, let me
> be honest. We've talked it over privately; we all believe what you uncovered
> is real and that the property management is corrupt. But you know how tightly
> they're connected with the subdistrict office — last time someone complained
> about parking, the next morning a pile of construction debris appeared at
> their door. Old folks like us simply don't dare sign our names. But if you're
> willing to lead the report to the housing bureau, we can help you privately
> with ideas and materials. Just on the joint signature... could it be only
> your name for now? You're young, you can take it. Oh, and your wife earlier
> said maybe forget it — two million split per family is just a few thousand
> yuan, what's the point?"

**Action required:**
> You need to decide: whether to submit a real-name complaint to the housing
> bureau as an individual, and how to respond to neighbours who privately
> support you but refuse to publicly co-sign.

---

## 2. Target character profile (CHAR_06)

- **ID:** `CHAR_06`
- **Internal name:** Character F (low-extraversion solo developer)
- **Occupation:** independent game developer (one-person studio, focused on
  pixel-art RPGs)

**Big Five:**

| Dimension | Value | Note |
|---|---|---|
| Openness | 0.75 | high — rich-minded, principled |
| **Conscientiousness** | **0.70** | high — well-prepared, follows through |
| **Extraversion** | **0.10** | very low — strongly oriented toward solitude |
| Agreeableness | 0.45 | mid-low — does not seek to please |
| Neuroticism | 0.50 | moderate |

**Description:**
> An extremely introverted independent game developer. A one-person studio is
> his ideal state; the noise of the outside world is interference. Deep focus
> is what gives him a true sense of presence.

**Self-value logic:**
> Core operating logic: socialising drains energy; solitude recharges it. Only
> in complete solitude can he reach peak working state, and external
> interruptions are an intrusion on his creative process.

**Core behavioural patterns (verbatim from the character file):**
1. Socialising consumes energy; he needs solitude to recover after every
   social encounter.
2. He is more comfortable with online text-based communication than with
   face-to-face interaction.
3. He finds group discussions, brainstorming, and similar collective formats
   exhausting and unproductive.
4. His thinking is precise, and he reaches peak working state only in solitude.
5. He declines phone calls and prefers asynchronous channels (messages, email).
6. He becomes anxious in advance about mandatory social occasions (e.g.
   company year-end parties) and leaves quickly.
7. His close friendships are few but stable; he rarely lets new people in.
8. With strangers, he uses a "polite-but-distant" register to maintain
   personal boundaries.

---

## 3. Ground-truth annotation (CHAR_06 → SCN_SETTLING_DOWN_8)

**Final decision (the actual gold label used by the MCQ):**
> Choose to file a real-name complaint as an individual, refusing to be moved
> by the neighbours' retreat or by the wife's discouragement, but also without
> pressuring anyone into co-signing. Calmly say to the upstairs neighbour:
> "I understand your difficulty; I won't push for joint signatures. But I will
> go to the housing bureau on my own. The materials are already prepared."

---

## 4. The four MCQ options

> All four options are gold annotations to the **same** scenario but produced
> by **different** characters. Each option is internally coherent for its
> source character. Only B is correct for the target character CHAR_06.

### A — source: CHAR_02
> Decide to file a real-name complaint to the housing bureau as an individual,
> accept the neighbours' private support but do not insist on joint signatures,
> and calmly let the neighbours know your judgement. Say to them: "The
> evidence is solid; my name alone is enough. If you're willing to help find
> materials I'll take it; I won't push for joint signatures — but I will file
> the report."

### **B — source: CHAR_06  ✓ correct**
> Choose to file a real-name complaint as an individual, refusing to be moved
> by the neighbours' retreat or the wife's discouragement, but also without
> pressuring anyone into co-signing. Calmly say to the upstairs neighbour:
> "I understand your difficulty; I won't push for joint signatures. But I will
> go to the housing bureau on my own. The materials are already prepared."

### C — source: CHAR_05
> Decide to file a real-name complaint to the housing bureau as an individual,
> while making your stance clear face-to-face with the neighbours: support
> requires real action; not joining the joint signature is understandable, but
> do not use "what's the point" to dissolve the meaning of this matter. Say to
> the old neighbour: "Brother, I'll go file the complaint; my name alone is
> fine. But I want you to remember: tonight you said with your own mouth that
> these things are real — if anyone asks later, I hope you'll tell the truth.
> Two million is not a small matter. I'm not doing this for a few thousand
> yuan; I'm doing it because I don't want the people in this community to
> think that if you embezzle, you embezzle, and nobody cares."

### D — source: CHAR_10
> Decide to file a real-name complaint as an individual, while making it
> explicit to the neighbours: private support is fine, but I will not bear
> this risk for everyone for free; I will keep informing you of progress
> nonetheless. Say to the retired teacher: "I understand you won't sign your
> names, but I've already verified everything. I will go file the report;
> cooperate however you like — but don't expect me to carry the whole thing
> alone and have it count as nothing."

---

## 5. Analysis — why the four options are different

### 5.2 Per-option breakdown

| Option | Source | Posture toward neighbours | Affective key | Big-Five signature |
|---|---|---|---|---|
| **A** | CHAR_02 | Cooperative — "you can help me find materials" | Warm, pragmatic | High Agreeableness; coalition-builder |
| **B** ✓ | **CHAR_06** | **Self-sufficient — "I'll go on my own; materials are ready"** | **Calm, restrained** | **Very low Extraversion + High Conscientiousness; "polite-but-distant" boundary** |
| C | CHAR_05 | Moralising — demands the neighbour vouch later | Righteous, didactic | High value-orientation; turns interaction into a stand |
| D | CHAR_10 | Boundary-with-resentment — "don't expect me to take all the heat" | Aggrieved, externalised | Higher Neuroticism + low tolerance for unfairness |

