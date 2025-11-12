from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class GenerateRequest(BaseModel):
    prompt: str = Field(..., description="The prompt to send to the LLM")
    provider: str = Field(default="auto", description="LLM provider: auto, groq, gemini, openai")
    model: Optional[str] = Field(None, description="Specific model to use")
    max_tokens: int = Field(default=2000, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, description="Temperature for generation")

class GenerateResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None
    provider: str
    model: Optional[str] = None

class WebsiteGenerateRequest(BaseModel):
    description: str = Field(..., description="Description of the website to generate")
    style: Optional[str] = Field("modern", description="Style of the website")
    pages: Optional[int] = Field(1, description="Number of pages to generate")

class CreateProjectRequest(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    files: Dict[str, Any] = Field(default_factory=dict, description="Project files")
    userId: Optional[str] = None

class ProjectSchema(BaseModel):
    id: str
    name: str
    description: str
    created_at: str
    files: Dict[str, Any] = Field(default_factory=dict)
    userId: Optional[str] = None
    githubSynced: Optional[bool] = False
    githubRepoUrl: Optional[str] = None

class ChatMessageSchema(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str

class CreateChatHistoryRequest(BaseModel):
    userId: str
    projectId: Optional[str] = None
    messages: List[Dict[str, Any]] = Field(default_factory=list)

class ChatHistorySchema(BaseModel):
    id: str
    userId: str
    projectId: Optional[str] = None
    messages: List[Dict[str, Any]]
    created_at: str
    updated_at: str

class UpdateChatHistoryRequest(BaseModel):
    messages: List[Dict[str, Any]]

class PaymentMethodSchema(BaseModel):
    id: str
    name: str
    enabled: bool
    accountNumber: Optional[str] = None
    qrCodeUrl: Optional[str] = None
    apiKey: Optional[str] = None
    instructions: Optional[str] = None
    walletAddress: Optional[str] = None

class GoogleDriveAuthRequest(BaseModel):
    code: str

class GitHubAuthRequest(BaseModel):
    code: str

class SyncProjectToGitHubRequest(BaseModel):
    projectId: str
    repoName: str
    description: Optional[str] = ""
    isPrivate: Optional[bool] = True
