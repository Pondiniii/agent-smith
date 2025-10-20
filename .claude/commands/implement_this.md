# /implement_this

Wykonaj zaplanowane zadanie używając agenta orchestrator.

## Użycie
```
/implement_this <job-slug>
```

## Co To Robi

1. Waliduje że `jobs/scheduled/<job-slug>/` istnieje
2. Uruchamia **agenta orchestrator** z kontekstem zadania
3. Orchestrator czyta PRD.md i plan.md
4. Wykonuje fazy sekwencyjnie delegując do sub-agentów
5. Śledzi postęp w status.md
6. Po ukończeniu przenosi zadanie do `jobs/completed/`

## Warunki Wstępne

- Zadanie musi istnieć w `jobs/scheduled/<job-slug>/`
- Musi zawierać `PRD.md` i `plan.md`
- Użyj `/plan` żeby najpierw stworzyć zadanie

## Przykład

```bash
# Po utworzeniu zadania z /plan
/implement_this user-auth

# Orchestrator będzie:
# - Czytać jobs/scheduled/user-auth/PRD.md
# - Czytać jobs/scheduled/user-auth/plan.md
# - Wykonywać każdą fazę
# - Delegować zadania do coding-agent, validator, etc.
# - Aktualizować status.md na bieżąco
# - Przenosić do jobs/completed/user-auth po ukończeniu
```

## Monitorowanie Postępu

Podczas wykonania sprawdzaj:
- `jobs/scheduled/<job-slug>/status.md` - Bieżący status i postęp
- `jobs/scheduled/<job-slug>/worklog.md` - Szczegółowy dziennik wykonania
- Orchestrator będzie dostarczać zwięzłe aktualizacje w chacie

## Ręczna Interwencja

Jeśli orchestrator utknął:
- Sprawdź status.md w poszukiwaniu opisu blokera
- Napraw problem ręcznie jeśli trzeba
- Ponownie uruchom `/implement_this <job-slug>` żeby wznowić z bieżącej fazy

## Opcje Zaawansowane

```
/implement_this <job-slug> --phase <N>      # Zacznij od konkretnej fazy
/implement_this <job-slug> --resume         # Wznów z ostatniego checkpointa
/implement_this <job-slug> --validate-only  # Tylko walidacja bez wykonania
```

## Powiązane Komendy

- `/plan` - Utwórz nowe zadanie
- `/status <job-slug>` - Sprawdź status zadania
- `/archive <job-slug>` - Przenieś do ukończonych bez wykonania
- `/cancel <job-slug>` - Anuluj i wyczyść zadanie
