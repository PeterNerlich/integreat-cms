import pytest

from ..utils import check_view_status_code
from ..view_config import PARAMETRIZED_VIEWS


# pylint: disable=missing-function-docstring
@pytest.mark.django_db
@pytest.mark.parametrize("view_name,kwargs,post_data,roles", PARAMETRIZED_VIEWS[1::16])
def test_view_status_code_1(login_role_user, view_name, kwargs, post_data, roles):
    check_view_status_code(login_role_user, view_name, kwargs, post_data, roles)
