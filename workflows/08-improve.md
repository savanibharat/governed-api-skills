# 08 - Improve
<!-- Fix the skill on failure - never the sources. -->

On failure:
1. Diagnose the failing contract or requirement.
2. Fix the SKILL - not the source docs, and never by inventing a business rule to pass.
3. If the failure reveals a missing guard, fix it in the uber standard (propose to federation,
   approved), then re-bake by regeneration - do not hand-edit a baked copy.
4. Re-run the failed eval AND the regression suite.
5. Preserve the original failure and the remediation as evidence (do not erase history).

When the correct behavior cannot be determined from the sources, stop and ask (human approval).

Loop until the evaluation-policy gate passes. Then `09-validate.md`.
