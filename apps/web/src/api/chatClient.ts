import type { ChatCompletionResponse, ChatMessage } from "@/types";

const API_BASE = import.meta.env.VITE_API_URL || window.location.origin;

export class ApiError extends Error {
	status: number;

	constructor(message: string, status: number) {
		super(message);
		this.name = "ApiError";
		this.status = status;
	}
}

/**
 * Send a chat request to the FAQ API.
 *
 * @param messages - Array of chat messages to send
 * @returns The chat completion response
 * @throws ApiError if the request fails
 */
export async function sendChatRequest(
	messages: ChatMessage[]
): Promise<ChatCompletionResponse> {
	const response = await fetch(`${API_BASE}/chat`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			model: "faq-chat",
			messages,
		}),
	});

	if (!response.ok) {
		throw new ApiError(
			`API request failed: ${response.statusText}`,
			response.status
		);
	}

	return response.json();
}

/**
 * Build a user message object for the chat API.
 */
export function buildUserMessage(content: string): ChatMessage {
	return {
		id: crypto.randomUUID(),
		role: "user",
		content,
	};
}

/**
 * Convert chat history to API format, filtering out system messages.
 */
export function formatHistoryForApi(history: ChatMessage[]): ChatMessage[] {
	return history
		.filter((msg) => msg.role !== "system" && msg.content)
		.map((msg) => ({
			id: crypto.randomUUID(),
			role: msg.role as "user" | "assistant",
			content:
				typeof msg.content === "string" ? msg.content : JSON.stringify(msg.content),
		}));
}
