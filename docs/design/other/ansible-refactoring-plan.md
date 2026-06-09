---
grand_parent: Software design
parent: Other
---
# Plan: modularize the Ansible playbook, fail early on misconfiguration, reduce runtime

Status: phases 1, 2.1 and 3.1 implemented; remaining phases proposed
Date: 2026-06-09

Implemented so far:

- Phase 1.1: `roles/validate_config` runs as the first play of `playbook.yml`
  (`playbooks/validate.yml`, tagged `always`/`validate`).
- Phase 1.3: `.github/workflows/ansible-syntax-check.yml` syntax-checks all
  playbooks and runs the validation play against all four development
  environments on every push and pull request.
- Phase 2.1: smart fact gathering, fact caching, `forks = 20` and
  task/role profiling callbacks in `ansible.cfg`.
- Phase 3.1: `playbook.yml` is now a thin aggregator of per-component
  playbooks under `playbooks/`.

## Goals

1. **Modularize** `playbook.yml` so individual servers/components can be deployed and iterated on independently.
2. **Fail early** on wrong or incomplete configuration, before any host is changed.
3. **Reduce total running time** of a full deployment and especially of repeated (no-op) runs.

Together these reduce the risk and effort of changes and upgrades and make iteration faster.

## Current state (measured)

- One monolithic `playbook.yml` with 14 plays across 8 host groups, ~60 roles.
- Variables live in 5 tiers (role defaults, role vars, group_vars, host_vars, inventory); ~466 unique
  variables, 57 `PLACEHOLDER` values that must be replaced manually.
- Almost no input validation: only 5 roles contain a `fail:` check (e.g. `postfix`, `yoda_rulesets`);
  a misconfigured variable typically fails mid-run, deep inside a role, after hosts have been changed.
- No fact caching and no `gathering` policy in `ansible.cfg`: every play re-gathers facts on the same
  hosts (~11 fact-gathering plays per run; on an all-in-one host that is 11x redundant work).
- 48 tasks carry `noqa: no-changed-when` (always report "changed"), several `git` checkouts use
  `force: true`/`force: "yes"` (`roles/yoda_portal/tasks/main.yml:49`,
  `roles/yoda_rulesets/tasks/main.yml:23`), so a no-op rerun still does real work and a diff run is noisy.
- 43 task files use legacy `with_items`; tags exist only at play level, never at task level.
- 11 roles duplicate `install-ubuntu.yml` / `install-redhat.yml` pairs.
- CI runs `ansible-lint` only; no syntax check against real inventories, no role-level (Molecule) tests.

## Phase 1 — Fail early on wrong configuration

Cheapest phase, biggest risk reduction. Do this first.

### 1.1 A dedicated validation play that runs before anything else

Create a `roles/validate_config` role and make it the first play of `playbook.yml`
(and importable from `test.yml` / `zabbix.yml`):

```yaml
- name: Validate configuration
  hosts: all
  gather_facts: false
  tags: [always, validate]
  roles:
    - validate_config
```

The role only runs assertions (no changes), so it is safe under `--check` and fast. It should verify:

- **No `PLACEHOLDER` values remain** for variables required by the features that are enabled
  (`enable_postfix` ⇒ `postfix_relayhost`, `enable_data_package_archive` ⇒ archive settings,
  EUS enabled ⇒ `eus_api_secret`/`eus_db_password`, etc.). Express this as a data structure:
  a list of `{when: <enable flag>, required: [vars...]}` entries iterated with `assert`.
- **Types and formats**: FQDNs match a hostname regex, ports are integers in range, booleans are
  booleans (catches `enable_x: "false"` string traps), `yoda_environment` is one of the four valid
  values, `default_yoda_schema` is a known schema.
- **Cross-variable consistency**: e.g. `enable_s3_resource` ⇒ S3 credentials present;
  `yoda_davrods_anonymous_enabled` ⇒ anonymous FQDN/host set.
- **Inventory shape**: required groups (`icats`, `databases`, `portals`, …) are non-empty for the
  chosen environment.

