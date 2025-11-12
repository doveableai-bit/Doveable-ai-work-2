const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface PaymentMethod {
  id: string;
  name: string;
  enabled: boolean;
  accountNumber?: string;
  qrCodeUrl?: string;
  apiKey?: string;
  instructions?: string;
  walletAddress?: string;
}

export const adminService = {
  async getPaymentMethods(): Promise<PaymentMethod[]> {
    const storedMethods = localStorage.getItem('payment_methods');
    if (storedMethods) {
      return JSON.parse(storedMethods);
    }
    
    const defaultMethods: PaymentMethod[] = [
      { id: 'jazzcash', name: 'JazzCash', enabled: true, accountNumber: '', qrCodeUrl: '', instructions: 'Send payment to the account number above' },
      { id: 'easypaisa', name: 'Easypaisa', enabled: true, accountNumber: '', qrCodeUrl: '', instructions: 'Send payment to the account number above' },
      { id: 'stripe', name: 'Stripe', enabled: false, apiKey: '', instructions: 'Payment will be processed via Stripe' },
      { id: 'paypal', name: 'PayPal', enabled: false, accountNumber: '', instructions: 'Send payment to PayPal email above' },
      { id: 'bank-transfer', name: 'Bank Transfer', enabled: false, accountNumber: '', instructions: 'Transfer to bank account above' },
      { id: 'crypto', name: 'Cryptocurrency', enabled: false, walletAddress: '', instructions: 'Send crypto to wallet address above' },
    ];
    
    localStorage.setItem('payment_methods', JSON.stringify(defaultMethods));
    return defaultMethods;
  },

  async updatePaymentMethods(methods: PaymentMethod[]): Promise<void> {
    localStorage.setItem('payment_methods', JSON.stringify(methods));
  },

  async getGoogleDriveConfig() {
    const config = localStorage.getItem('google_drive_config');
    return config ? JSON.parse(config) : null;
  },

  async saveGoogleDriveConfig(clientId: string, clientSecret: string, projectId: string) {
    const config = { clientId, clientSecret, projectId };
    localStorage.setItem('google_drive_config', JSON.stringify(config));
  },

  async getGitHubConfig() {
    const config = localStorage.getItem('github_config');
    return config ? JSON.parse(config) : null;
  },

  async saveGitHubConfig(clientId: string, clientSecret: string) {
    const config = { clientId, clientSecret };
    localStorage.setItem('github_config', JSON.stringify(config));
  },
};
