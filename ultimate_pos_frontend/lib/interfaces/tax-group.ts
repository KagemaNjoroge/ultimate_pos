/*
  {
      "id": 1,
      "created_at": "2025-07-19T12:26:28.753603+03:00",
      "updated_at": "2025-07-19T12:27:18.697066+03:00",
      "name": "Value Added Tax (VAT)",
      "description": "VAT is an indirect tax that is paid by the person who consumes taxable goods and taxable services supplied in Kenya and/or imported into Kenya.",
      "tax_rate": 16,
      "status": "ACTIVE"
    }
*/

// Tax group type definition
export interface TaxGroup {
  id: number;
  created_at: string;
  updated_at: string;
  name: string;
  description: string;
  tax_rate: number;
  status: string | null; // Can be "ACTIVE", "INACTIVE", or null
}
