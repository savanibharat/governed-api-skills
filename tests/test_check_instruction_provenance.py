import shutil
from pathlib import Path

from scripts import check_instruction_provenance as cip

PKG = Path(__file__).resolve().parent.parent
OAPI = PKG / "examples/inputs/customer-api.openapi.yaml"


def _skill(tmp, extra_skill="", extra_ref=""):
    d = tmp / "customer-api"
    shutil.copytree(PKG / "examples/expected/customer-api", d)
    if extra_skill:
        (d / "SKILL.md").write_text((d / "SKILL.md").read_text() + extra_skill)
    if extra_ref:
        (d / "references/customers.md").write_text((d / "references/customers.md").read_text() + extra_ref)
    return d


def test_example_ok_against_spec():
    assert cip.check(PKG / "examples/expected/customer-api", OAPI) == []


def test_lowercase_flagged(tmp_path):
    assert cip.check(_skill(tmp_path, "\n- call delete /customers\n"), OAPI)


def test_full_url_flagged(tmp_path):
    assert cip.check(_skill(tmp_path, "\n- call DELETE https://api.example.com/customers\n"), OAPI)


def test_documented_in_refs_still_flagged(tmp_path):
    # The generator "documents" the bogus op in its own references; comparing to the spec still catches it.
    assert cip.check(_skill(tmp_path, "\n- DELETE /customers\n", "\n## DELETE /customers\n"), OAPI)
