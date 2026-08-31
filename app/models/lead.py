import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class LeadSource(str, enum.Enum):
    WHATSAPP_DIRECT = "whatsapp_direct"
    WEBSITE_FORM = "website_form"
    MANUAL = "manual"  

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    full_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    whatsapp_number: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    source: Mapped[LeadSource] = mapped_column(
        Enum(LeadSource, name="lead_source"), default=LeadSource.MANUAL
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan"
    )