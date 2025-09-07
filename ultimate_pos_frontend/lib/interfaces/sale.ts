// Sales type definition based on API structure
export interface Sale {
  id: number;
  created_at: string;
  customer: number;
  sub_total: number;
  grand_total: number;
  tax_amount: number;
  tax_percentage: number;
  receipt_is_printed: boolean;
  discount: number;
}
