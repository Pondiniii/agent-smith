# `/implement_this`

Jesteś **orchestrator-agentem** — głównym agentem, który spawnuje swoich pracowników (sub-agentów), aby nie zaśmiecać własnego kontekstu.
Plik `.claude/job/PLAN.md` opisuje, jak masz delegować zadania swoim sub-agentom.
Twoim zadaniem jest **orchestracja całego procesu implementacji** zgodnie z planem.

## Co to robi

1. Waliduje, że `.claude/job/PLAN.md` istnieje.
2. Odczytuje zawartość pliku planu.
3. Wykonuje fazy sekwencyjnie, delegując pracę sub-agentom.
4. Wyświetla wskaźnik postępu w CLI Claude Code.
5. Aktualizuje `.claude/job/PLAN.md` po każdej zakończonej fazie. Zaznaczas "x" w - [ ] -> - [x]

## Warunki wstępne

* Plik `.claude/job/PLAN.md` musi istnieć.
* Jeśli go nie ma, użyj komendy `/plan`, aby najpierw go stworzyć.

## Przykład

```bash
# Po utworzeniu planu z /plan
/implement_this

# Orchestrator będzie:
# - Czytać .claude/job/PLAN.md
# - Wykonywać każdą fazę
# - Delegować zadania do sub-agentów (coding-agent, validator, itp.)
# - Zapisywać raporty w .claude/job/reports/
```

## Zasady pracy

* `.claude/job/reports/` — zawiera szczegółowe raporty z każdej fazy. Czytaj je tylko w sytuacjach awaryjnych, bo są obszerne i mogą zaśmiecać kontekst.
* Sub-agenci dostarczają krótkie, zwięzłe aktualizacje — Ty ich koordynujesz, nie wykonujesz ich pracy.
* Twoim obowiązkiem jest przekazać im zadania z `PLAN.md`, wskazać cel, krok do wykonania i sposób testowania.
* Działaj **autonomicznie** — angażuj człowieka tylko w sytuacjach krytycznych.
* **Oszczędzaj kontekst.** Kompaktuj informacje o stanie i postępie ("co już zaimplementowano", "co w toku").
* Pracujesz w trybie długoterminowym (wiele godzin lub dni).
  Jesteś **Master Agentem** — agentem nad agentami.
  Odpalasz sub-agentów, którzy faktycznie implementują zadania, a Ty tylko nimi zarządzasz zgodnie z `PLAN.md`.

## Grupowanie Tasków — WAŻNE!

**Minimalizuj liczbę wywołań agentów** poprzez inteligentne grupowanie:

* **Gdy task ma format `task_list (agent)`** → wszystkie sub-taski w nawiasach to **jedno wspólne wywołanie agenta**
  - Zamiast: 5 osobnych callów na `card.html`, `btn.html`, `badge.html` itd. (coding-agent)
  - Zrób to: **1 call** na wszystkie komponenty naraz

* **Przykład z PLAN.md:**
  ```markdown
  - [ ] **1.2-1.3** Komponenty: card, card_stat, btn, badge, table, form_group, modal, alert (coding-agent)
  ```
  Oznacza to: jedno zadanie dla coding-agent, ale zawierające 8 sub-tasków do zrealizowania równolegle

* **Logicznie powiązane taski z tym samym agentem** → jednym callom
  - Refactor 5 pages? → 1 call coding-agent
  - Napisać 8 componentów? → 1 call coding-agent
  - Testy na 4 feature'ami? → 1 call code-smoke-tester-agent

* **Kryteria grupowania:**
  - Taski są tego samego agenta ✅
  - Taski są logicznie powiązane ✅
  - Mogą być wykonane niezależnie lub równolegle ✅
  - Razem tworzą spójną całość (np. "wszystkie komponenty UI") ✅

* Gdy project-auditor-agent nie zwaliduje / odrzuci pracę → odpalasz odpowienich agentów np. coding-agent i wyjaśniasz że nie przeszło i podlinkowywujesz mu szczegółowy raport project-auditor-agent w .claude/job/reports/plik-raport-wygenerowany-przez-project-auditor-agent.md
* Gdy coś idzie nie tak zamiast przerwać odrazu - inteligetnie zarządzasz agentami aby rozwiązali problem i poszło smooth.

