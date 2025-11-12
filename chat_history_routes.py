from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import uuid
from schemas import ChatHistorySchema, CreateChatHistoryRequest, UpdateChatHistoryRequest
from database import get_database

router = APIRouter(prefix="/api/chat-history", tags=["Chat History"])

@router.get("/", response_model=List[ChatHistorySchema])
async def get_chat_histories(userId: str = None):
    """Get all chat histories, optionally filtered by userId"""
    db = get_database()
    if not db:
        return []
    
    collection = db.chat_histories
    query = {"userId": userId} if userId else {}
    histories = await collection.find(query).to_list(100)
    
    return [ChatHistorySchema(**history) for history in histories]

@router.post("/", response_model=ChatHistorySchema)
async def create_chat_history(request: CreateChatHistoryRequest):
    """Create a new chat history"""
    history_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    
    history_dict = {
        "id": history_id,
        "userId": request.userId,
        "projectId": request.projectId,
        "messages": request.messages,
        "created_at": created_at,
        "updated_at": created_at
    }
    
    db = get_database()
    if db:
        collection = db.chat_histories
        await collection.insert_one(history_dict)
    
    return ChatHistorySchema(**history_dict)

@router.get("/{history_id}", response_model=ChatHistorySchema)
async def get_chat_history(history_id: str):
    """Get a specific chat history by ID"""
    db = get_database()
    if not db:
        raise HTTPException(
            status_code=404, 
            detail="Chat history not found. Database is not connected."
        )
    
    collection = db.chat_histories
    history = await collection.find_one({"id": history_id})
    
    if not history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    
    return ChatHistorySchema(**history)

@router.put("/{history_id}", response_model=ChatHistorySchema)
async def update_chat_history(history_id: str, request: UpdateChatHistoryRequest):
    """Update an existing chat history"""
    db = get_database()
    if not db:
        raise HTTPException(
            status_code=404,
            detail="Chat history not found. Database is not connected."
        )
    
    collection = db.chat_histories
    history = await collection.find_one({"id": history_id})
    
    if not history:
        raise HTTPException(status_code=404, detail="Chat history not found")
    
    updated_at = datetime.utcnow().isoformat()
    await collection.update_one(
        {"id": history_id},
        {"$set": {"messages": request.messages, "updated_at": updated_at}}
    )
    
    history["messages"] = request.messages
    history["updated_at"] = updated_at
    
    return ChatHistorySchema(**history)

@router.delete("/{history_id}")
async def delete_chat_history(history_id: str):
    """Delete a chat history"""
    db = get_database()
    if not db:
        raise HTTPException(
            status_code=404,
            detail="Chat history not found. Database is not connected."
        )
    
    collection = db.chat_histories
    result = await collection.delete_one({"id": history_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chat history not found")
    
    return {"message": "Chat history deleted successfully"}

@router.get("/user/{userId}/project/{projectId}", response_model=List[ChatHistorySchema])
async def get_user_project_chat_histories(userId: str, projectId: str):
    """Get all chat histories for a specific user and project"""
    db = get_database()
    if not db:
        return []
    
    collection = db.chat_histories
    histories = await collection.find({"userId": userId, "projectId": projectId}).to_list(100)
    
    return [ChatHistorySchema(**history) for history in histories]
