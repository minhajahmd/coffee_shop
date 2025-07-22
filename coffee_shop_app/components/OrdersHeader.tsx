import { Text, View } from 'react-native'
import React from 'react'
import DeliveryToggle from './DeliveryToggle'

const OrdersHeader = () => {
  return (
    <View>
      <DeliveryToggle />
      <Text
        className='mx-7 mt-7 text-[#242424] text-lg font-[Sora-SemiBold]'
      >Deliver Address</Text>
      <Text className='mx-7 mt-3 text-[#242424] text-base font-[Sora-Regular] mb-2'>
        Jl. Kpg Sutoyo
      </Text>
      <Text className='mx-7 text-[#A2A2A2] text-xs font-[Sora-Regular] mb-3'>
        Kpg. Sutoyo No. 620, Bilzen, Tanjungbalai.
      </Text>
      <View className='mx-12 border-b border-gray-400 my-4'>
      </View>
    </View>
  )
}

export default OrdersHeader
