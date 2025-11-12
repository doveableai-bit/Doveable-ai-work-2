const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface GenerateRequest {
  prompt: string;
  provider?: 'auto' | 'groq' | 'gemini' | 'emergent' | 'openai';
  model?: string;
  max_tokens?: number;
  temperature?: number;
}

export interface GenerateResponse {
  success: boolean;
  response?: string;
  error?: string;
  provider: string;
  model?: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  created_at: string;
  files: Record<string, any>;
}

export interface CreateProject {
  name: string;
  description: string;
  files?: Record<string, any>;
}

class BackendApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async generateText(request: GenerateRequest): Promise<GenerateResponse> {
    try {
      const response = await fetch(`${this.baseUrl}/api/llm/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to generate text');
      }

      return await response.json();
    } catch (error) {
      console.error('Error generating text:', error);
      throw error;
    }
  }

  async getAvailableProviders(): Promise<string[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/llm/providers`);
      if (!response.ok) {
        throw new Error('Failed to fetch providers');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching providers:', error);
      return [];
    }
  }

  async checkHealth(): Promise<any> {
    try {
      const response = await fetch(`${this.baseUrl}/api/llm/health`);
      return await response.json();
    } catch (error) {
      console.error('Error checking health:', error);
      return { status: 'unavailable' };
    }
  }

  async getProjects(): Promise<Project[]> {
    try {
      const response = await fetch(`${this.baseUrl}/api/projects/`);
      if (!response.ok) {
        throw new Error('Failed to fetch projects');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching projects:', error);
      return [];
    }
  }

  async createProject(project: CreateProject): Promise<Project> {
    try {
      const response = await fetch(`${this.baseUrl}/api/projects/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(project),
      });

      if (!response.ok) {
        throw new Error('Failed to create project');
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating project:', error);
      throw error;
    }
  }

  async getProject(projectId: string): Promise<Project> {
    try {
      const response = await fetch(`${this.baseUrl}/api/projects/${projectId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch project');
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching project:', error);
      throw error;
    }
  }

  async deleteProject(projectId: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}/api/projects/${projectId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete project');
      }
    } catch (error) {
      console.error('Error deleting project:', error);
      throw error;
    }
  }
}

export const backendApiService = new BackendApiService();
