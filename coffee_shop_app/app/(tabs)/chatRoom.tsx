import { KeyboardAvoidingView, Platform, Text, TouchableOpacity, View } from 'react-native'
import React, { useRef, useState } from 'react'
import PageHeader from '@/components/PageHeader'
import { MessageInterface } from '@/types/types'
import { GestureHandlerRootView, TextInput } from 'react-native-gesture-handler'
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen'
import Feather from '@expo/vector-icons/Feather';
import MessageList from '@/components/MessageList'
import { callChatBotAPI } from '@/services/chatBot'
import { useCart } from '@/components/CartContext'


const ChatRoom = () => {
  const [messages, setMessages] = useState<MessageInterface[]>([])
  const textRef = useRef<string>('')
  const inputRef = useRef<TextInput>(null)

  const [isTyping, setIsTyping] = useState(false);

  const { addToCart, emptyCart } = useCart();

  const handleSendMessage =  async () => {
    let message = textRef.current.trim();
    if (!message) return;
    try {
      let inputMessages = [...messages, { content: message, role: 'user' }];
      setMessages(inputMessages)
      textRef.current = '';
      if (inputRef) inputRef?.current?.clear();
      
      // Call API to get response
      setIsTyping(true);
      let responseMessage = await callChatBotAPI(inputMessages);
      setIsTyping(false);
      setMessages([...inputMessages, responseMessage]);

      if (responseMessage) {
        if (responseMessage.memory) {
          if (responseMessage.memory.order) {
            emptyCart();
            responseMessage.memory.order.forEach((item: any) => {
              addToCart(item.item, Number(item.quantity));
            });
          }
        }
      }

    } catch (error) {
      console.error('Error sending message:', error);
      
    }
  }

  return (
    <GestureHandlerRootView>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'android' ? 'padding' : 'height'}
        style={{ flex: 1}}
        keyboardVerticalOffset={Platform.OS === 'android' ? 40: 0}
      >      
      <PageHeader title='ChatBot' showHeaderRight={false} bgColor='#F5F5F5'/>
      <View
        className='flex-1 justify-between bg-neutral-100 overflow-visible pb-20'
      >
        <View className='flex-1'>
          <MessageList
            messages={messages}
            isTyping={isTyping}
          />
        </View>
        <View>
          <View className='flex-row justify-between mx-3 mb-3 border p-2 bg-white border-neutral-300 rounded-full pl-5'>
            <TextInput
                ref={inputRef}
                onChangeText={value => textRef.current = value}
                placeholder='Type a message...'
                style={{fontSize: hp(1.5)}}
                className='flex-1 mr-2'
            />
            <TouchableOpacity 
              className='bg-neutral-200 p-3 mr-[2px] rounded-full'
              onPress={handleSendMessage}
            >
              <Feather name='send' size={hp(2.6)} color='#737373'/>
            </TouchableOpacity>
          </View>
        </View>

      </View>
      </KeyboardAvoidingView>
    </GestureHandlerRootView>
  )
}

export default ChatRoom