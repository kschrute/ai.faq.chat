import type { ChatCompletionResponse, ChatMessage } from "@/types";
import {
	buildUserMessage,
	formatHistoryForApi,
	sendChatRequest,
} from "@/api/chatClient";

export const fetchResponse = async (
	message: string,
	history?: ChatMessage[]
): Promise<ChatCompletionResponse> => {
	const messages = [
		...(history ? formatHistoryForApi(history) : []),
		buildUserMessage(message),
	];

	return sendChatRequest(messages);
};
