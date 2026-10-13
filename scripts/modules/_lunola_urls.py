# SPDX-License-Identifier: GPL-2.0-or-later
"""Lunola product navigation, separate from upstream API and extension services.

Availability is release-maintained, not checked via network during UI startup.
Issues are enabled; no public release or verified tutorial collection exists at
this development milestone. Recheck GitHub before changing those destinations.
"""

LUNOLA_PROJECT_URL = "https://github.com/pujosety/Lunola-Forma"
LUNOLA_DOCS_URL = LUNOLA_PROJECT_URL + "#readme"
LUNOLA_ISSUES_URL = LUNOLA_PROJECT_URL + "/issues"
LUNOLA_BUG_REPORT_URL = LUNOLA_ISSUES_URL + "/new"
LUNOLA_FEATURE_REQUEST_URL = LUNOLA_ISSUES_URL + "/new"
LUNOLA_RELEASES_URL = LUNOLA_PROJECT_URL + "/releases"
# The release collection is empty; the repository changelog is a useful fallback.
LUNOLA_RELEASE_NOTES_URL = LUNOLA_PROJECT_URL + "/blob/main/CHANGELOG.md"
LUNOLA_LICENSES_URL = LUNOLA_PROJECT_URL + "/blob/main/docs/lunola/product/LEGAL.md"
# Hide the tutorial entry until a verified Lunola tutorial collection is published.
LUNOLA_TUTORIALS_URL = None
