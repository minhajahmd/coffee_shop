import { Text, View } from 'react-native'
import React from 'react'
import { MessageInterface } from '@/types/types';
import { ScrollView } from 'react-native-gesture-handler';
import MessageItem from './MessageItem';

interface MessageListProps {
    messages: MessageInterface[];
}

const MessageList = ({messages}: MessageListProps) => {
  
  return (
    <ScrollView>
      {messages.map((message, index) => (
        <MessageItem key={index} message={message} />
      ))}
    </ScrollView>
  )
}

export default MessageList