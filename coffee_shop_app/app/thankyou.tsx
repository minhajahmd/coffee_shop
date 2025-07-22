import { Text, TouchableOpacity, View } from 'react-native'
import React from 'react'
import { Gesture, GestureHandlerRootView } from 'react-native-gesture-handler'
import { router } from 'expo-router'

const thankyou = () => {
  return (
    <GestureHandlerRootView>
      <View className='w-full h-full items-center justify-center'>
        <Text className='text-3xl font-[Sora-SemiBold] text-center mx-10 mb-5'>
            Thank you for your order!
        </Text>
      <TouchableOpacity 
        className='bg-app_orange_color w-[75%] rounded-2xl items-center justify-center mt-4 px-4 py-2'
        onPress={() => router.push('/home')}
      >
        <Text className='text-xl color-white font-[Sora-Regular]'>
          Return to Home
        </Text>
      </TouchableOpacity>
      </View>
    </GestureHandlerRootView>
  )
}

export default thankyou