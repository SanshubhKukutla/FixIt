import { chatConfig } from '../config/chatConfig';

export const nlxService = {
    async startConversation() {
        try {
            const response = await fetch(chatConfig.botUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...chatConfig.headers
                }
            });
            const data = await response.json();
            return data.conversationId;
        } catch (error) {
            console.error('Error starting conversation:', error);
            throw error;
        }
    },

    async sendMessage(conversationId, message) {
        try {
            const response = await fetch(`${chatConfig.botUrl}/messages`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...chatConfig.headers
                },
                body: JSON.stringify({
                    type: 'text',
                    text: message,
                }),
            });
            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }
};