export interface Project {
  id: string;
  name: string;
  description: string;
  created_at: string;
  files: Record<string, any>;
  userId?: string;
  githubSynced?: boolean;
  githubRepoUrl?: string;
}

export interface CreateProject {
  name: string;
  description: string;
  files?: Record<string, any>;
  userId?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export interface ChatHistory {
  id: string;
  userId: string;
  projectId?: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

export interface CreateChatHistoryRequest {
  userId: string;
  projectId?: string;
  messages: ChatMessage[];
}

export interface UpdateChatHistoryRequest {
  messages: ChatMessage[];
}

export interface User {
  id: string;
  email: string;
  name: string;
  coins: number;
  subscriptionStatus: 'active' | 'inactive';
  googleDriveConnected?: boolean;
  githubConnected?: boolean;
  createdAt: string;
}

export interface PaymentRequest {
  id: string;
  userId: string;
  userName: string;
  userEmail: string;
  paymentMethod: PaymentGateway;
  plan: string;
  amount: number;
  proofScreenshotUrl: string;
  status: 'pending' | 'approved' | 'rejected';
  submittedAt: string;
  processedAt?: string;
}

export type PaymentGateway = 'jazzcash' | 'easypaisa' | 'stripe' | 'paypal' | 'bank-transfer' | 'crypto';

export interface PaymentMethod {
  id: PaymentGateway;
  name: string;
  enabled: boolean;
  accountNumber?: string;
  qrCodeUrl?: string;
  apiKey?: string;
  instructions?: string;
  walletAddress?: string;
}

export interface CoinRate {
  plan: string;
  coins: number;
  price: number;
}

export interface Learning {
  id: string;
  content: string;
  createdAt: string;
}

export type AiProvider = 'gemini' | 'groq' | 'emergent' | 'openai' | 'custom';

export interface AiApiKey {
  id: string;
  provider: AiProvider;
  key: string;
  name?: string;
  enabled: boolean;
}

export type BackendServiceType = 
  | 'supabase'
  | 'firebase'
  | 'mongodb'
  | 'cloudflare'
  | 'google-drive-oauth'
  | 'google-drive-service'
  | 'google-sheets'
  | 'github-oauth';

export interface BackendIntegration {
  id: string;
  type: BackendServiceType;
  purpose: string;
  credentials: Record<string, string>;
  enabled: boolean;
}

export type AdProvider = 'google' | 'facebook' | 'custom';

export interface AdvertisementConfig {
  id: string;
  provider: AdProvider;
  name?: string;
  scriptOrCode: string;
  enabled: boolean;
}

export interface GoogleDriveAuth {
  accessToken: string;
  refreshToken?: string;
  expiresAt: number;
  userEmail: string;
  userName: string;
}

export interface GitHubAuth {
  accessToken: string;
  username: string;
  email?: string;
  name?: string;
  repos?: string[];
}
