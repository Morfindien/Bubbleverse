# Independent review and resolution

A separate fresh-context reviewer inspected the cleanup checker, tests and catalogs without running scientific programs or changing repository files. All four initial fixtures passed during that review. This was a source review, not independent scientific verification or a second production run.

| Finding | Resolution and evidence |
| --- | --- |
| Important: missing protected/launch coverage checks | Added BASE_SHA Git-tree placement coverage, protected inventory cross-check, Python/shell/workflow source coverage, and every program in every tracked registry snapshot. Adversarial omission fixtures fail before the fix and pass after it. |
| Important: documented-command omissions and fragments | Replaced line-start extraction with full tracked-document scan of shell fences, continued commands in plain fences and inline command spans. Verified the full inputcheck invocation is present and the “make n=3 EDE costly” prose is excluded. Source contexts and verification NOT_RUN are retained. |
| Important: special files could block integrity reads | lstat now rejects non-regular/non-symlink types before open. Directory rejection and a FIFO subprocess with a two-second test timeout pass. |
| Minor: unsupported schema branches could be skipped | Added schema-definition traversal before instance checking. Absent-property and empty-array adversarial cases fail before the fix and pass after it. |
| Minor: executed V9 catalog row still NOT_RUN | Linked that exact source invocation to the observed V9 package PASS evidence. |

Final fixture suite: six tests pass. Changes addressing the review were verified by the author; no independent rereview is claimed. No reviewer model setting is claimed or changed. No unresolved review finding is knowingly shipped.
