from scripts import run_evals


def test_deterministic_all_pass():
    res = run_evals.deterministic_checks()
    assert res and all(r["result"] == "PASS" for r in res)


def test_agent_judged_marked_requires_agent():
    aj = run_evals.agent_judged()
    assert aj and all(r["result"] == "REQUIRES_AGENT" for r in aj)
