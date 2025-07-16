import { Text, TouchableOpacity, View, Image} from 'react-native'
import React, { use, useEffect, useState } from 'react'
import { Product } from '@/types/types'
import { fetchProducts } from '@/services/productService';
import { FlatList, GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaView } from 'react-native-safe-area-context';
import AntDesign from '@expo/vector-icons/AntDesign';
import SearchArea from '@/components/SearchArea';
import { StatusBar } from 'expo-status-bar';
import Banner from '@/components/Banner';


const home = () => {
  const [products, setProducts] = useState<Product[]>([]);    // 
  const [loading, setLoading] = useState<boolean>(true);

  //  Runs once when the screen first loads
  useEffect(() => {
    const loadProducts = async () => {
      try {
        // Get the prodcuts data from the firebase
        const productsData = await fetchProducts();
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
    <GestureHandlerRootView>
      <SafeAreaView className='w-full h-full'>
        <FlatList 
          horizontal={false} 
          numColumns={2}
          columnWrapperStyle={{ justifyContent: 'space-between', marginLeft: 15, marginRight: 15 }}
          keyExtractor={(item, index) => index.toString()}
          data ={products}
          renderItem={({ item }) => (
            <View className='w-[48%] mt-2 bg-white rounded-2xl p-2 justify-between'>
              <TouchableOpacity>
                <Image
                  className="w-full h-32 rounded-2xl"
                  source={{ uri: item.image_url }}
                />
                <Text
                  className='text-[#242424] text-lg font-[Sora-SemiBold] ml-1 mt-2'
                >{item.name}</Text>
                <Text
                  className='text-[#A2A2A2] text-sm font-[Sora-Regular] ml-1 mt-2'
                >{item.category}</Text>
              </TouchableOpacity>
                <View className='flex-row justify-between ml-1 mt-5 mb-2'>
                  <Text className='text-[#050505] text-xl font-[Sora-SemiBold]'>
                    ${item.price.toFixed(2)}
                  </Text>
                <TouchableOpacity>
                  <View className='mr-2 p-2 -mt-1 bg-app_orange_color rounded-lg'>
                    <AntDesign name="plus" size={20} color="white" />
                  </View>
                </TouchableOpacity>
                </View>
            </View>
          )}
        ListHeaderComponent={() => (
          <View
            className='flex'
          >
            <SearchArea/>
            <Banner/>
          </View>
        )}
        />
      </SafeAreaView>
    </GestureHandlerRootView>
  )
}


export default home