# /plan

Jednolita komenda planowania nowego projektu implementacji. Tworzy PRD + plan poprzez interaktywną sesję.

## Cel
Jeden punkt wejścia który przepytuje użytkownika, tworzy PRD.md i plan zadań, zapisuje do `jobs/scheduled/`, gotowe do wykonania.

## Przepływ

### Faza 1: Wywiad Discovery
1. Zapytaj o nazwę projektu/zadania i slug (np. "user-auth" z "User Authentication")
2. Jaki jest główny cel? Jaki problem rozwiązujemy?
3. Jak wygląda sukces? (mierzalne rezultaty)
4. Co jest w zakresie vs poza zakresem?
5. Jakieś ograniczenia, zależności lub ryzyka?
6. Spodziewana oś czasu/priorytet?

### Faza 2: Generowanie Artefaktów
7. Utwórz strukturę PRD:
   ```markdown
   # PRD — {{ project_name }}

   ## Cel & kontekst
   {{ goal_description }}

   ## Kryteria sukcesu
   - [ ] {{ criterion_1 }}
   - [ ] {{ criterion_2 }}

   ## Zakres
   **W zakresie:**
   - {{ in_scope_items }}

   **Poza zakresem:**
   - {{ out_of_scope_items }}

   ## Ograniczenia & Zależności
   - {{ constraints }}

   ## Ryzyka & Mitygacja
   - {{ risks_with_mitigations }}
   ```

8. Podziel na fazy i zadania:
   ```markdown
   # Plan — {{ project_name }}

   **Status:** zaplanowane
   **Utworzono:** {{ timestamp }}
   **Priorytet:** {{ priority }}

   ## Fazy

   ### Faza 1: {{ phase_name }}
   - [ ] {{ task_1 }} (agent: {{ agent_name }})
   - [ ] {{ task_2 }} (agent: {{ agent_name }})
   - [ ] Walidacja fazy 1

   ### Faza 2: {{ phase_name }}
   ...

   ## Punkty Walidacji
   - [ ] Testy jednostkowe przechodzą
   - [ ] Integracja działa
   - [ ] Dokumentacja kompletna
   ```

### Faza 3: Przegląd & Potwierdzenie
9. Pokaż PRD i plan użytkownikowi
10. Zapytaj: "Czy mogę utworzyć pliki w `jobs/scheduled/{{ slug }}/`?"
11. Jeśli użytkownik chce zmian:
    - Iteruj PRD/plan
    - Wróć do kroku 9
12. Jeśli użytkownik potwierdzi:
    - Utwórz `jobs/scheduled/{{ slug }}/`
    - Zapisz `PRD.md`
    - Zapisz `plan.md`
    - Zapisz `status.md` z metadanymi
    - Potwierdź użytkownikowi: "Utworzono w jobs/scheduled/{{ slug }}. Gotowe do /implement_this"

## Struktura Katalogów
```
jobs/scheduled/{{ slug }}/
├── PRD.md          # Wymagania produktu
├── plan.md         # Podział zadań na fazy
├── status.md       # Bieżący status, metadane
└── README.md       # Szybki przegląd
```

## Reguły
- Wywiad rozmowny ale skoncentrowany (max 5-7 pytań)
- Nie twórz plików zanim użytkownik potwierdzi
- Slug format: lowercase-with-hyphens
- Zawsze twórz status.md z: timestamp utworzenia, priorytet, bieżąca faza
- Wskaż które agenty będą użyte dla każdego typu zadania

## Następne Kroki
Po ukończeniu `/plan`, użytkownik może:
- `/implement_this {{ slug }}` - uruchom orchestrator
- `/edit {{ slug }}` - modyfikuj PRD/plan przed wykonaniem
- `/archive {{ slug }}` - przenieś do jobs/completed

## Przykład Użycia
```
Human: /plan
Agent: Co chcesz zaimplementować? (nazwa projektu)
Human: System logowania użytkowników
Agent: Jaki jest główny cel tego systemu?
Human: Bezpieczne uwierzytelnianie z JWT tokens
...
Agent: [Pokazuje PRD i plan]
Agent: Czy mogę utworzyć pliki w jobs/scheduled/user-login/?
Human: tak
Agent: ✓ Utworzono jobs/scheduled/user-login/
       - PRD.md
       - plan.md
       - status.md
       Gotowe do /implement_this user-login
```

## Punkty Integracji
- Używa szablonów z `.claude/agents/templates/`
- Może delegować do sub-agentów podczas fazy wykonania
- Integruje się z workflow `/implement_this`
- Walidacja CODEX może być dodana do faz planu
