import { Text, View, Image } from 'react-native'
import React from 'react'

const Banner = () => {
  return (
    <View className='rounded-lg items-center'>
      <View className='absolute w-full h-[90px] -top-1 items-center bg-[#222222] pb-10'/>
        <Image
          source={require('../assets/images/banner.png')}
          className='w-[90%] h-40 rounded-3xl'
        />
        <View className='absolute w-[90%] pl-7 mt-2 '>
        {/* Promo Badge */}
        <Text
          className='bg-[#ED5151] rounded-lg text-white mb-1 text-m p-1.5 font-[Sora-SemiBold] self-start'>
          Promo
        </Text>
        {/* Promo Title */}
        <View className='bg-[#222222] w-[58%] h-7 top-6'>
        </View>
        <View className='bg-[#222222] w-[45%] h-7 top-9'>
        </View>
        <Text className='text-white text-4xl font-[Sora-SemiBold] mt-3 w-[65%] -top-16' style={{lineHeight:40}}>
          Buy one get one FREE
        </Text>
      </View>
    </View>
  )
}

export default Banner