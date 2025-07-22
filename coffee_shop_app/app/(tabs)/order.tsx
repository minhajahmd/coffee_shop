import { Text, TouchableOpacity, View } from 'react-native'
import React, { useEffect, useState } from 'react'
import PageHeader from '@/components/PageHeader'
import { GestureHandlerRootView } from 'react-native-gesture-handler'
import ProductList from '@/components/CartProductList'
import { Product } from '@/types/types'
import { useCart } from '@/components/CartContext'
import { fetchProducts } from '@/services/productService'
import Ionicons from '@expo/vector-icons/Ionicons';
import MaterialIcons from '@expo/vector-icons/MaterialIcons'


const Order = () => {
  const {cartItems, setQuantityCart, emptyCart} = useCart();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [totalPrice, setTotalPrice] = useState<number>(0);

  // Function to calculate the total price based on the quantities in the cart and the products
  const calculateTotalPrice = (quantities: { [key: string]: number }, products: Product[]) => {
    return products.reduce((total, product) => {
      const quantity = quantities[product.name] || 0;
      return total + (product.price * quantity);
    }, 0)
  }

  // Calculate the total price whenever the cart items or products change
  useEffect(() => {
    const total = calculateTotalPrice(cartItems, products);
    setTotalPrice(total);
  }, [cartItems, products]);

  useEffect(() => {
    const loadProducts = async () => {
      try {
        const productsData = await fetchProducts();
        setProducts(productsData);

        const total = calculateTotalPrice(cartItems, productsData);
        setTotalPrice(total);

      } catch (err) {
        console.error("Error fetching products:", err);
      } finally {
        setLoading(false);
      }
    }
    loadProducts();
  },[])

  return (
    <GestureHandlerRootView className='w-full h-full bg-[#F9F9F9]'>
      <PageHeader title='Order' showHeaderRight={false} bgColor='#F5F5F5'/>
      <View className='h-full flex-col justify-between'>
        <View className='h-[80%]'>
          <ProductList products={products} quantities={cartItems} setQuantities={setQuantityCart} totalPrice={totalPrice}/>
        </View>
        <View className='bg-white rounded-tl-3xl rounded-tr-3xl px-7 pt-5 pb-12'>
          <View className='flex-row justify-between items-center '>
            <View className='flex-row items-center'>
              <Ionicons name='wallet-outline' size={24} color="#C67C4E"/>
              <View>
              <Text className='text-[#242424] text-base font-[Sora-SemiBold] pb-1 pl-3'>
                Cash/Wallet
                </Text>
                <Text className='text-app_orange_color text-base font-[Sora-SemiBold] pb-1 pl-3'>
                  $ {totalPrice === 0 ? 0 : (totalPrice + 2.99).toFixed(2)}
                </Text>
              </View>
            </View>
            <MaterialIcons name='keyboard-arrow-down' size={30} color="black" />
          </View>
          <TouchableOpacity 
            className={` ${totalPrice===0 ? 'bg-[#EDEDED]' : 'bg-app_orange_color'} rounded-2xl items-center justify-between mt-6 py-3`}
            disabled={totalPrice === 0}
          >
            <Text className='text-xl text-white font-[Sora-Regular]'>
              Order
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </GestureHandlerRootView>
  )
}

export default Order