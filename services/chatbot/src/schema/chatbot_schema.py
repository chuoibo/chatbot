from pydantic import BaseModel, StrictStr
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    success = "success"
    failure = "failure"

class InputChatbotSystemModel(BaseModel):
    user_prompt: Optional[StrictStr]

class ResultChatbotSystemModel(BaseModel):
    output_prompt: Optional[StrictStr]
    emotion: Optional[StrictStr]

class StatusModel(BaseModel):
    status: StatusEnum
    message: Optional[str] = None

class OutputChatbotSystemModel(BaseModel):
    input: Optional[StrictStr]
    result: ResultChatbotSystemModel
    status: StatusModel