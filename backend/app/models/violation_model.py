from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.database import Base


class Violation(Base):

    __tablename__ = "violations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    violation_type = Column(
        String,
        nullable=False,
    )

    track_id = Column(
        Integer,
        nullable=False,
    )

    vehicle_type = Column(
        String,
        nullable=False,
    )

    frame_number = Column(
        Integer,
        nullable=False,
    )

    confidence = Column(
        Float,
        nullable=False,
    )

    timestamp = Column(
        String,
        nullable=False,
    )

    violation_metadata = Column(
        Text,
        nullable=False,
    )