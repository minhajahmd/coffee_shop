// Cart Context logic to manage global shopping cart state

import { createContext, useContext, useState } from "react";

type CartItems = {
    [key: string]: number;
}

type CartContextType = {
    cartItems: CartItems;
    addToCart: (itemKey: string, quantity: number) => void;
    setQuantityCart: (itemKey: string, delta: number) => void;
    emptyCart: () => void;
}

// Create the context with an initial undefined state
const CartContext = createContext<CartContextType | undefined>(undefined);

// Provider component that wraps the app and provides cart state
export const CartProvider = ({children}: {children: React.ReactNode}) => {
  const [cartItems, setCartItems] = useState<CartItems>({});

  // Add or update item quantity in the cart
  const addToCart = (itemKey: string, quantity: number) => {
    setCartItems((prevCartItems) => {
      return {
        ...prevCartItems,
        [itemKey]: (prevCartItems[itemKey] || 0) + quantity,
      }
    })
  }

  // Change quantity based on delta (can be + or -)
  const setQuantityCart = (itemKey: string, delta: number) => {
    setCartItems((prevCartItems) => {
      return {
        ...prevCartItems,
        [itemKey]: Math.max((prevCartItems[itemKey] || 0) + delta, 0)
      }
    })
  }

  // Clears the cart completely
  const emptyCart = () => {
    setCartItems({});
  }


  return (
    <CartContext.Provider value={{cartItems, addToCart, setQuantityCart, emptyCart}}>
      {children}
    </CartContext.Provider>
  );
}

// Custom hook to easily use the cart
export const useCart = (): CartContextType => {
  const context = useContext(CartContext);
  if (!context){
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}