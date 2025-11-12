from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import uuid
from schemas import ProjectSchema, CreateProjectRequest
from database import get_database

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectSchema])
async def get_projects():
    db = get_database()
    if not db:
        return []
    
    projects_collection = db.projects
    projects = await projects_collection.find().to_list(100)
    
    return [ProjectSchema(**project) for project in projects]

@router.post("/", response_model=ProjectSchema)
async def create_project(project: CreateProjectRequest):
    project_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    
    project_dict = {
        "id": project_id,
        "name": project.name,
        "description": project.description,
        "files": project.files,
        "created_at": created_at,
        "userId": project.userId,
        "githubSynced": False,
        "githubRepoUrl": None
    }
    
    db = get_database()
    if db:
        projects_collection = db.projects
        await projects_collection.insert_one(project_dict)
    
    return ProjectSchema(**project_dict)

@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(project_id: str):
    db = get_database()
    if not db:
        raise HTTPException(
            status_code=404, 
            detail="Project not found. Database is not connected. Projects are not persisted without MongoDB."
        )
    
    projects_collection = db.projects
    project = await projects_collection.find_one({"id": project_id})
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return ProjectSchema(**project)

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    db = get_database()
    if not db:
        raise HTTPException(
            status_code=404,
            detail="Project not found. Database is not connected. Projects are not persisted without MongoDB."
        )
    
    projects_collection = db.projects
    result = await projects_collection.delete_one({"id": project_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": "Project deleted successfully"}
