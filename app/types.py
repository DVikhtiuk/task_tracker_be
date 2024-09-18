import datetime
from typing import Annotated

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]


when_created = Annotated[
    datetime.datetime,
    mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False),
]

when_updated = Annotated[
    datetime.datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
]
