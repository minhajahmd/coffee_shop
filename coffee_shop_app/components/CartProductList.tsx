import { Text, View, Image, TouchableOpacity } from 'react-native'
import React from 'react'
import { Product } from '@/types/types'
import { FlatList } from 'react-native-gesture-handler';

interface ProductListProps {
    products: Product[];
    quantities: { [key: string]: number };
    setQuantities: (itemKey: string, delta: number) => void;
    totalPrice: number;
}

const ProductList = ({products, quantities, setQuantities, totalPrice}: ProductListProps) => {
  const filteredProducts = products.filter((product) => (quantities[product.name] || 0) > 0);
  const renderItem = ({ item }: { item: Product }) => (
    <View className='flex-row items-center justify-between mx-7 pb-3'>
      <Image 
        source={{ uri: item.image_url }}
        className='w-16 h-16 rounded-lg'
      />
      <View className='flex-1 ml-4'>
        <Text className='text-lg font-[Sora-SemiBold] text-[#242424]'>{item.name}</Text>
        <Text className='font-[Sora-Regular] text-xs text-gray-500'>{item.category}</Text>
      </View>

      <View className='flex-row items-center'>
        <TouchableOpacity
          className='bg-[#EDEDED] w-9 h-9 rounded-full items-center justify-center border border-[#F9F2ED]'
          onPress={() => setQuantities(item.name, -1)}>
          <Text className='text-2xl'>-</Text>
        </TouchableOpacity>
        <Text className='mx-3 font-[Sora-Regular]'>{quantities[item.name]||0}</Text>
        <TouchableOpacity
          className='bg-[#EDEDED] w-9 h-9 rounded-full items-center justify-center border border-[#F9F2ED]'
          onPress={() => setQuantities(item.name, 1)}>
          <Text className='text-xl'>+</Text>
        </TouchableOpacity>
      </View>
    </View>
  )

  return (
    <View>
      {filteredProducts.length > 0 ? (
        <FlatList 
          data={filteredProducts}
          renderItem={renderItem}
          keyExtractor={(item) => item.name}
        />
      ): (
        <View className='mx-7 items-center'>
          <Text className='text-2xl font-[Sora-SemiBold] text-gray-500 mv-4 text-center'>No items in the cart yet</Text>
          <Text className='text-xl font-[Sora-SemiBold] text-gray-500 mv-4 text-center'>Let's Go Get Something Delicious</Text>
        </View>
      )}
    </View>
  )
}

export default ProductList