import { StyleSheet, Text, View } from 'react-native'
import React, { use, useEffect, useState } from 'react'
import { Product } from '@/types/types'
import { fetchProducts } from '@/services/productService';

const home = () => {
  const [products, setProducts] = useState<Product[]>([]);    // 
  const [loading, setLoading] = useState<boolean>(true);

  //  Runs once when the screen first loads
  useEffect(() => {
    const loadProducts = async () => {
      try {
        // Get the prodcuts data from the firebase
        const productsData = await fetchProducts();
        console.log(productsData)
        setProducts(productsData);    // Save products in state
      } catch (err) {
        console.error("Error fetching products:", err);
      } finally {
        setLoading(false);
      }

    }

    loadProducts();
  }, [])    // [] means run this only once when screen opens


  if (loading) {
    return <Text>Loading...</Text>;
  }

  return (
    <View>
      <Text>home</Text>
    </View>
  )
}

export default home

const styles = StyleSheet.create({})