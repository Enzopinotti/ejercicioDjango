# B4 — Template accessibility and admin truth

## Scope

B4 improves concrete HTML/CSS semantics without redesigning the academic exercise.

The Django admin remains the framework-provided learning surface. No custom CMS or business administration product is introduced.

## Red phase

Tests-only commit:

`45dafd7cc864e5d8991828beef53831b86c1970b`

Quality run:

`35364297511`

The suite expanded from 17 to **25 tests**.

Eight new failures documented the missing template/accessibility contracts while the existing 17 behavior tests and two admin contracts remained logically independent.

## Admin contract

The maintained admin surface is deliberately small:

- `Question` is registered;
- `Choice` is registered;
- anonymous access to `/admin/` redirects to Django's login.

B4 does not replace or restyle Django admin.

## Template/runtime improvements

Maintained pages now include:

- responsive viewport metadata;
- a single `<main>` landmark;
- `fieldset` + `legend` for answer choices;
- explicit radio `id` / label `for` relationships;
- browser-required answer selection;
- `role="alert"` for the server-side vote error.

Results now use correct Spanish vote grammar:

- `1 voto`;
- `N votos`.

An empty question reports that it has no available options rather than inaccurately saying there are no recorded votes.

## CSS accessibility

The original visual identity is retained.

B4 adds:

- visible keyboard focus for links/buttons/radios;
- a `prefers-reduced-motion: reduce` contract;
- minimal fieldset/choice layout needed by the semantic markup.

## Green evidence

Final B4 head:

`c7c137b20e70a64a3e75f20151b10c5a4cdca937`

Quality run:

`35364603669` — success.

Final suite:

- **25 tests**;
- behavior tests: green;
- template/static accessibility tests: green;
- admin contracts: green;
- configuration contract: green;
- migrations: green;
- dependency audit: green.

## Non-adoptions

B4 does not:

- change the color system or visual concept;
- add JavaScript;
- add a CSS framework;
- replace templates with React;
- customize Django admin into a new product.

## Exit

B4 is complete with 25/25 tests and the original academic visual scope preserved.
