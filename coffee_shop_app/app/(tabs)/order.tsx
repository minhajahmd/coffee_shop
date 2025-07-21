import { Text, View } from 'react-native'
import React from 'react'
import PageHeader from '@/components/PageHeader'
import { GestureHandlerRootView } from 'react-native-gesture-handler'

const Order = () => {
  return (
    <GestureHandlerRootView className='w-full h-full bg-[#F9F9F9]'>
      <PageHeader title='Order' showHeaderRight={false} bgColor='#F5F5F5'/>
      <Text>Order</Text>
    </GestureHandlerRootView>
  )
}

export default Order