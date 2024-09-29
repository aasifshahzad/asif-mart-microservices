from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from datetime import datetime
import enum
from pydantic import EmailStr, BaseModel


# Enum for NotificationType matching Protobuf
class NotificationType(str, enum.Enum):
    TRANSACTIONAL = "TRANSACTIONAL"
    PROMOTIONAL = "PROMOTIONAL"
    INFORMATIONAL = "INFORMATIONAL"
    USER_INTERACTION = "USER_INTERACTION"
    SECURITY = "SECURITY"
    EVENT_BASED = "EVENT_BASED"
    FEEDBACK_SURVEY = "FEEDBACK_SURVEY"


# Enum for Event matching Protobuf
class Event(str, enum.Enum):
    PAYMENT_CONFIRMATION = "PAYMENT_CONFIRMATION"
    ORDER_CONFIRMATION = "ORDER_CONFIRMATION"
    SHIPPING_NOTIFICATION = "SHIPPING_NOTIFICATION"
    DELIVERY_CONFIRMATION = "DELIVERY_CONFIRMATION"
    PASSWORD_RESET = "PASSWORD_RESET"
    ACCOUNT_ACTIVATION = "ACCOUNT_ACTIVATION"
    REFUND_PROCESSED = "REFUND_PROCESSED"
    NEW_PRODUCT_LAUNCH = "NEW_PRODUCT_LAUNCH"
    DISCOUNT_OFFERS = "DISCOUNT_OFFERS"
    SEASONAL_SALES = "SEASONAL_SALES"
    ABANDONED_CART_REMINDERS = "ABANDONED_CART_REMINDERS"
    LOYALTY_PROGRAM_UPDATES = "LOYALTY_PROGRAM_UPDATES"
    ACCOUNT_ACTIVITY_ALERTS = "ACCOUNT_ACTIVITY_ALERTS"
    SUBSCRIPTION_RENEWALS = "SUBSCRIPTION_RENEWALS"
    SYSTEM_MAINTENANCE_ANNOUNCEMENTS = "SYSTEM_MAINTENANCE_ANNOUNCEMENTS"
    PRODUCT_BACK_IN_STOCK = "PRODUCT_BACK_IN_STOCK"
    NEWSLETTERS = "NEWSLETTERS"
    FRIEND_REQUESTS = "FRIEND_REQUESTS"
    MESSAGES_OR_CHAT_ALERTS = "MESSAGES_OR_CHAT_ALERTS"
    SOCIAL_MEDIA_MENTIONS = "SOCIAL_MEDIA_MENTIONS"
    COMMENT_REPLIES = "COMMENT_REPLIES"
    LIKES_AND_REACTIONS = "LIKES_AND_REACTIONS"
    UNUSUAL_LOGIN_ATTEMPT = "UNUSUAL_LOGIN_ATTEMPT"
    TWO_FACTOR_AUTHENTICATION_CODES = "TWO_FACTOR_AUTHENTICATION_CODES"
    SECURITY_ALERTS = "SECURITY_ALERTS"
    UPCOMING_EVENTS = "UPCOMING_EVENTS"
    EVENT_REMINDERS = "EVENT_REMINDERS"
    EVENT_CANCELLATIONS_OR_RESCHEDULES = "EVENT_CANCELLATIONS_OR_RESCHEDULES"
    REVIEW_REQUESTS = "REVIEW_REQUESTS"
    CUSTOMER_SATISFACTION_SURVEYS = "CUSTOMER_SATISFACTION_SURVEYS"
    FEATURE_FEEDBACK_REQUESTS = "FEATURE_FEEDBACK_REQUESTS"


# Enum for NotificationStatus matching Protobuf
class NotificationStatus(str, enum.Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"


class NotificationBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(), nullable=False)


class RecipientInfo(SQLModel):
    username: str
    contact: int
    address: str
    email: EmailStr  # Using Pydantic's EmailStr for better validation


class Notification(NotificationBase, RecipientInfo, table=True):
    notification_type: NotificationType
    event: Event
    subject: str
    message: str
    notification_status: NotificationStatus
    sent_at: Optional[datetime] = None


class CreateNotification(BaseModel):
    notification_type: NotificationType
    event: Event
    subject: str
    message: str
    notification_status: NotificationStatus
    sent_at: Optional[datetime] = None


