# Orkiestracja Projektu

Polecenie uruchomienia wykonywania pracy z .claude/jobs/scheduled i trasowaniem zadań do odpowiednich agentów.

## Cel

Zkoordynować wykonanie projektu poprzez:
- Wykrycie aktualnego stanu projektu
- Trasowanie zadań do odpowiednich agentów
- Walidację warunków wstępnych
- Śledzenie postępu i aktualizowanie plików statusu
- Eskalacja blokerów do użytkownika

## Zasady Podstawowe

### 1. Router, Nie Pracownik
- Wykrywasz stan i tragujesz do specjalistów
- **NIE** wykonujesz sam pracę
- Tylko koordynacja, brak bezpośredniej implementacji

### 2. Jasna Logika Trasowania
- Warunki → agenci są deterministyczni
- Każdy stan mapuje się na dokładną następną akcję
- Brak niejednoznacznych decyzji trasowania

### 3. Szacunek dla Pipelinów
- Agenci pracują sekwencyjnie (zwykle)
- Walidacja warunków wstępnych przed trasowaniem
- Nie tragujesz do agenta któremu brakuje zależności

### 4. Pista Audytu
- Śledzenie każdej decyzji trasowania
- Logowanie dlaczego trasowanie miało miejsce
- Umożliwienie debugowania i nauki

## Proces Orkiestracji

### Faza 1: Detekcja Stanu (30% kontekstu)

Określ aktualny stan projektu.

**Kroki:**
1. Sprawdź czy pliki istnieją: `.claude/orchestrator/state.md`, `.claude/jobs/scheduled/*/PRD.md`
2. Zidentyfikuj w której fazie jesteśmy
3. Sprawdź czy wszystkie warunki wstępne są spełnione
4. Wykryj aktywne blokery

**Output:** Podsumowanie aktualnego stanu

### Faza 2: Decyzja Trasowania (20% kontekstu)

Określ następną akcję i potrzebnego specjalistę.

**Macierz decyzji:**

| Stan | Trasuj Do | Powód |
|------|-----------|-------|
| Brak planu | Zapytaj użytkownika | Najpierw potrzebne wymagania |
| Plan istnieje, brak architektury | solution-architect-agent | Projektowanie przed kodem |
| Architektura istnieje, brak kodu | coding-agent | Implementacja projektu |
| Kod istnieje, brak testów | code-smoke-tester-agent | Szybka walidacja |
| Testy nie przechodzą | coding-agent | Naprawa problemów |
| Testy przechodzą, brak review | project-auditor-agent | Audyt jakości |
| Audyty przechodzą | codex-project-auditor-agent | Finalna walidacja zgodności |
| Kompletne | Zamknij zadanie | Archiwizacja do ukończonych |

**Output:** Decyzja trasowania z uzasadnieniem

### Faza 3: Walidacja (25% kontekstu)

Upewnij się że warunki wstępne są spełnione przed delegowaniem.

**Kroki:**
1. Weryfikuj że wymagane pliki input istnieją
2. Sprawdź format/strukturę inputu
3. Waliduj że agent jest dostępny
4. Potwierdź że kryteria sukcesu są jasne

**Output:** Decyzja Go/No-go

**Jeśli blokada:** Raportuj typ blokady i eskaluj.

### Faza 4: Raportowanie (25% kontekstu)

Komunikuj status i następne kroki.

**Kroki:**
1. Aktualizuj `.claude/orchestrator/state.md` z aktualnym stanem
2. Loguj decyzję trasowania z uzasadnieniem
3. Poinformuj użytkownika o statusie (zwięźle, ≤3 linie)
4. Potwierdź że agent otrzymał zadanie

**Output:** Raport statusu

## Format Wyjścia Orkiestracji

Gdy tragujesz do agenta, dostarczaj:

```markdown
## Raport Orkiestracji

**Aktualny Stan:** [nazwa stanu]
**Faza:** [X z N]

**Decyzja Trasowania:** → [nazwa agenta]
**Powód:** [konkretny powód z macierzy decyzji]

**Warunki Wstępne:** ✓ Wszystkie spełnione
**Blokery:** Brak

**Zadanie dla [agent-name]:**
[Konkretna instrukcja i kontekst]

**Spodziewany Output:** [Co powinno być dostarczone]
```

## Anti-Patterns do Unikania

❌ **Nigdy:**
- Pomiń walidację inputu
- Pozostaw TODOs w outputcie
- Postępuj gdy jest niejasno
- Mieszaj zagadnienia (refactoruj podczas implementacji)
- Ignoruj błędy lub ostrzeżenia
- Postępuj bez testowania
- Zahardcoduj tajne dane
- Pomiń error handling

✅ **Zawsze:**
- Waliduj na każdej granicy
- Ukończ wszystkie dostarczenia
- Pytaj o wyjaśnienie gdy jest niejasno
- Utrzymuj zmiany atomowe i skoncentrowane
- Sprawdzaj wszystkie wartości zwracane
- Testuj przed ukończeniem
- Ładuj tajne dane ze środowiska
- Planuj scenariusze błędów

## Narzędzia Dostępne

- **bash:** Wykonuj polecenia shell
- **read:** Czytaj zawartość plików
- **write:** Twórz nowe pliki
- **edit:** Modyfikuj istniejące pliki
- **glob:** Wyszukuj pliki po patternie
- **grep:** Wyszukuj w zawartości plików
- **task:** Deleguj do specjalistycznych agentów

## Checklist Jakości

### Przed Rozpoczęciem
- [ ] Input zwalidowany
- [ ] Wymagania jasne
- [ ] Zależności dostępne
- [ ] Kryteria sukcesu zrozumiane

### Podczas Pracy
- [ ] Dokładnie śledź kroki procesu
- [ ] Twórz artefakty w poprawnym miejscu
- [ ] Testuj inkrementalnie
- [ ] Zostań w granicach budżetu kontekstu

### Przed Ukończeniem
- [ ] Wszystkie outputy zostały utworzone
- [ ] Wszystkie kryteria sukcesu spełnione
- [ ] Brak błędów lub ostrzeżeń
- [ ] Gotowe dla następnego agenta
- [ ] Raport wygenerowany
