from fastapi import APIRouter, HTTPException
import httpx
import os
import base64
from typing import Dict, Any, List
from schemas import ProjectSchema, SyncProjectToGitHubRequest
from database import get_database

router = APIRouter(prefix="/api/github-sync", tags=["GitHub Sync"])

async def create_github_repo(access_token: str, repo_name: str, description: str, is_private: bool) -> Dict[str, Any]:
    """Create a new GitHub repository"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json"
            },
            json={
                "name": repo_name,
                "description": description,
                "private": is_private,
                "auto_init": True
            }
        )
        
        if response.status_code not in [201, 200]:
            error_data = response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=error_data.get("message", "Failed to create repository")
            )
        
        return response.json()

async def create_or_update_file(
    access_token: str,
    owner: str,
    repo: str,
    path: str,
    content: str,
    message: str,
    sha: str = None
) -> Dict[str, Any]:
    """Create or update a file in GitHub repository"""
    async with httpx.AsyncClient() as client:
        encoded_content = base64.b64encode(content.encode()).decode()
        
        data = {
            "message": message,
            "content": encoded_content
        }
        
        if sha:
            data["sha"] = sha
        
        response = await client.put(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json"
            },
            json=data
        )
        
        if response.status_code not in [200, 201]:
            error_data = response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=error_data.get("message", f"Failed to create/update file: {path}")
            )
        
        return response.json()

async def get_file_sha(access_token: str, owner: str, repo: str, path: str) -> str:
    """Get the SHA of a file in the repository (if it exists)"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("sha")
        
        return None

@router.post("/sync")
async def sync_project_to_github(
    request: SyncProjectToGitHubRequest,
    accessToken: str
):
    """Sync a project to GitHub repository"""
    
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    projects_collection = db.projects
    project = await projects_collection.find_one({"id": request.projectId})
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {accessToken}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            
            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid GitHub access token")
            
            user_data = user_response.json()
            username = user_data.get("login")
        
        repo_data = await create_github_repo(
            accessToken,
            request.repoName,
            request.description or project.get("description", ""),
            request.isPrivate
        )
        
        repo_url = repo_data.get("html_url")
        repo_name = repo_data.get("name")
        
        files = project.get("files", {})
        
        for file_path, file_content in files.items():
            if isinstance(file_content, dict):
                file_content = file_content.get("content", "")
            
            sha = await get_file_sha(accessToken, username, repo_name, file_path)
            
            await create_or_update_file(
                accessToken,
                username,
                repo_name,
                file_path,
                str(file_content),
                f"Add/Update {file_path}",
                sha
            )
        
        await projects_collection.update_one(
            {"id": request.projectId},
            {"$set": {
                "githubSynced": True,
                "githubRepoUrl": repo_url
            }}
        )
        
        return {
            "success": True,
            "repoUrl": repo_url,
            "message": f"Project successfully synced to {repo_url}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update")
async def update_github_repo(
    projectId: str,
    accessToken: str
):
    """Update existing GitHub repository with latest project changes"""
    
    db = get_database()
    if not db:
        raise HTTPException(status_code=500, detail="Database not connected")
    
    projects_collection = db.projects
    project = await projects_collection.find_one({"id": projectId})
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not project.get("githubSynced") or not project.get("githubRepoUrl"):
        raise HTTPException(status_code=400, detail="Project is not synced with GitHub")
    
    try:
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {accessToken}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            
            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid GitHub access token")
            
            user_data = user_response.json()
            username = user_data.get("login")
        
        repo_url = project.get("githubRepoUrl")
        repo_name = repo_url.split("/")[-1]
        
        files = project.get("files", {})
        
        for file_path, file_content in files.items():
            if isinstance(file_content, dict):
                file_content = file_content.get("content", "")
            
            sha = await get_file_sha(accessToken, username, repo_name, file_path)
            
            await create_or_update_file(
                accessToken,
                username,
                repo_name,
                file_path,
                str(file_content),
                f"Update {file_path} via Doveable AI",
                sha
            )
        
        return {
            "success": True,
            "message": f"Project successfully updated in {repo_url}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
