import type { APIResponse, ChatMessage } from "@/types";

export default async function fetchResponse(
	message: string,
	history?: ChatMessage[],
): Promise<APIResponse> {
	try {
		const sanitizedHistory = history
			?.filter(({ role }) => role !== "system")
			.map(({ role, content }) => ({
				role,
				content,
			}));
		const baseUrl = import.meta.env.VITE_API_URL || window.location.origin;
		const response = await fetch(`${baseUrl}/chat`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ message, history: sanitizedHistory }),
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
}
