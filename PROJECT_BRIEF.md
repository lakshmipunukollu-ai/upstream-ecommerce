# PROJECT BRIEF
# (Extracted from MASTER_PROJECT_PLAYBOOK.md — your section only)

## SENIOR ENGINEER DECISIONS — READ FIRST

Before any code is written, here are the opinionated decisions made across all 9 projects
and why. An agent should never second-guess these unless given new information.

### Stack choices made
| Project | Backend | Frontend | DB | Deploy | Rationale |
|---------|---------|---------|-----|--------|-----------|
| FSP Scheduler | TypeScript + Node.js | React + TypeScript | PostgreSQL (multi-tenant) | Azure Container Apps | TS chosen over C# — same Azure ecosystem, better AI library support, faster iteration |
| Replicated | Python + FastAPI | Next.js 14 | PostgreSQL + S3 | Docker | Python wins for LLM tooling; Next.js for real-time streaming UI |
| ServiceCore | Node.js + Express | Angular (required) | PostgreSQL | Railway | Angular required — clean REST API behind it |
| Zapier | Python + FastAPI | None (API only + optional React dashboard) | PostgreSQL + Redis | Railway | Redis for event queue durability; Python for DX-first API |
| ST6 | Java 21 + Spring Boot | TypeScript micro-frontend (React) | PostgreSQL | Docker | Java required — Spring Boot is the senior choice; React micro-frontend mounts into PA host |
| ZeroPath | Python + FastAPI | React + TypeScript | PostgreSQL | Render | Python for LLM scanning logic; React for triage dashboard |
| Medbridge | Python + FastAPI + LangGraph | None (webhook-driven) | PostgreSQL | Railway | LangGraph is the correct tool for state-machine AI agents |
| CompanyCam | Python + FastAPI | React + TypeScript | PostgreSQL | Render | Python for CV/ML inference; React for annotation UI |
| Upstream | Django + DRF | React + TypeScript | PostgreSQL | Render | Django for rapid e-commerce scaffolding; built-in admin is a bonus |

### The 4 shared modules — build these FIRST
These are the highest ROI pieces of work. Build them once, copy-scaffold into every project.

1. `shared/llm_client.py` — Claude API wrapper with retry, streaming, structured output parsing
2. `shared/auth/` — JWT auth + role-based guards (Python + TypeScript versions)
3. `shared/state_machine.py` — Generic FSM: states, transitions, guards, event log
4. `shared/queue/` — Job queue pattern: enqueue, dequeue, ack, retry (Redis + Postgres fallback)

### Build order (wave system)
**Wave 0 (Day 1):** Build shared modules. All other waves depend on these.
**Wave 1 (Days 2-3):** Zapier + ZeroPath — establish LLM pipeline + REST API patterns
**Wave 2 (Days 4-5):** Medbridge + Replicated — LLM pipeline variants, more complex AI
**Wave 3 (Days 6-8):** FSP + ST6 — complex business logic, approval flows
**Wave 4 (Days 9-11):** ServiceCore + Upstream + CompanyCam — isolated stacks, finish strong

---

## PROJECT 9: UPSTREAM LITERACY — E-COMMERCE CHECKOUT SYSTEM
**Company:** Upstream Literacy | **Stack:** Django + DRF + React + TypeScript + PostgreSQL + Stripe

### Company mission to impress
Upstream Literacy gets literacy curriculum into schools. Their customers are school
districts and administrators buying educational materials. What will impress them: a clean,
accessible e-commerce experience that could actually serve a school district, with proper
order management and inventory tracking. The AI-accelerated angle: smart product recommendations
based on district demographics and purchase history.

### Architecture
```
Render
├── api (Django 5 + DRF)
│   ├── /api/products/           — catalog with categories, images, descriptions
│   ├── /api/cart/               — add/update/remove, persistent session
│   ├── /api/checkout/           — Stripe payment intent creation
│   ├── /api/orders/             — order status, history, email confirmation
│   ├── /api/inventory/          — stock levels, low-stock alerts
│   ├── /api/accounts/           — registration, login, JWT
│   └── /api/recommendations/   — AI: product recommendations (Claude API)
└── storefront (React + TypeScript)
    ├── Catalog                  — grid/list, filter by grade level, category
    ├── ProductDetail            — description, availability, add to cart
    ├── Cart                     — persistent, quantity updates
    ├── Checkout                 — Stripe Elements, guest + registered flow
    ├── OrderHistory             — tracking, reorder
    └── AdminDashboard           — inventory, orders (Django admin + custom views)
```

