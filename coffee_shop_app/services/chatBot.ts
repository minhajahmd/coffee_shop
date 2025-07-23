import axios from 'axios';
import { MessageInterface } from '@/types/types';
import { API_KEY, API_URL } from '@/config/runpod.config';

async function callChatBotAPI(messages: MessageInterface[]): Promise<MessageInterface> {
    try {
        const response = await axios.post(API_URL, {
            // Define the input structure expected by the API
            input: { messages }
        }, {
            // Set the headers for the request
            headers: {
                'Content-Type': 'application/json',         // Specify the content type
                'Authorization': `Bearer ${API_KEY}`        // Include the API key for authorization
            }
        });
        
        let output = response.data;         // Extract the output from the response
        let outputMessage: MessageInterface = output['output'];         // Get the output message from the response

        return outputMessage;
    } catch (error) {
        console.error('Error calling the API:', error);
        throw error;
    }
}

export { callChatBotAPI };