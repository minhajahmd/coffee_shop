import axios from 'axios';
import { MessageInterface } from '@/types/types';
import { API_URL, API_KEY } from '@/config/runpod.config';

async function callChatBotAPI(messages: MessageInterface[]): Promise<MessageInterface> {
  try {
    // Send user's messages to the chatbot server
    const response = await axios.post(
      API_URL,
      { input: {messages} },   // sending the message history
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`,
        },
      }
    );

    const data = response.data;

    console.log('Raw API response:', JSON.stringify(data, null, 2)); // 🔍 log everything

    const output = data?.output;

    if (
      output &&
      typeof output.content === 'string' &&
      typeof output.role === 'string'
    ) {
      const outputMessage: MessageInterface = {
        content: output.content,
        role: output.role,
      };
      console.log('Chatbot formatted response:', outputMessage);
      return outputMessage;
    } else {
      console.warn('⚠️ Unexpected response structure:', data);
      return {
        content: 'Hmm, I did not get a valid response. Please try again.',
        role: 'assistant',
      };
    }

  } catch (error) {
    console.error('API error:', error);
    return {
      content: 'There was a problem reaching the assistant.',
      role: 'assistant',
    };
  }
}

export { callChatBotAPI };
