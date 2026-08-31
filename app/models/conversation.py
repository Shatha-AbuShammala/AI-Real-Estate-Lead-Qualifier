import enum
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class QualificationTier(str, enum.Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"
    PENDING = "pending"


class ConversationMode(str, enum.Enum):
    """
    مين ماسك المحادثة حالياً - هاد اللي الـ webhook بيتحقق منه أول شي.
    """
    AI_HANDLING = "ai_handling"        # الـ AI مسموح له يرد ويكمل جمع المعلومات
    ESCALATED = "escalated"            # صار escalation، الـ AI متوقف، بانتظار موظف
    HUMAN_HANDLING = "human_handling"  # موظف استلم المحادثة فعلياً


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    lead_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("leads.id"), index=True)

    questions_asked: Mapped[int] = mapped_column(Integer, default=0)
    tier: Mapped[QualificationTier] = mapped_column(
        Enum(QualificationTier, name="qualification_tier"),
        default=QualificationTier.PENDING,
    )
    is_qualification_complete: Mapped[bool] = mapped_column(Boolean, default=False)

    mode: Mapped[ConversationMode] = mapped_column(
        Enum(ConversationMode, name="conversation_mode"),
        default=ConversationMode.AI_HANDLING,
    )
    escalation_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    escalated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_lead_message_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_human_response_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    has_pending_suggested_reply: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    lead: Mapped["Lead"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )
    qualification_data: Mapped["QualificationData"] = relationship(
        back_populates="conversation", uselist=False, cascade="all, delete-orphan"
    )
    suggested_replies: Mapped[list["SuggestedReply"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan"
    )