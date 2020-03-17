import io

import pytest
from django.core import management


@pytest.mark.django_db
def test_command():
    out = io.StringIO()
    management.call_command('process_receipts', once=True, stdout=out)
    assert 'Start' in out.getvalue()
