# Report a Lunola Forma issue

Use the official [issue tracker](https://github.com/pujosety/Lunola-Forma/issues). Search existing reports first and choose one of four forms:

| Form | Use it for |
| --- | --- |
| Bug Report | Incorrect behavior, crashes or a reproducible product-identity regression |
| Feature Request | A concrete user need and proposed behavior, not an assertion that a feature already exists |
| Performance Issue | Measured slow behavior with a workload, settings and meaningful comparison |
| Compatibility Issue | A project, add-on, file format, device or platform that behaves differently or fails |

The forms are source files in this branch. GitHub will expose them after they reach the default branch; until then a normal issue can include the same information. No default labels or maintainer assignees are imposed.

## Information that helps

1. **Actual Lunola build:** copy the reported version from About or `blender.exe --version`; include the commit/build identifier if available. The current upstream engine base is **5.4.0 Alpha**. Do not invent a Lunola release number or replace actual version output with this expected base.
2. **Environment:** OS version and architecture; GPU model, driver version and backend when relevant. For a non-graphics request, say `Not applicable`; for unavailable information, say `Unknown`. Do not include serial numbers, machine identifiers or account names.
3. **Reproduction:** describe a minimal scene/workload, exact steps, settings, expected behavior and actual behavior. Include frequency and a comparison build only if you actually tested it. A feature request can describe a current workflow and a concrete example of the desired result.
4. **Compatibility/performance:** name the file format or add-on and its version, or provide measured duration/memory/frame rate with units and test conditions. Estimates and untested comparisons should be explicitly marked.

Existing smoke passes do not guarantee every add-on, GPU or project. Preserve important files and reproduce with a disposable copy. Do not change your system, preferences or drivers simply to fill out a report.

## Privacy and attachments

Reports and attachments on this tracker are public. **Logs, screenshots, `.blend` files and other attachments are optional.** None of these templates collects, reads, attaches or uploads local data automatically. A form's log field is ordinary text you choose to paste, not permission to access your system.

Before posting, manually review every field and attachment. Remove credentials/tokens, email/account names, personal filesystem paths, private project names, client assets, embedded metadata and any confidential data. A `.blend` file may contain text, images or packed assets; prefer a small synthetic scene created for reproduction. Check screenshots for other windows and notifications. Only share material you have permission to publish; choose a short redacted log excerpt rather than a full diagnostic dump.

A checkbox cannot sanitize data for you. You may submit without logs or attachments. If you cannot share a reproduction safely, describe the behavior without uploading the private file. No maintainer response time or fix is promised.

## Security reports

Follow [SECURITY.md](../../SECURITY.md) for vulnerabilities. Do not post exploit details, secrets or private data in public issues. The issue tracker is not a private support channel.

## Build and release context

The current verified artifact is a locally built Windows x64 alpha; public binary releases are pending. Record the exact executable used. Documentation/template validation does not certify a fresh application build. See [test results](TEST_RESULTS.md), [known issues](KNOWN_ISSUES.md), [changelog](../../CHANGELOG.md) and [contribution guidance](../../CONTRIBUTING.md).
