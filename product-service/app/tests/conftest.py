import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncConnection

from testcontainers.community.postgres import PostgresContainer

from main import app
from database.database import get_session
from database.models import Product


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:18.6", driver="asyncpg") as pg:
        yield pg


@pytest_asyncio.fixture(scope="session")
async def engine(postgres_container):
    url = postgres_container.get_connection_url()
    engine = create_async_engine(url, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine):
    connection: AsyncConnection = await engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        bind=connection, expire_on_commit=False, class_=AsyncSession
    )
    session = session_maker()

    await connection.begin_nested()

    from sqlalchemy import event
    @event.listens_for(session.sync_session, "after_transaction_end")
    def _restart_savepoint(sync_session, transaction):
        if transaction.nested and not transaction._parent.nested:
            sync_session.begin_nested()

    yield session

    await session.close()
    await trans.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://") as ac:
        yield ac
        
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def mock_product_data():
    return {
        "title": "Second",
        "description": "Some",
        "photo_uri": "http://localhost:8000/some_photo",
        "price": 1000
    }


@pytest_asyncio.fixture
async def create_new_product(client: AsyncClient, mock_product_data):
    response = await client.post("/api/products", json=mock_product_data)

    assert response.status_code == 201

    assert response.json()["title"] == mock_product_data["title"]
    assert response.json()["description"] == mock_product_data["description"]
    assert response.json()["photo_uri"] == mock_product_data["photo_uri"]
    assert response.json()["price"] == mock_product_data["price"]

    return response


@pytest_asyncio.fixture
async def get_id_created_product(client: AsyncClient, db_session: AsyncSession, mock_product_data):

    statement = select(Product).where(Product.title == mock_product_data["title"])
    scalar_result = await db_session.exec(statement)
    product = scalar_result.first()

    assert product is not None
    assert product.id > 0
   
    return product.id