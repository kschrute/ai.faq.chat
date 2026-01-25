import type { ChatCompletionResponse, ChatMessage } from "@/types";

const API_TIMEOUT = 30000; // 30 seconds

export const fetchResponse = async (
	message: string,
	history?: ChatMessage[]
): Promise<ChatCompletionResponse> => {
	const controller = new AbortController();
	const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

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
			signal: controller.signal,
		});

		if (!response.ok) {
			const errorText = await response.text();
			throw new Error(`HTTP ${response.status}: ${errorText}`);
		}

		const data = await response.json();
		return data;
	} catch (error) {
		if (error instanceof Error && error.name === "AbortError") {
			throw new Error("Request timeout. Please try again.");
		}
		console.error("API error:", error);
		throw error;
	} finally {
		clearTimeout(timeoutId);
	}
};