class NotificationResponse(BaseModel):
    id: int
    created_at: datetime
    username: str
    contact: int
    address: str
    email: EmailStr
    notification_type: NotificationType
    event: Event
    subject: str
    message: str
    notification_status: NotificationStatus
    sent_at: Optional[datetime] = None


# class NotificationType(str, enum.Enum):
#     TRANSACTIONAL = "transactional"
#     PROMOTIONAL = "promotional"
#     INFORMATIONAL = "informational"
#     USER_INTERACTION = "user_interaction"
#     SECURITY = "security"
#     EVENT_BASED = "event_based"
#     FEEDBACK_SURVEY = "feedback_survey"


# class Event(str, enum.Enum):
#     PAYMENT_CONFIRMATION = "Payment Confirmation"
#     ORDER_CONFIRMATION = "Order Confirmation"
#     SHIPPING_NOTIFICATION = "Shipping Notification"
#     DELIVERY_CONFIRMATION = "Delivery Confirmation"
#     PASSWORD_RESET = "Password Reset"
#     ACCOUNT_ACTIVATION = "Account Activation"
#     REFUND_PROCESSED = "Refund Processed"
#     NEW_PRODUCT_LAUNCH = "New Product Launch"
#     DISCOUNT_OFFERS = "Discount Offers"
#     SEASONAL_SALES = "Seasonal Sales"
#     ABANDONED_CART_REMINDERS = "Abandoned Cart Reminders"
#     LOYALTY_PROGRAM_UPDATES = "Loyalty Program Updates"
#     ACCOUNT_ACTIVITY_ALERTS = "Account Activity Alerts"
#     SUBSCRIPTION_RENEWALS = "Subscription Renewals"
#     SYSTEM_MAINTENANCE_ANNOUNCEMENTS = "System Maintenance Announcements"
#     PRODUCT_BACK_IN_STOCK = "Product Back in Stock"
#     NEWSLETTERS = "Newsletters"
#     FRIEND_REQUESTS = "Friend Requests"
#     MESSAGES_OR_CHAT_ALERTS = "Messages or Chat Alerts"
#     SOCIAL_MEDIA_MENTIONS = "Social Media Mentions"
#     COMMENT_REPLIES = "Comment Replies"
#     LIKES_AND_REACTIONS = "Likes and Reactions"
#     UNUSUAL_LOGIN_ATTEMPT = "Unusual Login Attempt"
#     TWO_FACTOR_AUTHENTICATION_CODES = "Two-Factor Authentication (2FA) Codes"
#     SECURITY_ALERTS = "Security Alerts"
#     UPCOMING_EVENTS = "Upcoming Events"
#     EVENT_REMINDERS = "Event Reminders"
#     EVENT_CANCELLATIONS_OR_RESCHEDULES = "Event Cancellations or Reschedules"
#     REVIEW_REQUESTS = "Review Requests"
#     CUSTOMER_SATISFACTION_SURVEYS = "Customer Satisfaction Surveys"
#     FEATURE_FEEDBACK_REQUESTS = "Feature Feedback Requests"


# class NotificationStatus(str, enum.Enum):
#     PENDING = "pending"
#     SENT = "sent"
#     FAILED = "failed"


# class NotificationBase(SQLModel):
#     id: int | None = Field(default=None, primary_key=True)
#     created_at: datetime = Field(default=datetime.now(), nullable=False)


# class RecipientInfo(SQLModel):
#     username: str
#     contact: int
#     address: str
#     email: str


# class Notification(NotificationBase, RecipientInfo, table=True):
#     notification_type: NotificationType
#     event: Event
#     subject: str
#     message: str
#     notification_status: NotificationStatus
#     sent_at: Optional[datetime] = None


# class CreateNotification(SQLModel):
#     notification_type: NotificationType
#     event: Event
#     subject: str
#     message: str
#     notification_status: NotificationStatus
#     sent_at: Optional[datetime] = None


# class NotificationResponse(NotificationBase, RecipientInfo, SQLModel):
#     notification_type: str
#     event: str
#     subject: str
#     message: str
#     notification_status: str
#     sent_at: None | datetime