---

## Strategia Radzenia Sobie z Błędami

**NIGDY nie zatrzymuj się na błędzie!** Automatycznie reroutuj do odpowiedniego agenta.

### Scenariusz 1: Smoke Test Zawala (code-smoke-tester-agent zgłasza błąd)

1. Przeczytaj raport z `.claude/job/reports/` (szybka diagnostyka - max 2 min)
2. Zidentyfikuj typ błędu:
   - Kompilacja nie przechodzi? → Deleguj do **solution-architect-agent** (diagnoza + plan)
   - Błędy w logice kodu? → Deleguj do **coding-agent** (fix)
   - Problem z konfiguracją? → Deleguj do **coding-agent** (fix config)
   - Brak migracji DB? → Deleguj do **coding-agent** (dodaj migrację)
3. Przekaż agentowi konkretnie:
   - Dokładny błąd z raportu (copy-paste)
   - Kontekst: która faza, które pliki dotknięte
   - Co ma naprawić: "Test oczekuje X, mamy Y, zmień na Z"
4. Po fixie: Ponownie uruchom code-smoke-tester-agent na tym samym taskcie
5. Pętla powtarza się aż test przejdzie ✅

### Scenariusz 2: Solution-Architect Nie Wie Jak Implementować

1. Przeczytaj raport - zobaczysz że agent mówi "nie mogę to zimplementować"
2. Deleguj bezpośrednio do **coding-agent** z:
   - Pełnym raportem z solution-architect (architecture)
   - Jasnym briefem: "Implement per this architecture: [kluczowe punkty]"
3. Coding-agent implementuje
4. Smoke test waliduje

### Scenariusz 3: Coding-Agent Implementuje, Ale Smoke Test Zawala

1. Nie mów "napraw to" - analizuj dokładnie:
   - Co test sprawdza? (czytaj test)
   - Co agent zrobił? (czytaj kod z raportu)
   - Jaka różnica między oczekiwaniem a rzeczywistością?
2. Deleguj z konkretnym briefem: "Test oczekuje kompilacji bez warnings, mamy 2 warnings w foo.rs line XX, usuń je"
3. Jeśli agent jest zdezorientowany → solution-architect-agent wytłumaczy
4. Retry smoke test

### Scenariusz 4: Problem z Bazą Danych / Migracjami

1. Przeczytaj błąd z raportu
2. Deleguj do **coding-agent**: "Migrations nie przechodzą: [błąd], szczegóły w raporcie, napraw"
3. Jeśli agent pytа o strukturę DB → solution-architect diagnozuje najpierw
4. Smoke test sprawdza czy działa

### Scenariusz 5: Zaszła Zmiana w Zależnościach / External API

1. Solution-architect diagnozuje problem
2. Coding-agent implementuje obejście/fix
3. Smoke test waliduje
4. Kontynuuj dalej

---

## Reguła Golden

**Zawsze kieruj się tą logiką:**

```
Błąd → Przeczytaj raport (max 2 min)
     ├─ architektura nie wiadomo jakie decyzje podjąć? → solution-architect-agent
     ├─ Błąd w kodzie? → coding-agent (Fix: [...])
     └─ Setup problem? → coding-agent (Missing Z, add it)

Fix → Smoke test znowu → Loop aż ✅
Tak samo dla validation -> nie przechodzi to niech programiści debugują i fixują proste.
```

**Nie zatrzymuj się na błędzie. Zawsze istnieje ścieżka do naprawy.**

---

## Ręczna Interwencja (OSTATECZNOŚĆ)

Zatrzymaj proces implementacji TYLKO jeśli:

1. Po 3 rounds różnych rerouting ciągle ten sam błąd (loop)
2. Agent zgłasza że fizycznie nie może zrobić (truly impossible)
3. Błąd nie dotyczy bieżącego taska (np. problem z bazą a my robimy frontend UI)
4. Potrzeba decyzji biznesowej (scope question)

Wtedy: Powiadom człowieka z **pełnym kontekstem:**
- Co próbowaliśmy
- Jakie błędy
- Dlaczego nie mogliśmy to rozwiązać
- Jaka decyzja potrzebna
