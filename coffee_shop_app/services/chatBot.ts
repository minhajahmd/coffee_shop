import axios from 'axios';
import { MessageInterface } from '@/types/types';
import { API_URL, API_KEY } from '@/config/runpod.config';


const HEADERS = {
  // Set the headers for the API request
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${API_KEY}`,
};

// Polling configuration
const POLL_INTERVAL_MS = 2000; // Wait 2 seconds between each check
const MAX_POLL_ATTEMPTS = 30;  // wait max 1 minute

/**
 * This function keeps checking the chatbot's status until it's ready.
 * It checks once every 2 seconds, up to 30 times.
 */
async function pollUntilComplete(taskId: string): Promise<MessageInterface> {
  for (let i = 0; i < MAX_POLL_ATTEMPTS; i++) {
    console.log(`Polling attempt ${i + 1}/${MAX_POLL_ATTEMPTS}...`);

    // Call the API to check the status of the task using its ID
    const pollResponse = await axios.get(`${API_URL}/status/${taskId}`, {
    headers: HEADERS,
    });


    const data = pollResponse.data;
    console.log('Polling response:', data);

    // If the status is COMPLETED and content is present, return it
    if (data.status === 'COMPLETED' && data.output?.content && data.output?.role) {
      return {
        content: data.output.content,
        role: data.output.role,
      };
    }

    // If still in progress, wait and retry
    await new Promise(res => setTimeout(res, POLL_INTERVAL_MS));
  }

  // If we reach here, it means the task did not complete in time
  throw new Error('Timed out waiting for chatbot response.');
}

// Function to call the chatbot API
async function callChatBotAPI(messages: MessageInterface[]): Promise<MessageInterface> {
  try {
    //send user's messages to the API
    const response = await axios.post(
      API_URL,
      { input: { messages } }, // Send the messages history
      { headers: HEADERS }
    );

    const data = response.data;
    console.log('Initial API response:', data);

    // If the response is already ready, return it
    if (data.status === 'COMPLETED' && data.output?.content && data.output?.role) {
      return {
        content: data.output.content,
        role: data.output.role,
      };
    }

    // If the response is still processing, keep checking until it's ready
    if (data.status === 'IN_PROGRESS' && data.id) {
      return await pollUntilComplete(data.id);
    }

    // If none of the above matched, return a fallback error message
    return {
      content: 'Unexpected API response. Try again.',
      role: 'assistant',
    };
  } catch (error) {
    console.error('API error:', error);
    return {
      content: 'Failed to contact the assistant.',
      role: 'assistant',
    };
  }
}

export { callChatBotAPI };
