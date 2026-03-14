import client from './client';
import type {
  Product,
  Cart,
  Order,
  UserProfile,
  DistrictProfile,
  Recommendation,
  InventoryItem,
  Category,
  PaginatedResponse,
  AuthTokens,
} from '../types';

// Auth
export const register = (data: {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}) => client.post<{ id: string; email: string; tokens: AuthTokens }>('/accounts/register/', data);

export const login = (email: string, password: string) =>
  client.post<AuthTokens>('/accounts/login/', { email, password });

export const getProfile = () => client.get<UserProfile>('/accounts/profile/');
export const updateProfile = (data: Partial<UserProfile>) =>
  client.put<UserProfile>('/accounts/profile/', data);

export const getDistrictProfile = () =>
  client.get<DistrictProfile>('/accounts/district-profile/');
export const updateDistrictProfile = (data: Partial<DistrictProfile>) =>
  client.put<DistrictProfile>('/accounts/district-profile/', data);

// Products
export const getProducts = (params?: Record<string, string>) =>
  client.get<PaginatedResponse<Product>>('/products/', { params });

export const getProduct = (slug: string) =>
  client.get<Product>(`/products/${slug}/`);

export const getCategories = () =>
  client.get<Category[]>('/products/categories/');

// Cart
export const getCart = () => client.get<Cart>('/cart/');
export const addToCart = (product_id: string, quantity: number) =>
  client.post('/cart/items/', { product_id, quantity });
export const updateCartItem = (itemId: string, quantity: number) =>
  client.put(`/cart/items/${itemId}/`, { quantity });
export const removeCartItem = (itemId: string) =>
  client.delete(`/cart/items/${itemId}/delete/`);
export const clearCart = () => client.delete('/cart/clear/');

// Checkout & Orders
export const checkout = (data: {
  shipping_address: Record<string, string>;
  guest_email?: string;
}) => client.post<{ client_secret: string; order_id: string }>('/checkout/', data);

export const confirmCheckout = (order_id: string) =>
  client.post<Order>('/checkout/confirm/', { order_id });

export const getOrders = () =>
  client.get<PaginatedResponse<Order>>('/orders/');

export const getOrder = (id: string) =>
  client.get<Order>(`/orders/${id}/`);

// Inventory (admin)
export const getInventory = () =>
  client.get<PaginatedResponse<InventoryItem>>('/inventory/');

export const getLowStock = () =>
  client.get<PaginatedResponse<InventoryItem>>('/inventory/low-stock/');

export const updateStock = (productId: string, stock: number) =>
  client.put<InventoryItem>(`/inventory/${productId}/`, { stock });

// Recommendations
export const getRecommendations = () =>
  client.get<{ recommendations: Recommendation[] }>('/recommendations/');
