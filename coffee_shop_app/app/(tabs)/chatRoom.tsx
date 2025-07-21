import { Text, View } from 'react-native'
import React from 'react'
import PageHeader from '@/components/PageHeader'

const ChatRoom = () => {
  return (
    <View>
      <PageHeader title='ChatBot' showHeaderRight={false} bgColor='#F9F9F9'/>
      <Text>chatRoom</Text>
    </View>
  )
}

export default ChatRoom