Run it with `delegate_to: localhost` semantics where possible (`hosts: all` but assertion-only) so a
typo never reaches a managed host. Existing scattered checks (postfix, yoda_rulesets) move here or
stay as role-local guards — both is fine; the central role is the gate.

### 1.2 Per-role contracts via `validate-input.yml`

For roles with required inputs, add a small `tasks/validate-input.yml` included first from
`tasks/main.yml`, asserting the role's required variables. This documents each role's interface and
protects roles when they are reused outside the main playbook. Start with the roles that have
caused mid-run failures historically (rulesets, EUS, davrods, postgresql).

### 1.3 Make CI catch it before a human runs it

Extend `.github/workflows/ansible-lint.yml` (or add a workflow) with:

- `ansible-playbook playbook.yml --syntax-check -i environments/development/<env>/hosts` for each
  of the four development environments — catches undefined roles, bad YAML, missing files.
- A "validation only" run against the development inventories:
  `ansible-playbook playbook.yml --tags validate -i ... --connection local` — exercises the
  Phase 1.1 assertions on every PR.

### 1.4 Effort and outcome

Roughly one week. Outcome: a wrong variable fails in seconds with a named message, instead of
after 20 minutes with half a host provisioned.

## Phase 2 — Reduce running time

Ordered by ratio of win to effort.

### 2.1 Fact caching and smart gathering (one-line config, large win)

In `ansible.cfg`:

```ini
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = ~/.ansible/factcache
fact_caching_timeout = 86400
forks = 20
```

With 14 plays re-targeting the same hosts, this removes ~10 redundant fact-gathering rounds per
run. `forks = 20` helps multi-host environments (default is 5). SSH pipelining and ControlPersist
are already enabled — keep them.

### 2.2 Make reruns no-ops (idempotency)

The biggest iteration-speed cost is that a rerun does real work:

- Remove `force: true` from `git` tasks (`yoda_portal`, `yoda_rulesets`, `yoda_web_mock`,
  `yoda_external_user_service`) or gate it: `force: "{{ yoda_environment == 'development' }}"` if
  dev needs to clobber local edits. With pinned versions, an up-to-date checkout then costs one
  `git rev-parse` instead of a fetch/reset, and stops triggering downstream handlers (pip installs,
  asset builds, service restarts).
- Burn down the 48 `noqa: no-changed-when` tasks: give each a `creates:` argument, a
  `changed_when:` based on registered output, or a pre-check (e.g. `s3cmd ls` before `s3cmd mb` in
  `roles/minio/tasks/main.yml`). Target: `--check --diff` on a converged host reports zero changes.
  This is also what makes upgrades safe to preview.
- Batch loop-driven work where the module supports lists; convert serial `with_items` copies
  (e.g. the 23 AppArmor profile copies in `roles/postfix/tasks/main.yml:147`) to single tasks with
  `loop:` over a list — or better, a `copy` of a directory tree where applicable.

### 2.3 Skip work that cannot apply

- Move expensive always-run tasks behind feature flags that are checked before doing work, not after.
- Use `run_once: true` for cluster-singleton operations (database index creation in
  `yoda_database_indexes`, test-data setup in `yoda_test`) so multi-resource environments don't repeat them.
- Audit `retries`/`delay` loops (e.g. `retries: 25` in `roles/yoda_rulesets/tasks/yoda-ruleset.yml`)
  and replace blind delays with `wait_for` on the actual port/file where possible.

### 2.4 Measure

The `timer` callback is already enabled; add `profile_tasks` and `profile_roles` to
`callbacks_enabled` and record a baseline full-run profile before starting, then re-profile after
each sub-phase. Optimize the measured top-10 tasks, not assumptions.

### 2.5 Expected outcome

- First-run: 10–20% faster (fact caching, forks, batched loops).
- Rerun on a converged host: dramatically faster (minutes instead of tens of minutes) once git
  force-checkouts and always-changed tasks are fixed — this is the win that makes iteration fast.

## Phase 3 — Modularize the playbook

### 3.1 Split `playbook.yml` into per-component playbooks

Keep `playbook.yml` as a thin aggregator of imports, so existing invocations keep working:

