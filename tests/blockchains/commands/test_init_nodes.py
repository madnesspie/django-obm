import io

import pytest
from django.core import management


@pytest.mark.django_db
def test_command():
    out = io.StringIO()
    management.call_command('init_nodes', stdout=out)
    assert 'successfully' in out.getvalue()
