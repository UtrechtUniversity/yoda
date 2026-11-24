# Contributing to Yoda

Thank you for your interest in contributing to Yoda!

Yoda is developed by [Utrecht University](https://www.uu.nl/) and used by
multiple institutes around the world. Contributions from the community are
very welcome, whether that's reporting a bug, suggesting an improvement,
improving the documentation or submitting code.

This document explains how you can contribute and what we look for when
reviewing contributions. We're happy to help you along the way.

## Table of contents

- [Ways to contribute](#ways-to-contribute)
- [Before you start](#before-you-start)
- [Setting up a development environment](#setting-up-a-development-environment)
- [Making changes](#making-changes)
- [Submitting a pull request](#submitting-a-pull-request)
- [Definition of done](#definition-of-done)
- [Reporting security vulnerabilities](#reporting-security-vulnerabilities)
- [License](#license)
- [Recognition](#recognition)

## Ways to contribute

There are many ways to help out:

- **Asking questions and sharing ideas**: the best place for this is our
  [GitHub Discussions page](https://github.com/UtrechtUniversity/yoda/discussions).
  You can [ask a question](https://github.com/UtrechtUniversity/yoda/discussions/categories/q-a)
  or [share an idea](https://github.com/UtrechtUniversity/yoda/discussions/categories/ideas).
- **Reporting bugs**: please search the existing
  [issues](https://github.com/UtrechtUniversity/yoda/issues) first. If your
  problem isn't tracked yet, please
  [create a new issue](https://github.com/UtrechtUniversity/yoda/issues/new/choose).
- **Requesting features**: you can submit a feature request using the
  [issue tracker](https://github.com/UtrechtUniversity/yoda/issues/new/choose).
- **Improving the documentation**: the documentation lives in the
  [`docs`](docs) directory of this repository and is published at
  <https://utrechtuniversity.github.io/yoda/>.
- **Contributing code**: see the sections below.

## Before you start

### Small changes

For small changes, such as fixing a typo, a small bug fix or a minor
improvement, feel free to open a pull request right away.

### Larger contributions

If you're planning to contribute a larger amount of work, such as a new
feature, a substantial refactoring or a change that affects multiple
components, please **contact the development team before you start**. That
way we can coordinate the work, make sure it fits in with our plans, and avoid
you spending time on something that overlaps with ongoing work or that would
be hard to merge. You can reach us via email at yoda@uu.nl.

### Which repository?

Yoda consists of multiple repositories. This repository contains the Ansible
playbooks and roles, the Docker setup and the technical documentation. Other
components, such as the portal and the ruleset, have their own repositories.
See the [overview of repositories](docs/development/overview-repositories.md)
to find out where your change belongs.

## Setting up a development environment

The development documentation explains how to get started:

- [Setting up a development environment](docs/development/setting-up-development-environment.md)
  (using Vagrant)
- [Running Yoda using Docker Compose](docs/development/docker-setup.md)
- [Development tips](docs/development/development-tips.md)

For running tests:

- [Running unit and integration tests](docs/development/running-unit-integration-tests.md)
- [Running API and UI tests](docs/development/running-api-ui-tests.md)

## Making changes

### Coding style

Our CI runs a number of linters, including
[ansible-lint](https://ansible.readthedocs.io/projects/lint/),
[ShellCheck](https://www.shellcheck.net/) and a Dockerfile linter, and the
documentation build is checked as well. Please make sure your changes pass
these checks.

For the `yoda-ruleset` and `yoda-portal` repositories, see the `setup.cfg`
file for the linting tool configuration. For `yoda-moai`,
`yoda-external-user-service` and `yoda-web-mock`, see the
`pyproject.toml` file.

### Commit messages

Please write clear commit messages that describe what the change does.
Prefer the imperative mood (e.g. "update the foo package") rather
than the past tense (e.g. "updated the foo package") or the gerund
(e.g. "updating the foo package").

Commit messages in this repository typically start with the related ticket
number or the affected component, for example:

```
YDA-1234: add configuration parameter for foo
```

or

```
Mailpit: update to v1.33.0
```

The internal issue tracker is currently not publicly accessible. If you
are not aware of any ticket number associated with the issue/improvement,
please just use the second form with the component prefix instead.

For fixes where other people may need some context to understand the changes
(so not, for example, spelling fixes or routine dependency bumps),
please include a short explanation of why the change was made, for example:

```
Ruleset: fix regression in vault module

The vault module failed with an uncaught exception when
the foo function returned a None result. Added a
special case to the bar function to handle this situation.
```

### Release notes

The development team will take care of updating the [release notes](docs/release-notes)
when needed.

## Submitting a pull request

1. Fork the repository and create a branch for your change, based on the default branch.
   That's the `development` branch for most repositories. Special cases: `yoda-clienttools`
   uses `master` whereas `irods-uu-microservices`, `davrods` and
   `irods-sudo-microservices` use `main`.
2. Make your changes, including tests and documentation where relevant (see
   the [definition of done](#definition-of-done) below).
3. Open a draft pull request with a clear description of what the change does
   and why. Please link to the related issue if there is one.
4. Make sure that CI checks pass. A maintainer may have to approve the
   CI run for your first pull request.
5. Mark the pull request "Ready for review".
6. A member of the development team will review your pull request. We may ask
   questions or suggest changes; this is a normal part of the process and
   helps us keep Yoda reliable and maintainable.

**Please address one issue per pull request**, unless agreed otherwise
beforehand. Small, focused pull requests are much easier to review and test,
so they can usually be merged sooner.

## Definition of done

To keep the quality of Yoda high, we use a *definition of done*: a checklist
of criteria a change should meet before it's merged. It applies to the main Yoda
repositories (yoda, yoda-ruleset, yoda-portal, yoda-external-user-service,
yoda-moai, yoda-web-mock, yoda-zabbix, irods-uu-microservices and
irods-sudo-microservices).

A change is considered done when:

- **It meets the requirements**: it does what the issue describes, including
  any non-functional requirements (such as performance or security).
- **It has been reviewed**: the change has been submitted as a pull request,
  has had a code review, and has been tested for regressions.
- **Existing tests and checks pass**: all CI jobs pass (e.g. linting,
  unit tests, integration tests and ruleset API tests).
- **New functionality has automated tests**:
  - Unit tests and/or integration tests for domain logic, utility functions
    and microservices that interact with iRODS.
  - API tests for at least the happy flow of new functionality in the ruleset
    API.
- **Documentation is up to date**: new or changed functionality is
  documented. This can also mean updating docstrings.

The definition of done is a guideline, not a set of rigid rules. If a
particular item doesn't make sense for your change, that's fine. Just mention
it in your pull request and we can discuss it. And if you're unsure how to,
for example, write a test for your change, feel free to ask for help.

## Reporting security vulnerabilities

Please **don't** report security vulnerabilities through public GitHub
issues. Instead, follow the instructions in our [security policy](SECURITY.md).

## License

Yoda is mainly licensed under [GPL-v3](LICENSE). Some repositories
have different licenses (see the LICENSE file of each repository). By
contributing to Yoda, you agree that your contributions will be licensed
under the license of the repository you contribute to.
