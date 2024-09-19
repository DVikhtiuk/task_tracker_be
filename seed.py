import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.basic_jwt_user_auth import pwd_context
from app.db.database import AsyncSessionLocal
from app.enums.user_role import UserRole
from app.models import User


async def create_initial_users(session: AsyncSession) -> None:
    """
    Creates initial users in the database if they do not already exist.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session.

    This function checks for existing users with predefined emails
    and creates new users with specific roles (ADMIN, MANAGER, USER)
    if they are not found in the database.
    """
    # List of initial users to be created
    users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin1234",
            "role": UserRole.ADMIN,
        },
        {
            "username": "manager",
            "email": "manager@example.com",
            "password": "manager1234",
            "role": UserRole.MANAGER,
        },
        {
            "username": "user",
            "email": "user@example.com",
            "password": "user1234",
            "role": UserRole.USER,
        },
    ]

    existing_emails_query = await session.execute(select(User.email))
    existing_emails = {email for email, in existing_emails_query.all()}

    for user_data in users:
        if user_data["email"] not in existing_emails:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password=pwd_context.hash(user_data["password"]),
                role=user_data["role"],
            )
            session.add(user)
            print(f"Created user: {user.username} with role {user.role}")

    await session.commit()


async def main():
    """
    Main function to create initial users in the database.

    Establishes a database session and calls the `create_initial_users` function
    to ensure predefined users exist in the system.
    """
    async with AsyncSessionLocal() as session:
        await create_initial_users(session)


if __name__ == "__main__":
    asyncio.run(main())
