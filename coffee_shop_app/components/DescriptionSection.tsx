import { Text, TouchableOpacity, View } from 'react-native'
import React, { useState } from 'react'

interface DetailsInterface {
  description: string;
}

const DescriptionSection = ({ description }: DetailsInterface) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <View>
      <Text className='text-[#242424] text-lg font-[Sora-SemiBold] ml-1'>
        Description
      </Text>
      <View className='p-2'>
        <Text className='text-[#A2A2A2] text-base font-[Sora-Regular]'>
          {expanded ? description : `${description.slice(0, 120)}... `}
          <Text
            className='text-app_orange_color'
            onPress={() => setExpanded(!expanded)}
          >
            {expanded ? ' Read Less' : 'Read More'}
          </Text>
        </Text>
      </View>
    </View>
  );
}

export default DescriptionSection
