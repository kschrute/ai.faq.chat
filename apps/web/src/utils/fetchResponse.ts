import type { ChatCompletionResponse, ChatMessage } from "@/types";

export const fetchResponse = async (
	message: string,
	history?: ChatMessage[]
): Promise<ChatCompletionResponse> => {
	try {
		// Build messages array in OpenAI format
		const messages: Array<ChatMessage> = [];

		// Add history messages (excluding system messages)
		if (history) {
			for (const msg of history) {
				if (msg.role !== "system" && msg.content) {
					const content =
						typeof msg.content === "string"
							? msg.content
							: JSON.stringify(msg.content);
					messages.push({
						id: crypto.randomUUID(),
						role: msg.role as "user" | "assistant",
						content,
					});
				}
			}
		}

		// Add current user message
		messages.push({
			id: crypto.randomUUID(),
			role: "user",
			content: message,
		});

		const baseUrl = import.meta.env.VITE_API_URL || window.location.origin;
		const response = await fetch(`${baseUrl}/chat`, {
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
			throw new Error("Network response was not ok");
		}
		const data = await response.json();
		return data;
	} catch (error) {
		console.error("API error:", error);
		throw error;
	}
};
