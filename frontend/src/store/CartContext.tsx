import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { Cart } from '../types';
import * as api from '../api';

interface CartContextType {
  cart: Cart | null;
  loading: boolean;
  refreshCart: () => Promise<void>;
  addItem: (productId: string, quantity: number) => Promise<void>;
  updateItem: (itemId: string, quantity: number) => Promise<void>;
  removeItem: (itemId: string) => Promise<void>;
  clearCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType>({
  cart: null,
  loading: true,
  refreshCart: async () => {},
  addItem: async () => {},
  updateItem: async () => {},
  removeItem: async () => {},
  clearCart: async () => {},
});

export const useCart = () => useContext(CartContext);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshCart = useCallback(async () => {
    try {
      const res = await api.getCart();
      setCart(res.data);
    } catch {
      setCart(null);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    refreshCart();
  }, [refreshCart]);

  const addItem = async (productId: string, quantity: number) => {
    await api.addToCart(productId, quantity);
    await refreshCart();
  };

  const updateItem = async (itemId: string, quantity: number) => {
    await api.updateCartItem(itemId, quantity);
    await refreshCart();
  };

  const removeItem = async (itemId: string) => {
    await api.removeCartItem(itemId);
    await refreshCart();
  };

  const clearCartItems = async () => {
    await api.clearCart();
    await refreshCart();
  };

  return (
    <CartContext.Provider
      value={{ cart, loading, refreshCart, addItem, updateItem, removeItem, clearCart: clearCartItems }}
    >
      {children}
    </CartContext.Provider>
  );
};
