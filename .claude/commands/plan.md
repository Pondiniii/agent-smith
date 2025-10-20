# /plan

Jednolita komenda planowania nowego projektu implementacji. Zbiera wymagania i tworzy ujednolicony **PLAN.md** zawierający całą zawartość.

## Cel
Jeden punkt wejścia który przepytuje użytkownika, zbiera wymagania (cel, sukces, zakres, ograniczenia), generuje kompletny **PLAN.md** i zapisuje do `jobs/scheduled/`, gotowy do wykonania.

## Przepływ

### Faza 1: Wywiad Discovery
1. Zapytaj o nazwę projektu/zadania i slug (np. "user-auth" z "User Authentication")
2. Jaki jest główny cel? Jaki problem rozwiązujemy?
3. Jak wygląda sukces? (mierzalne rezultaty - co będzie oznaczać że gotowe)
4. Co jest w zakresie vs poza zakresem?
5. Jakieś ograniczenia, zależności lub ryzyka?
6. Spodziewana oś czasu/priorytet?

### Faza 2: Generowanie PLAN.md
7. Na podstawie odpowiedzi, utwórz **unified PLAN.md** z pełną strukturą:

```markdown
# PLAN — {{ project_name }}

**Slug:** {{ slug }}
**Status:** scheduled
**Utworzono:** {{ timestamp }}
**Priorytet:** {{ priority }}

---

## Cel & Kontekst

{{ goal_description }}

### Problem
{{ problem_description }}

### Wynik Sukcesu
Projekt będzie ukończony gdy:
{{ success_criteria_list }}

---

## Zakres

### W Zakresie
{{ in_scope_items }}

### Poza Zakresem
{{ out_of_scope_items }}

---

## Ograniczenia & Zależności

{{ constraints_and_dependencies }}

---

## Ryzyka & Mitygacja

{{ risks_with_mitigations }}

---

## Fazy Wykonania

### Faza 1: {{ phase_1_name }}
- [ ] {{ task_1_1 }} (agent: {{ agent_type }})
- [ ] {{ task_1_2 }} (agent: {{ agent_type }})
- [ ] Walidacja fazy 1

### Faza 2: {{ phase_2_name }}
- [ ] {{ task_2_1 }} (agent: {{ agent_type }})
- [ ] {{ task_2_2 }} (agent: {{ agent_type }})
- [ ] Walidacja fazy 2

### Faza 3: {{ phase_3_name }} (opcjonalna)
- [ ] {{ task_3_1 }}
...

---

## Punkty Walidacji & Kryteria Ukończenia

- [ ] Testy jednostkowe przechodzą
- [ ] Integracja działa end-to-end
- [ ] Dokumentacja kompletna
- [ ] Nie ma aktywnych blokerów
- [ ] Wszystkie success criteria spełnione

---

## Następne Kroki

Po zatwierdzeniu tego planu:
1. Uruchom: `/implement_this {{ slug }}`
2. Orchestrator przeczyta ten PLAN.md
3. Będzie wykonywać fazy sekwencyjnie
4. Po ukończeniu przeniesie do `jobs/completed/{{ slug }}/`
```

### Faza 3: Przegląd & Potwierdzenie
8. Pokaż wygenerowany PLAN.md użytkownikowi
9. Zapytaj: "**Czy mogę utworzyć plik PLAN.md w `jobs/scheduled/{{ slug }}/`?**"
10. Jeśli użytkownik chce zmian:
    - Iteruj nad PLAN.md
    - Wróć do kroku 8
11. Jeśli użytkownik potwierdzi:
    - Utwórz `jobs/scheduled/{{ slug }}/`
    - Zapisz `PLAN.md`
    - Potwierdź użytkownikowi: "✓ Utworzono jobs/scheduled/{{ slug }}/PLAN.md. Gotowe do `/implement_this {{ slug }}`"

## Struktura Katalogów
```
jobs/scheduled/{{ slug }}/
└── PLAN.md         # Kompletny plan z celem, zakresem, fazami, zadaniami
```

## Reguły
- Wywiad rozmowny ale skoncentrowany (max 5-7 pytań)
- Nie twórz pliku zanim użytkownik potwierdzi
- Slug format: lowercase-with-hyphens
- PLAN.md zawiera wszystko: cel, sukces, zakres, ograniczenia, fazy, zadania
- Każde zadanie powinno mieć przypisanego agenta (coding-agent, docs-agent, itp.)
- Fazy powinny być sekwencyjne i testowalne

## Następne Kroki
Po ukończeniu `/plan`, użytkownik może:
- `/implement_this {{ slug }}` - uruchom orchestrator z tym planem
- Edytować PLAN.md ręcznie przed `/implement_this`
- `/archive {{ slug }}` - przesunąć do jobs/completed

## Przykład Użycia
```
Human: /plan
Agent: Co chcesz zaimplementować? (nazwa projektu)
Human: System logowania użytkowników
Agent: Jaki jest główny cel tego systemu?
Human: Bezpieczne uwierzytelnianie z JWT tokens
Agent: Jak wyglądałaby sytuacja gdy projekt jest gotowy?
Human: Użytkownicy mogą się logować, tokeny są walidowane, sesje się pamiętają
...
Agent: [Pokazuje wygenerowany PLAN.md]
Agent: Czy mogę utworzyć plik PLAN.md w jobs/scheduled/user-login/?
Human: tak
Agent: ✓ Utworzono jobs/scheduled/user-login/PLAN.md
       Gotowe do `/implement_this user-login`
```

## Punkty Integracji
- PLAN.md jest jedynym artefaktem dla job-a
- Orchestrator czyta PLAN.md i wykonuje fazy
- Sub-agenty delegują się na podstawie PLAN.md
- Status job-a śledzony w job-reports/ po `/implement_this`
