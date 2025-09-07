// Stock interface based on API response
export interface Stock {
  id: number;
  created_at: string;
  updated_at: string;
  quantity: number;
  alert_quantity: number;
  cost_price: string;
  selling_price: string;
  reserved_quantity: number;
  available_quantity: number;
  minimum_stock_level: number;
  maximum_stock_level: number | null;
  location: string | null;
  warehouse: string | null;
  batch_number: string | null;
  serial_number: string | null;
  expiry_date: string | null;
  manufacturing_date: string | null;
  is_active: boolean;
  is_damaged: boolean;
  is_expired: boolean;
  supplier_sku: string | null;
  notes: string | null;
  last_restocked_date: string | null;
  last_sold_date: string | null;
  product: number;
  branch: number | null;
}
