export interface ResponseItem {
  id: number;
  reference_code: string;
  title: string;
  description?: string;
  category: string | null;
  priority: string | null;
  status: string;
  location?: string;
  coordinator_id?: number | null;
  created_at: string;
  updated_at: string;
}

export interface ResponseCreatePayload {
  reference_code: string;
  title: string;
  description?: string;
  category: string;
  priority: string;
  location?: string;
}

export interface SystemStatus {
  status: string;
  database: string;
  whatsapp_webhook_configured: boolean;
  environment: string;
}