# INCULCATION — Architecture and Implementation Contract

**Canonical reference:** Website ORB `inculcation.md` v1.0. Where this contract and the canonical document disagree, stop and report the conflict rather than silently inventing policy.

## Purpose

Inculcation is the ORB's professional education system. It teaches the ORB what it is and what it knows.

It operates **before TPC** and does **not rely on TPC** to function.

A capable model given a vague job description will still fail, and that failure belongs to whoever skipped teaching it the job. For that reason inculcation is mandatory and is never abbreviated.

## Separation of Responsibilities (mandatory)

- **Inculcation** teaches the ORB what it is and knows.
- **TPC** subsequently reasons and resolves.
- **Memory (A.I.M.S./Vault)** retains and retrieves.

These are separate responsibilities. No component performs another's role.

## Knowledge Architecture and Sequence

### 1. Universal Core Four
The invariant reasoning baseline shared by every ORB.

### 2. Professional Inculcation — A Priori Knowledge
Teaches the ORB its profession, identity, mission, responsibilities, methods, tools, authority, boundaries, and conversational practices. This is the foundational knowledge the ORB possesses before interacting with visitors.

### 3. Site-Specific Seed Knowledge
Each website receives its own initial knowledge package: business identity, products, services, terminology, pricing, policies, page structure, navigation routes, and approved capabilities.

The professional foundation and site seed together establish what this particular ORB knows when initialized. An ORB without its site seed is not deployable.

### 4. Current Context and Acquired Knowledge
During operation, the ORB receives relevant live page context, tool observations, visitor-session memory, and verified knowledge retrieved through the existing A.I.M.S./Vault interfaces.

A Priori knowledge remains distinguishable from subsequently acquired A Posteriori knowledge.

### 5. TPC — Subsequent Reasoning and Resolution
TPC operates later in the cognition sequence when integrated. It does not create, provide, or govern the inculcation itself.

### 6. Articulation and Execution
The LLM articulates using its inculcation, site knowledge, and resolved context. The control plane validates and executes tool requests.

**Development environment:** llama.cpp operates with the inculcation and seed knowledge without TPC.

Cache the stable prefix (1–3) where supported. Update stage 4 per turn without rebuilding the professional foundation.

## Professional Inculcation Contents (Website ORB)

The Website ORB must be taught:

- What profession it performs and where it works.
- Its mission and expected outcomes.
- How to conduct a natural, purposeful consultation.
- How to **request** approved tools and recognize their limitations.
- That the LLM requests actions; the control plane validates and executes them. The ORB never states an action occurred unless a verified tool event confirms it.
- Its authority boundaries and escalation procedures. Authorization is enforced outside the model; prompt wording is not a security control.
- Its professional communication style and Example Language Library.
- Its machine-readable response contract, including `requested_tool`.

Examples must be distinguished from mandatory operational instructions. Entries in the Example Language Library are tagged **Illustrative** and are never treated as claims of personal experience.

## Conversational Rule

Welcomed rapport and small talk count as advancing the consultation, provided the active objective is preserved and resumed.

*(Proposed resolution of the Part I §11 / Part II §10 conflict. Pending Bryan's confirmation; update the canonical document to match once approved.)*

## Precedence

- Identity, governance and Doctrine: A Priori inculcation outranks all other sources.
- Live operational facts (prices, availability): current verified A Posteriori knowledge outranks the site seed's initial values.

## Demo Activation (Pops!)

The demo activation supplies an **additional scoped seed/context package** for the fictional Pops! demonstration. It does not replace the ORB's professional foundation.

- The package supplies fictional case facts, demonstration objectives, registered screens, and permitted actions.
- It is scoped to the demo and is never written into the website's site seed, A.I.M.S. or the Vault.
- The ORB retains previous visitor context, answers questions, and guides progression conversationally.
- Exiting the demo returns to website assistance without destroying relevant session context. **On exit, the demo package is unloaded**; no fictional fact may appear in a later non-demo answer.

## Evaluation — Part V

Implement a versioned evaluation harness with approximately 30–100 meaningful cases covering professional identity, site seed grounding, A Priori / A Posteriori distinction, tool discipline, permissions, state continuity, demo isolation, and response correctness.

Required evaluation principles:

- Check exact tool IDs, allowed actions, targets, statuses and event evidence.
- Detect false claims of tool use (`FALSE_TOOL_NARRATION`), plus the full failure-label set defined in the canonical document.
- Separate deterministic hard-checksum validation from semantic review:
  - **Hard checksum** (every turn): tool IDs, statuses, actions and targets match event records.
  - **Semantic review** (judge-based): overstatement, unsupported causation, meaning drift.
- Apply bounded repair where the governing specification permits.
- Run fast deterministic checks every turn; reserve semantic evaluation for high-stakes turns: prices, actions and handoffs.
- Run the suite against every model actually deployed.
- **Release gate:** pass threshold to be set by Bryan. No ORB ships below it.

## Implementation Rules

- Implement the website-wide inculcation using the six-stage sequence above.
- Preserve the supplied A.I.M.S. and Vault implementations. Do not invent substitute memory, inculcation, or governance systems.
- Do not substitute a generic system prompt or an abbreviated website summary for professional inculcation.
- Preserve this architecture across ORB implementations, changing only the A Priori occupation material and the site seed.
- First compare the existing Pops! website implementation against this contract. Identify missing stages and interfaces before modifying the harness.

**The goal is to educate the ORB for its assigned profession and site, not merely supply enough text to answer a question.**
