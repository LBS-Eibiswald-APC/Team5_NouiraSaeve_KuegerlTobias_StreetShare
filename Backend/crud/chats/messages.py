from Backend.crud.base import CRUDBase
from Backend.model.chats.conversation import Conversation
from Backend.schemas.chats.conversation import ConversationCreate, ConversationUpdate


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationUpdate]):
    pass

crud_conversation = CRUDConversation(Conversation)