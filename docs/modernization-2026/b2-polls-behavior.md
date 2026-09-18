# B2 — Polls behavior contracts

## Goal

Turn the historical Django polls exercise from an untested tutorial implementation into a small, deterministic behavior contract without adding unrelated product scope.

## Red phase

Tests-only commit:

`3c3b19773fc9fc0cfb685f827e71ce829fdf74d1`

Quality run:

`35363614088` — expected failure.

The new suite discovered **17 tests** and exposed **8 real failures**:

1. a future question detail returned 200 instead of 404;
2. a future question appeared in the index;
3. mixed past/future index data included the future question;
4. `was_published_recently()` returned `True` for a future date;
5. future-question results returned 200 instead of 404;
6. a future question could be voted and redirected normally;
7. an invalid choice rerendered detail without displaying the error message;
8. a missing choice rerendered detail without displaying the error message.

The last two were not missing view logic: the view already populated `error_message`, but `detail.html` never rendered it.

## Green phase

Fix commit:

`dc197ce5b90c693e29bedc2fc72343a87c4a39c0`

Quality run:

`35363711269` — success.

Final result:

- **17 tests found**;
- **17 tests passed**;
- runtime: 0.068 s in CI;
- migrations: no drift;
- clean database reconstruction: success;
- dependency audit: no known vulnerabilities;
- tracked tree remains clean.

## Maintained behavior

### Question recency

`Question.was_published_recently()` now returns true only when:

```text
now - 1 day <= pub_date <= now
```

Future publication dates are not treated as recent.

### Published-question visibility

A single query boundary now defines public questions:

```python
Question.objects.filter(pub_date__lte=timezone.now())
```

It is used by:

- index;
- detail;
- results;
- vote.

Therefore future questions:

- do not appear in the list;
- return 404 from detail;
- return 404 from results;
- cannot receive votes.

### Index contract

The index:

- shows only published questions;
- orders newest first;
- returns at most five;
- has a defined empty-state message.

### Voting contract

Tests protect:

- valid vote increments exactly once and redirects to results;
- missing choice rerenders detail;
- invalid choice rerenders detail;
- the user-visible error message is rendered;
- missing question returns 404;
- future question returns 404 and its choice count stays unchanged.

## Scope discipline

B2 does not:

- add authentication;
- change the data model;
- add APIs;
- add frontend frameworks;
- change database technology;
- redesign templates.

The changes only make the historical polls semantics internally consistent and testable.

## Exit

B2 is complete on `dc197ce5b90c693e29bedc2fc72343a87c4a39c0` with 17/17 tests and permanent Quality green.

B3 owns the remaining configuration/runtime boundary.
