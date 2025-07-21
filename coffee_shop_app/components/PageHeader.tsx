import { Text, TouchableOpacity, View } from 'react-native'
import React from 'react'
import {router, Stack} from 'expo-router'
import AntDesign from '@expo/vector-icons/AntDesign';
import Ionicons from '@expo/vector-icons/Ionicons';

interface HeaderProps {
    title: string,
    showHeaderRight: boolean,
    bgColor: string,
}

const PageHeader: React.FC<HeaderProps> = ({title, showHeaderRight, bgColor}) => {
  return (
    <Stack.Screen
      options={{
        headerShadowVisible: false,
        headerStyle: {
          backgroundColor: bgColor,
        },
        headerTitleAlign: 'center',

        headerTitle: () => (
          <Text className='text-xl text-[#242424] font-[Sora-SemiBold]'>
            {title}
          </Text>
        ),

        headerRight: showHeaderRight ? () => (
          <AntDesign name="hearto" style={{marginRight: 10}}  size={22} color="black" />
        ): undefined,
        headerBackVisible: false,

        headerLeft: () => (
          <View className='flex-row items-center gap-4'>
            <TouchableOpacity 
              className='pl-3'
              onPress={() => router.back()}
            >
              <Ionicons name="chevron-back" size={24} color="black" />            
            </TouchableOpacity>
          </View>
        )

      }}
    />
  )
}

export default PageHeader