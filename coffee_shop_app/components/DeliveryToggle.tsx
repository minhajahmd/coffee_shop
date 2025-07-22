import { Text, TouchableOpacity, View } from 'react-native'
import React, { useState } from 'react'

const DeliveryToggle = () => {
  const [isDelivery, setIsDelivery] = useState<boolean>(true);

  return (
    <View className='flex-row justify-between bg-[#EDEDED] mx-7 p-1 rounded-xl mt-7'>
      <TouchableOpacity
        className={`py-1 flex-1 rounded-xl items-center ${isDelivery ? 'bg-[#C67C4E]' : ''}`}
        onPress={() => setIsDelivery(true)}
      >
        <Text
          className={`text-lg font-[Sora-SemiBold] ${isDelivery ? 'text-white' : 'text-[#242424]'}`}  
        >Deliver</Text>
      </TouchableOpacity>
      <TouchableOpacity className={`py-1 flex-1 rounded-xl items-center ${!isDelivery ? 'bg-[#C67C4E]' : ''}`}
        onPress={() => setIsDelivery(false)}>
        <Text 
        className={`text-lg font-[Sora-SemiBold] ${!isDelivery ? 'text-white' : 'text-[#242424]'}`}  
        >Pick Up</Text>
      </TouchableOpacity>
    </View>
  )
}

export default DeliveryToggle