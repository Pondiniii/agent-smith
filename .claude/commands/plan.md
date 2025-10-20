# /plan

Pomóż userowi zaplanować prace dla sub-agentów i rozdzielić duży pomysł projekt na wiele małych króków. Zbiera wymagania i tworzy ujednolicony **PLAN.md** zawierający całą zawartość. Znajduje ryzyka i zagrorzenia.

## Cel
- Przeprowadzić PRD z userem a następnie
Wygenerować plik PLAN.md który zawiera:
- zadania podzielone na PHASE i dużo kroczków i opis jaki krok jaki sub-agent będzie robił
- aplikacja i plan działania musi być zoptymalizowany pod subagentów

# Dostępni Agenci

Każdy agent ma specjalną rolę. Wybieraj je do zadań na podstawie ich specjalizacji:

## Agenty Implementacyjne

- **coding-agent**: Implementacja. Atomowe zadania, czysty kod, testy na bieżąco.
  - Użyj: Pisanie kodu, feature implementation, bug fixes

- **docs-agent**: LLM documentation specialist. Generuje KISS docs dla context efficient restoration.
  - Użyj: Dokumentacja, knowledge base, context restoration files

## Agenty Walidacyjne & QA

- **code-smoke-tester-agent**: Fast smoke tester. Runs quick validation tests (compile and run). Quick feedback loop.
  - Użyj: Szybka walidacja czy program się odpala, smoke tests

- **project-auditor-agent**: Research validator. Weryfikuje czy job naprawdę done czy agenci flying in circles.
  - Użyj: Audit czy phase/projekt skończony, weryfikacja requirements

## Agent Orkiestracyjny

- **orchestrator-agent**: Main orchestrator - routes workflow i deleguje tasks do specialized sub-agents.
  - Użyj: Automatycznie - orkiestruje wszystkie fazy i deleguje do odpowiednich agentów

---

## Przepływ

### Faza 1: Wywiad PRD (Product Definition Review)
1. Jaki jest główny cel? 
2. Jaki problem rozwiązujemy?
3. Jak wygląda sukces? (mierzalne rezultaty - co będzie oznaczać że gotowe)
4. Co jest w zakresie vs poza zakresem?
5. Jakieś ograniczenia, zależności lub ryzyka?
6. Jasno zdefiniowanie kryteria akceptacji
7. plan testów
8. dopytuj lub proponuj tech stack.


### Faza 2: Generowanie PLAN.md
Gdy już poznasz wymagania i przeprowadzisz wywiad z userem i będziesz dosyć pewien. Zapytaj usera czy mogę napisać PLAN.md?

Na podstawie odpowiedzi, utwórz **PLAN.md** z pełną strukturą:

```markdown
# PLAN — {{ project_name }}

---

## Cel & Kontekst

### Problem

### Wynik Sukcesu

---

## Zakres

### W Zakresie

### Poza Zakresem

---

## Ograniczenia & Zależności

---

## Ryzyka & Mitygacja

---

## Fazy Wykonania

### Faza 1: {{ phase_1_name }}
- [ ] {{ task_1_1 }} (agent: {{ agent_type }})
- [ ] {{ task_1_2 }} (agent: {{ agent_type }})
- [ ] Walidacja fazy 1 {{ agent_type }} 

### Faza 2: {{ phase_2_name }}
- [ ] {{ task_2_1 }} (agent: {{ agent_type }})
- [ ] {{ task_2_2 }} (agent: {{ agent_type }})
- [ ] Walidacja fazy 2 {{ agent_type }}

### Faza 3: {{ phase_3_name }}
- [ ] {{ task_3_1 }} {{ agent_type }})
- Walidacja fazy 3 {{ agent_type }}

Finalna Walidacja walidacja całego projektu {{ agent_type }}
...

---

## Punkty Walidacji & Kryteria Ukończenia
Wyspecjalizowane agenty do walidacji: project-auditor-agent
sprawdza czy phase lub cały projekt został wykonany.
Wszystkie success criteria spełnione.

---

## Struktura Katalogów
```
.claude/job/
└── PLAN.md         # Kompletny plan z celem, zakresem, fazami, zadaniami
```

## Reguły
- Nie twórz pliku zanim użytkownik potwierdzi
- PLAN.md zawiera wszystko: cel, sukces, zakres, ograniczenia, fazy, zadania i więcej jeśl uważasz za słuszne.
- Każde zadanie powinno mieć przypisanego agenta (coding-agent, docs-agent, itp.)
- Fazy powinny być sekwencyjne i testowalne
- Pamiętasz rozbijasz wielki projekt na wiele małych kroczków aby agenci sobie mogli na spokojnie poradzić przez ogromny projekt.

## Następne Kroki
Po ukończeniu `/plan`, użytkownik może:
- `/implement_this {{ slug }}` - uruchom orchestrator z tym planem
- Edytować PLAN.md ręcznie przed `/implement_this`

## Punkty Integracji
- PLAN.md jest jedynym artefaktem dla job-a
- Orchestrator czyta PLAN.md i wykonuje fazy
- Sub-agenty delegują się na podstawie PLAN.md
