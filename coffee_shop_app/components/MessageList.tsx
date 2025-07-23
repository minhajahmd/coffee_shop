import { Text, View } from 'react-native'
import React, { useEffect, useRef } from 'react'
import { MessageInterface } from '@/types/types';
import { ScrollView } from 'react-native-gesture-handler';
import MessageItem from './MessageItem';
import TypingIndicator from './TypingIndicator';

interface MessageListProps {
    messages: MessageInterface[];
    isTyping: boolean
}

const MessageList = ({messages, isTyping}: MessageListProps) => {
  const ScrollViewRef = useRef<ScrollView | null>(null);
    ScrollViewRef.current?.scrollToEnd({ animated: true });
  useEffect(() => {

  }, [messages]);

  return (
    <ScrollView
      ref = {ScrollViewRef}
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={{ paddingTop: 10 }}
    >
      {messages.map((message, index) => (
        <MessageItem key={index} message={message} />
      ))}

      {isTyping && (
        <View className='w-[80%] ml-3 mb-3'>
          <View className='flex self-start p-3 px-4 rounded-2xl bg-indigo-100 border border-indigo-200'>
            <TypingIndicator/>
          </View>
        </View>
      )}
    </ScrollView>
  )
}

export default MessageList