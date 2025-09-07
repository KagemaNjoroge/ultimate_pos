export interface Customer {
  id: number;
  created_at: string;
  updated_at: string;
  first_name: string;
  last_name: string;
  address: string;
  email: string;
  phone: string;
  tax_number: string;
  is_active: boolean;
  photo: string;
}
