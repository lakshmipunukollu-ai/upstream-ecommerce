export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  parent: string | null;
  created_at: string;
}

export interface Product {
  id: string;
  title: string;
  slug: string;
  description?: string;
  price: string;
  stock: number;
  category: Category;
  grade_levels: string[];
  images: string[];
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface CartItem {
  id: string;
  product: Product;
  quantity: number;
  subtotal: string;
}

export interface Cart {
  id: string;
  items: CartItem[];
  total: string;
  item_count: number;
  created_at: string;
}

export interface OrderItem {
  id: string;
  product: Product;
  quantity: number;
  unit_price: string;
  subtotal: string;
}

export interface Order {
  id: string;
  status: string;
  total: string;
  shipping_address: Record<string, string>;
  guest_email: string | null;
  items: OrderItem[];
  created_at: string;
  updated_at: string;
}

export interface UserProfile {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface DistrictProfile {
  id: string;
  district_name: string;
  state: string;
  student_count: number;
  ell_percentage: string;
  free_reduced_lunch_pct: string;
  grade_levels_served: string[];
}

export interface Recommendation {
  product: Product;
  reason: string;
  confidence: number;
  grade_levels_served: string[];
}

export interface InventoryItem {
  id: string;
  title: string;
  slug: string;
  stock: number;
  category_name: string;
  is_active: boolean;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AuthTokens {
  access: string;
  refresh: string;
}