### The AI angle — smart curriculum recommendations
```python
class CurriculumRecommendationEngine:
    """
    AI-accelerated angle: recommend curriculum based on district profile.
    Upstream serves schools — their purchasing decisions are driven by
    district demographics (size, free/reduced lunch %, ELL population).
    Claude can reason about curriculum fit in a way a rule-based system can't.
    """
    
    async def recommend(
        self,
        district_profile: DistrictProfile,
        purchase_history: list[Order],
        current_cart: Cart,
    ) -> list[ProductRecommendation]:
        
        prompt = f"""You are a curriculum consultant for K-12 literacy education.
        
District profile: {district_profile.model_dump_json()}
Previous purchases: {[o.items for o in purchase_history]}
Current cart: {current_cart.items}

Recommend 3-5 additional literacy products that would complement their current selection.
Consider:
- Grade levels not yet covered
- ELL student percentage (bilingual materials if > 20%)
- Free/reduced lunch % (accessible pricing, intervention programs)
- Prior purchases (avoid duplicates, suggest natural progressions)

Return JSON with: product_id, reason (1 sentence), confidence (0-1), grade_levels_served"""
        
        result = await self.claude_client.complete(prompt, model="claude-sonnet-4-20250514")
        return self.parse_recommendations(result)
```

### Django models — clean and production-ready
```python
class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    grade_levels = models.JSONField(default=list)  # ["K", "1", "2", "3"]
    images = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [models.Index(fields=['category', 'is_active'])]

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
    
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)  # guest checkout
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    stripe_payment_intent = models.CharField(max_length=200, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### CLAUDE.md for Upstream agent
```
You are a senior Django + React engineer building an e-commerce platform for Upstream Literacy.

COMPANY MISSION: Get high-quality literacy curriculum into K-12 classrooms efficiently.
Their customers are school districts and administrators — not typical consumers.
The checkout experience should feel professional and trustworthy, not generic.

AI ANGLE (AI-Accelerated category): Product recommendations based on district profile.
Claude API recommends curriculum based on: grade coverage gaps, ELL %, demographics, purchase history.
This is the differentiating feature — make it real, not just a "you might also like" widget.

PAYMENT: Stripe Elements for frontend, payment intent on backend. Support guest checkout.
INVENTORY: Track stock levels, decrement on order, alert on low stock.
ACCESSIBILITY: This serves educational institutions — WCAG 2.1 AA compliance matters.

NEVER: Commit Stripe secret keys, skip order confirmation emails, skip guest checkout
ALWAYS: Optimistic cart updates, idempotent order creation, proper Stripe webhook handling
```

---

## SHARED MODULES — BUILD THESE IN WAVE 0

### shared/llm_client.py
```python
"""
Shared Claude API client. Used by: Replicated, ZeroPath, Medbridge, CompanyCam, FSP, Upstream.
Copy this file into each Python project that needs it.
"""
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
import json

client = anthropic.Anthropic()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def complete(
    prompt: str,
    system: str = "",
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 4096,
    as_json: bool = False,
) -> str | dict:
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    text = message.content[0].text
    if as_json:
        # Strip markdown fences if present
        clean = text.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(clean)
    return text

