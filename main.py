from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

project_db = [
    {"project_id": 1, "project_name": "Application Programming Interface", "project_details": "Manage connections", "is_active": True}
]

class Project(BaseModel):
    project_name: str = Field(..., min_length=1, details="Name of the project")
    project_details: Optional[str] = Field(None, details="Details of the project")
    is_active: bool = True

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = Field(None, min_length=1, details="Name of the project")
    project_details: Optional[str] = Field(None, details="Details of the project")
    is_active: Optional[bool] = None

def find_project_by_id(project_id: int):
    for project in project_db:
        if project["project_id"] == project_id:
            return project
    return None

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    if project_id <= 0:
        raise HTTPException(status_code=400, detail={"error": "Project ID must be a positive integer"})
    
    project = find_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail={"error": f"Project with id {project_id} not found"})
    
    return {"status": "ok", "PROJECT DETAILS": project}

@app.post("/projects")
def create_project(project: Project):
    new_project_id = len(project_db) + 1
    new_project = {
        "project_id": new_project_id,
        "project_name": project.project_name,
        "project_details": project.project_details,
        "is_active": project.is_active
    }
    project_db.append(new_project)
    
    return {"status": "ok", "PROJECT ADDED": new_project}

@app.patch("/projects/{project_id}")
def update_project(project_id: int, project_update: ProjectUpdate):
    if project_id <= 0:
        raise HTTPException(status_code=400, detail={"error": "Project ID must be a positive integer"})
    
    project = find_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail={"error": f"Project with id {project_id} not found"})
    
    if project_update.project_name is not None:
        project["project_name"] = project_update.project_name
    if project_update.project_details is not None:
        project["project_details"] = project_update.project_details
    if project_update.is_active is not None:
        project["is_active"] = project_update.is_active
    
    return {"status": "ok", "PROJECT UPDATED": project}

@app.delete("/projects/{project_id}")
def delete_project(project_id: int):
    if project_id <= 0:
        raise HTTPException(status_code=400, detail={"error": "Project ID must be a positive integer"})
    
    project = find_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail={"error": f"Project with id {project_id} not found"})
    
    project_db.remove(project)
    return {"status": "ok", "PROJECT DELETED": f"Project with id {project_id} deleted"}

@app.put("/projects/{project_id}")
def replace_project(project_id: int, project: Project):
    if project_id <= 0:
        raise HTTPException(status_code=400, detail={"error": "Project ID must be a positive integer"})
    
    existing_project = find_project_by_id(project_id)
    if existing_project is None:
        raise HTTPException(status_code=404, detail={"error": f"Project with id {project_id} not found"})
    
    existing_project["project_name"] = project.project_name
    existing_project["project_details"] = project.project_details
    existing_project["is_active"] = project.is_active
    
    return {"status": "ok", "PROJECT UPDATED": existing_project}
