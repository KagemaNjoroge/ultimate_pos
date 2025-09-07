// Supplier type definition based on API structure
export interface Supplier {
  id: number;
  name: string;
  address: string;
  phone: string;
  email: string;
  tax_id: string;
  website: string;
  logo: string | null;
  additional_notes: string;
}
