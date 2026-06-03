from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel

T = TypeVar('T')

class MessageDTO(BaseModel):
    type: str  
    message: str

class APIResponse(BaseModel, Generic[T]):
    status: str  
    message: List[MessageDTO]
    data: Optional[T] = None