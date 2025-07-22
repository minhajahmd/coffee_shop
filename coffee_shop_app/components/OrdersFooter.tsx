import { Text, View } from 'react-native'
import React from 'react'
interface OrdersFooterProps {
    totalPrice?: number;
}

const OrdersFooter = ({totalPrice}: OrdersFooterProps) => {
  return (
    <View>
      <View className='border-b-4 border-[#F9F2ED] mt-3'>
        <Text className='mx-7 text-[#242424] text-lg font-[Sora-SemiBold] mb-4 mt-4'>
          Payment Summary
        </Text>
        <View className='flex-row justify-between mx-7 mb-3'>
          <Text className='text-base font-[Sora-Regular]'>
            Subtotal
          </Text>
          <Text className='text-base font-[Sora-Regular]'>
            ${totalPrice?.toFixed(2)}
          </Text>
        </View>
        <View className='flex-row justify-between mx-7 mb-3'>
          <Text className='text-base font-[Sora-Regular]'>
            Delivery Fee
          </Text>
          <Text className='text-base font-[Sora-Regular]'>
            ${totalPrice === 0 ? '0.00' : '2.99'}
          </Text>
        </View>
      </View>
    </View>
  )
}

export default OrdersFooter