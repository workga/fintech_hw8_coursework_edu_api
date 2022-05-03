import pytest
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.app import create_app
from app.api.deps import Auth
from app.database.utils import recreate_db, create_admin
from app.models.user import User


@pytest.fixture(name='app', autouse=True)
async def fixture_app():
    await recreate_db(testing=True)
    await create_admin(
        email='admin@api.edu',
        password='admin',
        testing=True
    )

    return create_app(testing=True)


@pytest.fixture(name='client')
async def fixture_client(app):
    return TestClient(app)


@pytest.fixture(name='mocked_auth')
def fixture_mocked_auth(app, mocker):
    mocked_auth = mocker.patch('app.api.deps.Auth', spec=True)

    async def mocked_auth_dependency():
        return mocked_auth

    app.dependency_overrides[Auth] = mocked_auth_dependency

    return mocked_auth


@pytest.fixture(name='set_auth')
def set_auth_user(mocked_auth):
    
    def set_user(user: User):
        mocked_auth.check_roles = AsyncMock(return_value=user)
    
    return set_user