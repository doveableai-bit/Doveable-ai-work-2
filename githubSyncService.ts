const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface SyncProjectRequest {
  projectId: string;
  repoName: string;
  description?: string;
  isPrivate?: boolean;
}

export interface SyncProjectResponse {
  success: boolean;
  repoUrl: string;
  message: string;
}

export const githubSyncService = {
  async syncProjectToGitHub(
    request: SyncProjectRequest,
    accessToken: string
  ): Promise<SyncProjectResponse> {
    const response = await fetch(`${API_BASE_URL}/api/github-sync/sync`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    });

    const params = new URLSearchParams({ accessToken });
    const fullUrl = `${API_BASE_URL}/api/github-sync/sync?${params}`;

    const actualResponse = await fetch(fullUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    });
    
    if (!actualResponse.ok) {
      const error = await actualResponse.json();
      throw new Error(error.detail || 'Failed to sync project to GitHub');
    }
    
    return await actualResponse.json();
  },

  async updateGitHubRepo(
    projectId: string,
    accessToken: string
  ): Promise<{ success: boolean; message: string }> {
    const params = new URLSearchParams({ projectId, accessToken });
    const response = await fetch(`${API_BASE_URL}/api/github-sync/update?${params}`, {
      method: 'POST'
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to update GitHub repository');
    }
    
    return await response.json();
  },
};
