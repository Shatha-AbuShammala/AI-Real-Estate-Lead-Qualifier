import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class PropertyType(str, enum.Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    LAND = "land"
    OFFICE = "office"


class ReadinessTimeline(str, enum.Enum):
    IMMEDIATE = "immediate"
    WITHIN_3_MONTHS = "within_3_months"
    WITHIN_YEAR = "within_year"
    JUST_EXPLORING = "just_exploring"


class QualificationData(Base):
    __tablename__ = "qualification_data"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversations.id"), unique=True
    )

    property_type: Mapped[PropertyType | None] = mapped_column(
        Enum(PropertyType, name="property_type"), nullable=True
    )
    preferred_location: Mapped[str | None] = mapped_column(String(150), nullable=True)
    budget_min: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    budget_max: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    financing_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    readiness: Mapped[ReadinessTimeline | None] = mapped_column(
        Enum(ReadinessTimeline, name="readiness_timeline"), nullable=True
    )

    conversation: Mapped["Conversation"] = relationship(back_populates="qualification_data")