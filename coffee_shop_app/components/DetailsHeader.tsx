import { Text, View, Image } from 'react-native'
import React from 'react'
import MaterialIcons from '@expo/vector-icons/MaterialIcons'
import MaterialCommunityIcons from '@expo/vector-icons/MaterialCommunityIcons';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import AntDesign from '@expo/vector-icons/AntDesign';


interface DetailHeaderInterface {
    image_url: string,
    name: string,
    type: string,
    rating: number
}

const DetailsHeader = ({image_url, name, type, rating}:DetailHeaderInterface) => {
  return (
    <>
      <Image 
        source = {{uri: image_url}}
        className='w-full h-48 rounded-2xl mt-2'
      />
      <View>
        <Text
          className='text-[#242424] text-2xl font-[Sora-SemiBold] ml-1 mt-4'
        >
          {name}
        </Text>
        <View
          className='flex-row w-full justify-between'
        >
          <Text
            className='text-[#A2A2A2] text-base font-[Sora-Regular] ml-1 mt-1 mb-5'
          >
            {type}
          </Text>
          <View className='flex-row mt-2'>
            <View 
              className='bg-[#EDEDED] p-2 rounded-xl mr-2'
            >
              <MaterialIcons name='delivery-dining' size={24} color="#C67C4E"/>
            </View>
            <View 
              className='bg-[#EDEDED] p-2 rounded-xl mr-2'
            >
              <FontAwesome name="coffee" size={22} color="#C67C4E" />
            </View>
            <View 
              className='bg-[#EDEDED] p-2 rounded-xl mr-2'
            >
              <MaterialCommunityIcons name='food-croissant' size={24} color="#C67C4E"/>
            </View>
          </View>
        </View>
        <View className='flex-row pl-2'>
          <AntDesign name="star" size={23} color="#FBBE21" />
          <Text
          className='pl-2 text-xl -mt-0 font-[Sora-SemiBold]'
          >
            {rating}
          </Text>
        </View>
        <View className='w-full items-center'>
          <View className='w-[90%] border-b border-[#E3E3E3] my-4'>
          </View>
        </View>
      </View>
    </>
  )
}

export default DetailsHeader