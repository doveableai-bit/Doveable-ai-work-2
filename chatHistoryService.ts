import { ChatHistory, ChatMessage, CreateChatHistoryRequest, UpdateChatHistoryRequest } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const chatHistoryService = {
  async getChatHistories(userId?: string): Promise<ChatHistory[]> {
    const url = userId 
      ? `${API_BASE_URL}/api/chat-history/?userId=${userId}`
      : `${API_BASE_URL}/api/chat-history/`;
    
    const response = await fetch(url);
    if (!response.ok) {
      console.error('Failed to fetch chat histories');
      return [];
    }
    return await response.json();
  },

  async createChatHistory(request: Omit<ChatHistory, 'id' | 'created_at' | 'updated_at'>): Promise<ChatHistory> {
    const response = await fetch(`${API_BASE_URL}/api/chat-history/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    
    if (!response.ok) {
      throw new Error('Failed to create chat history');
    }
    
    return await response.json();
  },

  async getChatHistory(historyId: string): Promise<ChatHistory> {
    const response = await fetch(`${API_BASE_URL}/api/chat-history/${historyId}`);
    if (!response.ok) {
      throw new Error('Chat history not found');
    }
    return await response.json();
  },

  async updateChatHistory(historyId: string, messages: ChatMessage[]): Promise<ChatHistory> {
    const response = await fetch(`${API_BASE_URL}/api/chat-history/${historyId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages })
    });
    
    if (!response.ok) {
      throw new Error('Failed to update chat history');
    }
    
    return await response.json();
  },

  async deleteChatHistory(historyId: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/chat-history/${historyId}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete chat history');
    }
  },

  async getUserProjectChatHistories(userId: string, projectId: string): Promise<ChatHistory[]> {
    const response = await fetch(
      `${API_BASE_URL}/api/chat-history/user/${userId}/project/${projectId}`
    );
    
    if (!response.ok) {
      console.error('Failed to fetch project chat histories');
      return [];
    }
    
    return await response.json();
  },
};