async def analyze_image(
    image_b64: str,
    prompt: str,
    system: str = "",
    model: str = "claude-sonnet-4-20250514",
) -> dict:
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}},
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return json.loads(message.content[0].text)
```

### shared/auth.py (Python version)
```python
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(user_id: str, role: str) -> str:
    return jwt.encode(
        {"sub": user_id, "role": role, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY, algorithm=ALGORITHM
    )

def require_role(*roles: str):
    def dependency(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("role") not in roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    return dependency

# Usage: @router.get("/admin", dependencies=[Depends(require_role("admin", "manager"))])
```

### shared/state_machine.py
```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable
from datetime import datetime

S = TypeVar('S')  # State type
E = TypeVar('E')  # Event type

@dataclass
class Transition(Generic[S, E]):
    from_state: S
    event: E
    to_state: S
    guard: Callable | None = None  # optional condition function

class StateMachine(Generic[S, E]):
    def __init__(self, initial: S, transitions: list[Transition]):
        self.state = initial
        self._transitions = {(t.from_state, t.event): t for t in transitions}
        self._log: list[dict] = []

    def transition(self, event: E, context: dict = None) -> S:
        key = (self.state, event)
        t = self._transitions.get(key)
        if not t:
            raise ValueError(f"Invalid transition: {self.state} + {event}")
        if t.guard and not t.guard(context or {}):
            raise ValueError(f"Guard failed: {self.state} + {event}")
        prev = self.state
        self.state = t.to_state
        self._log.append({"from": prev, "event": event, "to": self.state, "at": datetime.utcnow().isoformat()})
        return self.state

    @property
    def history(self) -> list[dict]:
        return self._log.copy()
```

---

## MASTER CHECKLIST

### Wave 0 — Shared infrastructure
- [ ] `shared/llm_client.py` — Claude API wrapper with retry
- [ ] `shared/auth.py` — JWT + role guards (Python)
- [ ] `shared/auth.ts` — JWT + role guards (TypeScript)
- [ ] `shared/state_machine.py` — generic FSM
- [ ] `shared/queue/` — Redis job queue pattern

### Wave 1 — Establish patterns
- [ ] **Zapier**: FastAPI + Redis + PostgreSQL, /events, /inbox, retry worker, OpenAPI docs
- [ ] **ZeroPath**: FastAPI + React, repo cloner, LLM scanner, triage UI, deduplication

### Wave 2 — LLM complexity
- [ ] **Medbridge**: LangGraph agent, phase router, safety guard, 5 tools, all phases
- [ ] **Replicated**: Bundle extractor, signal extraction, LLM analysis, Next.js streaming UI

### Wave 3 — Business logic
- [ ] **FSP**: Multi-tenant API, 4 agent types, approval queue UI, rationale objects, FSP API integration
- [ ] **ST6**: Java state machine, Spring Boot API, React micro-frontend, Module Federation, manager dashboard

### Wave 4 — Isolated stacks
- [ ] **ServiceCore**: Angular dashboard, clock in/out, overtime calc, AI anomaly detection, approval flow
- [ ] **Upstream**: Django e-commerce, Stripe, inventory, AI curriculum recommendations, guest checkout
- [ ] **CompanyCam**: Two-stage CV pipeline, YOLO + Claude Vision, annotation UI, correction loop

---

## HOW TO USE THIS DOCUMENT WITH AN AGENT

### Starting a new project
```
Read MASTER_PROJECT_PLAYBOOK.md completely.
You are working on [PROJECT_NAME] for [COMPANY].
Your current task: [specific task].
All architecture decisions are already made — do not re-decide them.
Follow the CLAUDE.md instructions at the bottom of each project section.
When done, update .agent_status.json.
```

### Referencing shared modules
```
Read MASTER_PROJECT_PLAYBOOK.md.
Copy the shared/llm_client.py module into this project's src/ directory.
Then implement [specific feature] that uses it.
```

### Starting a new wave
```
Read MASTER_PROJECT_PLAYBOOK.md.
Wave [N] is starting. Begin with [PROJECT_NAME].
Stack: [stack from table at top].
Build the project skeleton first using 01_scaffold.sh, then implement the core feature.
```

## SHARED MODULES — BUILD THESE IN WAVE 0

### shared/llm_client.py
```python
"""
Shared Claude API client. Used by: Replicated, ZeroPath, Medbridge, CompanyCam, FSP, Upstream.
Copy this file into each Python project that needs it.
"""
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
import json

client = anthropic.Anthropic()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def complete(
    prompt: str,
    system: str = "",
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 4096,
    as_json: bool = False,
) -> str | dict:
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    text = message.content[0].text
    if as_json:
        # Strip markdown fences if present
        clean = text.strip()
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(clean)
    return text

async def analyze_image(
    image_b64: str,
    prompt: str,
    system: str = "",
    model: str = "claude-sonnet-4-20250514",
) -> dict:
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}},
                {"type": "text", "text": prompt},
            ],
        }],
    )
    return json.loads(message.content[0].text)
```

### shared/auth.py (Python version)
```python
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(user_id: str, role: str) -> str:
    return jwt.encode(
        {"sub": user_id, "role": role, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY, algorithm=ALGORITHM
    )

def require_role(*roles: str):
    def dependency(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("role") not in roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    return dependency

# Usage: @router.get("/admin", dependencies=[Depends(require_role("admin", "manager"))])
```

### shared/state_machine.py
```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Callable
from datetime import datetime

S = TypeVar('S')  # State type
E = TypeVar('E')  # Event type

@dataclass
class Transition(Generic[S, E]):
    from_state: S
    event: E
    to_state: S
    guard: Callable | None = None  # optional condition function

class StateMachine(Generic[S, E]):
    def __init__(self, initial: S, transitions: list[Transition]):
        self.state = initial
        self._transitions = {(t.from_state, t.event): t for t in transitions}
        self._log: list[dict] = []

    def transition(self, event: E, context: dict = None) -> S:
        key = (self.state, event)
        t = self._transitions.get(key)
        if not t:
            raise ValueError(f"Invalid transition: {self.state} + {event}")
        if t.guard and not t.guard(context or {}):
            raise ValueError(f"Guard failed: {self.state} + {event}")
        prev = self.state
        self.state = t.to_state
        self._log.append({"from": prev, "event": event, "to": self.state, "at": datetime.utcnow().isoformat()})
        return self.state

    @property
    def history(self) -> list[dict]:
        return self._log.copy()
```

---
