// Product type definition based on your API response
export interface Product {
  id: number;
  name: string;
  description: string;
  track_inventory: boolean;
  display_image: string | null;
  status: string | null;
  price: number;
  supplier: number | null;
  category: number;
  photos: number[];
  tax_group: number | null;
}
