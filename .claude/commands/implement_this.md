# /implement_this

Wykonaj zaplanowane zadanie używając agenta orchestrator.

## Użycie
```
/implement_this
```

## Co To Robi

1. Waliduje że `.claude/job/PLAN.md` istnieje
2. Uruchamia **agenta orchestrator** z kontekstem planu
3. Orchestrator czyta `.claude/job/PLAN.md`
4. Wykonuje fazy sekwencyjnie delegując do sub-agentów
5. Tworzy raporty w `.claude/job/reports/`

## Warunki Wstępne

- Plan musi istnieć w `.claude/job/PLAN.md`
- Użyj `/plan` żeby najpierw stworzyć plan

## Przykład

```bash
# Po utworzeniu planu z /plan
/implement_this

# Orchestrator będzie:
# - Czytać .claude/job/PLAN.md
# - Wykonywać każdą fazę
# - Delegować zadania do coding-agent, validator, etc.
# - Zapisywać raporty w .claude/job/reports/
```

## Monitorowanie Postępu

Podczas wykonania sprawdzaj:
- `.claude/job/reports/` - Raporty z każdej fazy
- Orchestrator będzie dostarczać zwięzłe aktualizacje w chacie

## Ręczna Interwencja

Jeśli orchestrator utknął:
- Sprawdź raporty w `.claude/job/reports/`
- Napraw problem ręcznie jeśli trzeba
- Ponownie uruchom `/implement_this` żeby wznowić z bieżącej fazy

## Powiązane Komendy

- `/plan` - Utwórz lub edytuj PLAN.md
- `/status` - Sprawdź status bieżącego planu
