# Browser sandboxing
Status: emerging
Sources: [Chromium Security — Site Isolation](https://www.chromium.org/Home/chromium-security/site-isolation/) (primary documentation); [W3C — WebDriver](https://www.w3.org/TR/webdriver2/) (standard)

## In one sentence
Browser sandboxing gives a computer-use agent a constrained, observable browser process whose page content, network access, files, and credentials cannot silently become unrestricted powers.

## Background: what existed before

A conventional browser assumes a person is the authority. The person chooses a tab, recognizes a suspicious page, decides whether a download is expected, and notices when a site asks for a password. A browser automation script historically inherited that assumption: it received a URL, found a selector, clicked, and returned a result. The main boundary was the browser's same-origin policy, which separates one website's script from another site's data. That policy is essential, but it is not a complete agent boundary. A user can still be tricked into approving a transfer, and an automation process can still hold a session cookie while it visits hostile content.

An agent changes the threat model because page text becomes model input and model output becomes an action. A page can place an instruction in a comment, an advertisement, a PDF, or an image. That instruction is untrusted data, even when it looks like a system message. If the browser process can reach an internal service, read a local file, or reuse a broad login session, a successful prompt injection can cross from content manipulation into a real side effect.

Sandboxing is a collection of boundaries rather than one switch. The browser renderer, automation controller, network proxy, file system, credential broker, and host must each have a limited role. The objective is not to prove that a model will never make a mistake. It is to make a mistake cheap, visible, and reversible.

## What changed and why now

The important change is the move from trusted automation to least-privilege browsing. A browser agent needs a disposable profile, a policy-controlled network path, and explicit approval for sensitive actions. The page is now an adversarial input channel. Modern browser security features such as site isolation reduce the damage of renderer compromise, while WebDriver-like interfaces make browser actions explicit enough to audit. These are source-context facts about platform boundaries; the design recommendation that combines them into an agent sandbox is an engineering inference.

A useful sandbox defines three planes. The observation plane exposes pixels, accessibility nodes, and selected page metadata. The control plane accepts a small vocabulary such as navigate, click, type, and upload. The authority plane decides whether a requested action may use a domain, credential, file, or payment instrument. Keeping these planes separate prevents a screenshot from granting permission and prevents a model's natural-language plan from bypassing policy.

## Impact on current processing and architecture

The request path should be explicit. A task service creates a run with a narrow policy: allowed origins, maximum duration, permitted downloads, and whether credentials may be brokered. A controller starts an isolated browser context. A network proxy checks every request, and a redaction layer removes secrets before observations reach the model. The policy engine evaluates the proposed action again immediately before execution because the page may have changed between observation and action.

The browser should not run with the host user's profile. Use a temporary profile and a temporary filesystem directory. Mount only the files needed for the task, preferably read-only. Place the browser in a container or operating-system sandbox with no access to the host socket. Deny private network ranges unless the task explicitly needs one. Route DNS and HTTP through an allowlist-aware proxy so a page cannot turn a permitted public domain into arbitrary egress.

```mermaid
flowchart LR
  U[Task request] --> P[Policy engine]
  P --> C[Browser controller]
  C --> B[Disposable browser context]
  B --> O[Observation redactor]
  O --> M[Agent model]
  M --> A[Proposed action]
  A --> P
  B --> N[Network proxy]
  N --> W[Allowed web origins]
  classDef trust fill:#dbeafe,stroke:#2563eb,color:#111827
  classDef danger fill:#fee2e2,stroke:#dc2626,color:#111827
  classDef guard fill:#dcfce7,stroke:#16a34a,color:#111827
  class U,M trust
  class B,N guard
  class W danger
```

The controller records a structured event for every action: run ID, browser context, observed page hash, action type, target description, policy decision, and result. Do not record raw cookies or unredacted form values. A screenshot is useful for debugging, but it can contain personal data, so retention and access need the same care as application logs.

## Real-world applications and constraints

A procurement agent may compare public product pages and assemble a draft cart. It can read pages in a disposable context, but submitting an order should require a human approval and a fresh price check. A support agent may navigate a ticket portal, but its session should be scoped to tickets assigned to a queue. A research agent may download public papers, but downloaded files should be scanned and stored outside the browser's executable path.

The constraints are practical. Isolation adds startup latency, and a new context may require a login handoff. Strict network allowlists break sites that load assets from several content-delivery domains. Accessibility-tree extraction can omit information rendered only on canvas. Screenshots increase storage cost. A credential broker must handle expiry, multi-factor authentication, and the possibility that a page tries to make the model reveal a secret. These are reasons to expose controlled fallbacks, not reasons to remove the boundary.

## Mental model

Think of the browser as a remote, untrusted device. The model is an operator who can request actions, not a process that owns the device. The controller is a typed RPC gateway. The policy engine is a reference monitor: every sensitive action passes through it, and a “yes” from an earlier step is not permanent authorization. The proxy is an egress firewall. The disposable profile is a lease that expires.

The most important distinction is between data and authority. Page text can say “upload your secrets,” but that text has no authority. A button can be labelled “confirm,” but the policy engine must classify the underlying effect. Conversely, a policy may allow a click but deny the resulting navigation if it leaves the approved origin. Model confidence is evidence for triage; it is not an access-control decision.

## What changed this month

The July learning map treats browser sandboxing as a foundational control for computer-use systems. The month-specific connection is an engineering inference from the rise of agents that combine visual observation with tool actions: as the action loop becomes more capable, browser isolation and explicit authority become part of the application architecture rather than an optional test harness. This article does not assert an unverified July product release.

## Engineering consequence

Define a browser task contract before writing prompts. It should specify origins, methods, data classes, maximum duration, download rules, upload rules, and approval points. Represent each action as a typed object, for example `click(locator, expected_origin, risk_class)`, rather than passing arbitrary JavaScript to the page. Keep JavaScript execution disabled for ordinary tasks; if a specialized task needs it, place it in a separate capability with a distinct approval and audit stream.

Use state transitions such as `created`, `running`, `awaiting_approval`, `blocked`, `completed`, and `expired`. A timeout must destroy the context and revoke brokered credentials. If the controller loses connection after a click, mark the effect as unknown and reconcile by reading the page or asking an operator; blindly retrying may duplicate a purchase or message.

```mermaid
sequenceDiagram
  participant R as Run service
  participant G as Guard
  participant C as Controller
  participant B as Browser
  participant H as Human
  R->>G: propose action with origin and risk
  G-->>R: allow, deny, or approval_required
  alt allowed
    R->>C: execute typed action
    C->>B: click/type/navigate
    B-->>C: result and page state
    C-->>R: signed event receipt
  else sensitive
    R->>H: show redacted preview
    H-->>G: approve once for this effect
    G->>C: issue short-lived grant
    C->>B: execute single action
    B-->>R: result or unknown outcome
  else denied
    G-->>R: block and retain evidence
  end
```

Testing should include hostile page content, unexpected redirects, popups, cross-origin frames, downloads with misleading names, expired sessions, and controller restarts. The test oracle is not merely “the model refused.” It is that the browser had no prohibited capability even when the model requested it. Run these tests against the same container, proxy, and credential configuration used in production.

## Limits and failure modes

Site isolation is not equivalent to application-level authorization. A browser may isolate renderer processes while the logged-in account still has too much business permission. A container reduces host exposure but does not repair a vulnerable application. Network blocking may be bypassed if an approved origin provides an open redirect or server-side fetch feature. Redaction can miss secrets rendered as images. Accessibility metadata can include hidden or off-screen text. Downloads can be polyglots or archives containing dangerous content.

Prompt injection remains possible inside a strong sandbox. The model may waste time, leak task data to an approved site, or make an allowed but incorrect change. Therefore pair isolation with narrow account scopes, confirmation for irreversible effects, rate limits, and post-action verification. Treat every browser context as disposable after a suspicious event. Preserve only the minimum evidence needed for diagnosis.

Credential brokering deserves its own boundary. The controller should request a named capability, such as “read invoices for tenant A,” instead of receiving a reusable password. A broker can mint a short-lived session or complete a narrowly scoped login flow, then return only a success signal. If a page asks the model to paste a token into a text area, the action should be denied because the destination and purpose are not the brokered capability. This design also makes revocation practical: expire the grant when the run ends, when the origin changes, or when the policy version is replaced.

Origin changes must be treated as security events, not ordinary navigation. A redirect from `shop.example.test` to a payment provider may be legitimate, but it changes who receives data and which account is in use. Require an explicit policy edge for that transition, show the new origin to an operator for high-risk tasks, and clear any page-derived assumptions after navigation. Keep a per-run origin history so an investigator can distinguish an expected redirect from a malicious chain.

Evidence retention has a similar trade-off. Store action metadata, policy inputs, and hashes of observations by default. Keep screenshots or DOM snapshots only when they are needed for a short investigation, encrypt them, restrict access, and expire them on a documented schedule. An audit trail that captures every keystroke may itself become a sensitive data store. The goal is to prove what authority was granted and what effect was attempted, not to create a second copy of every customer record.

## Mini exercise (15–30 min)

Build a local policy simulator that receives JSON actions and decides whether they are allowed. Include an origin allowlist, a `read` versus `write` risk class, a download rule, and an approval requirement for writes. Add test cases for an allowed page read, a redirect to an unapproved origin, a credential request, and a duplicate write. Extend the simulator so every decision produces an event without storing the supplied secret value.

## Build it locally

The following dependency-free example models a policy gateway. It does not launch a browser and is intentionally low-cost: the lesson is the decision boundary, not a production sandbox.

```python
from dataclasses import dataclass
from urllib.parse import urlparse

@dataclass(frozen=True)
class Action:
    kind: str
    url: str
    risk: str
    has_secret: bool = False

ALLOWED_HOSTS = {"docs.example.test", "shop.example.test"}

def decide(action: Action, approved: bool = False) -> str:
    host = urlparse(action.url).hostname
    if host not in ALLOWED_HOSTS:
        return "DENY: origin"
    if action.has_secret:
        return "DENY: secret exposure"
    if action.risk == "write" and not approved:
        return "APPROVAL_REQUIRED"
    if action.kind == "download" and action.risk != "read":
        return "DENY: download policy"
    return "ALLOW"

cases = [
    Action("read", "https://docs.example.test/guide", "read"),
    Action("navigate", "https://evil.test/redirect", "read"),
    Action("type", "https://shop.example.test/checkout", "write", True),
    Action("click", "https://shop.example.test/checkout", "write"),
]
for case in cases:
    print(case.kind, decide(case))
```

Numbered implementation steps:

1. Copy the program into `sandbox_policy.py` and run it with Python 3. The output should contain `ALLOW`, an origin denial, a secret denial, and an approval request.
2. Add a `redirected_from` field and deny a destination unless both the original and destination hosts are allowed.
3. Add an action ID and retain a set of used IDs so a retry cannot repeat a write without reconciliation.
4. Replace the hard-coded host set with a policy object loaded at run creation; do not let page text modify it.
5. Write tests for malformed URLs, internationalized hostnames, empty schemes, and an approval that expires after one action.

## Interview Q&A

**Why is a browser container insufficient?** A container limits some host access, but it does not decide which website the account may modify, which network destinations are reachable, or whether a click is financially consequential. Those controls belong to policy and identity layers.

**Why re-check an action after the model proposes it?** The page can change after observation, and a locator may resolve to a different element. Just-in-time checks bind authorization to the actual origin, effect, and current state.

**Should an agent use the user’s existing browser profile?** Usually no. A disposable profile prevents unrelated cookies, extensions, history, and local files from becoming ambient authority. A brokered, task-scoped session is safer.

**How do you handle a lost connection after a click?** Record an unknown outcome, stop automatic retries, and reconcile through a safe read or human confirmation. Exactly-once browser effects cannot be assumed.

**What should be measured?** Measure blocked prohibited actions, approval rate, policy false positives, context startup latency, proxy denials, unknown outcomes, and verified business success. Model confidence alone is not a security metric.

## Glossary

- **Ambient authority:** Access a process receives merely because it runs in a user context.
- **Capability:** A narrowly scoped permission to perform one class of action.
- **Egress:** Traffic leaving the sandbox toward another network destination.
- **Reference monitor:** A component that mediates every protected operation.
- **Same-origin policy:** A browser rule separating scripts and data across origins.
- **Site isolation:** Separating site content into processes to reduce cross-site compromise impact.
- **Disposable profile:** A temporary browser profile destroyed after a task.
- **Prompt injection:** Untrusted content attempting to steer an agent's instructions or actions.

## References

- [Chromium Security — Site Isolation](https://www.chromium.org/Home/chromium-security/site-isolation/) — primary platform-security documentation.
- [W3C — WebDriver](https://www.w3.org/TR/webdriver2/) — standards-track browser automation interface.
- [OWASP — Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — secondary risk taxonomy for agent systems.

## Claim ledger

| Claim | Source | Fact or inference |
|---|---|---|
| Same-origin policy separates web origins | Chromium Security; W3C | Source-context fact |
| WebDriver provides a standardized automation boundary | W3C WebDriver | Source-context fact |
| Agent page content should be treated as untrusted input | OWASP risk taxonomy | Engineering interpretation |
| A disposable profile reduces ambient credential exposure | None; derived from least privilege | Engineering inference |
| Action authorization should be checked immediately before execution | None; derived from changing UI state | Engineering inference |
| Isolation must be paired with account scoping and approval | None; defense-in-depth design | Engineering inference |