```
playbooks/
  validate.yml      # Phase 1 play
  preflight.yml     # ansible version check, git branch check
  common.yml        # hostentries, common, certificates
  database.yml      # postgresql, pgbouncer, irods_database, yoda_database_indexes
  icat.yml          # iCAT plays incl. composable_resources, rulesets on icats
  resource.yml      # resource server plays incl. rulesets on resources
  portal.yml
  davrods.yml
  public.yml
  eus.yml
```

```yaml
# playbook.yml
- import_playbook: playbooks/validate.yml
- import_playbook: playbooks/preflight.yml
- import_playbook: playbooks/common.yml
- import_playbook: playbooks/database.yml
...
```

Benefits: `ansible-playbook playbooks/portal.yml` iterates on one component without relying on
`--tags`/`--limit` discipline; each file is small and reviewable; the upgrade procedure can
reference component playbooks explicitly. The existing play-level tags keep working through
`import_playbook`.

### 3.2 Collapse the OS-split duplication

For the 11 roles with `install-ubuntu.yml`/`install-redhat.yml` pairs: where the two files differ
only in package names/URLs, merge into one task file using `ansible.builtin.package` plus
`vars/{{ ansible_os_family }}.yml` (a pattern the repo already uses for vars). Keep the split only
where the flows genuinely differ (repo setup, .deb vs .rpm handling).

### 3.3 Extract cross-cutting roles

- `selinux` helpers: SELinux booleans/fcontext snippets are repeated in `yoda_davrods`,
  `yoda_external_user_service`, `postfix`, `apache` — extract a small reusable role or task file.
- `apparmor` profile deployment (currently inline in `postfix`).
- Replace `meta/main.yml` dependency chains where they cause roles to run multiple times per play
  (e.g. `common` pulled in repeatedly) with explicit ordering in the component playbooks; role
  dependencies silently re-run unless deduplicated and obscure the actual execution order.

### 3.4 Task-level tags inside roles

Adopt a small fixed vocabulary — `install`, `configure`, `service` — applied to task blocks inside
roles. This enables `--tags configure` for config-only iteration (the most common change during
upgrades) without reinstalling packages. Introduce it opportunistically as roles are touched, not
as a big-bang sweep.

### 3.5 Role tests for the riskiest roles

Add Molecule (podman/docker driver) scenarios for the handful of roles where regressions hurt most:
`irods_icat`, `yoda_rulesets`, `postgresql`, `yoda_portal`. CI gains per-role convergence +
idempotence checks (`molecule test` asserts a second run reports no changes — which also guards the
Phase 2.2 work against regressions). The repo's existing Docker images can serve as a base.

## Sequencing and risk

| Phase | Effort | Risk | Depends on |
|---|---|---|---|
| 1. Early validation + CI syntax checks | ~1 week | very low (assert-only) | — |
| 2.1 ansible.cfg (facts, forks, profiling) | hours | very low | — |
| 2.2 Idempotency burn-down | 1–2 weeks | low–medium (behavior of reruns changes) | profiling baseline |
| 3.1 Playbook split via import_playbook | days | low (pure restructuring, tags preserved) | — |
| 3.2–3.4 Role consolidation, tags | 2–3 weeks, incremental | medium | 3.1, Molecule helpful |
| 3.5 Molecule for critical roles | 1 week initial | low | — |

Phases 1, 2.1 and 3.1 are independent and can land in the first week; they deliver most of the
risk reduction (validation), a measurable speedup (fact caching), and the structure that makes
everything afterwards reviewable in small PRs. The idempotency work (2.2) is the long tail — drive
it with the task profile and the Molecule idempotence check, role by role.

## Definition of done

- A run with a deliberately broken variable fails in the validation play with a named message.
- CI fails PRs on syntax errors against all four development inventories and on validation errors.
- `ansible-playbook playbook.yml --check` on a converged all-in-one host reports zero changes.
- A full all-in-one deployment is ≥15% faster than the recorded baseline; a converged rerun
  completes in a small fraction of the baseline.
- Each server type is deployable via its own playbook under `playbooks/`.
