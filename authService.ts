const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface GoogleAuthResponse {
  success: boolean;
  accessToken: string;
  refreshToken?: string;
  expiresIn: number;
  userEmail: string;
  userName: string;
}

export interface GitHubAuthResponse {
  success: boolean;
  accessToken: string;
  username: string;
  email?: string;
  name?: string;
  avatarUrl?: string;
}

export const authService = {
  async initiateGoogleAuth(): Promise<{ authUrl: string }> {
    const response = await fetch(`${API_BASE_URL}/api/auth/google/authorize`);
    if (!response.ok) {
      throw new Error('Failed to initiate Google authentication');
    }
    return await response.json();
  },

  async handleGoogleCallback(code: string): Promise<GoogleAuthResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/google/callback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    
    if (!response.ok) {
      throw new Error('Failed to complete Google authentication');
    }
    
    return await response.json();
  },

  async initiateGitHubAuth(): Promise<{ authUrl: string }> {
    const response = await fetch(`${API_BASE_URL}/api/auth/github/authorize`);
    if (!response.ok) {
      throw new Error('Failed to initiate GitHub authentication');
    }
    return await response.json();
  },

  async handleGitHubCallback(code: string): Promise<GitHubAuthResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/github/callback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    
    if (!response.ok) {
      throw new Error('Failed to complete GitHub authentication');
    }
    
    return await response.json();
  },

  async getGitHubRepos(accessToken: string): Promise<any> {
    const response = await fetch(
      `${API_BASE_URL}/api/auth/github/repos?accessToken=${accessToken}`
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch GitHub repositories');
    }
    
    return await response.json();
  },

  saveGoogleAuth(authData: GoogleAuthResponse, userId: string) {
    const storedAuth = {
      ...authData,
      userId,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('google_drive_auth', JSON.stringify(storedAuth));
  },

  getGoogleAuth(userId: string): GoogleAuthResponse | null {
    const stored = localStorage.getItem('google_drive_auth');
    if (!stored) return null;
    
    const auth = JSON.parse(stored);
    if (auth.userId !== userId) return null;
    
    return auth;
  },

  saveGitHubAuth(authData: GitHubAuthResponse, userId: string) {
    const storedAuth = {
      ...authData,
      userId,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('github_auth', JSON.stringify(storedAuth));
  },

  getGitHubAuth(userId: string): GitHubAuthResponse | null {
    const stored = localStorage.getItem('github_auth');
    if (!stored) return null;
    
    const auth = JSON.parse(stored);
    if (auth.userId !== userId) return null;
    
    return auth;
  },

  clearGoogleAuth() {
    localStorage.removeItem('google_drive_auth');
  },

  clearGitHubAuth() {
    localStorage.removeItem('github_auth');
  },
};
