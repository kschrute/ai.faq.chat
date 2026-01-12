export type ChatMessage = {
	id: number;
	role: "user" | "assistant" | "system";
	content?:
		| string
		| string[]
		| {
				type: "text" | "image_url";
				text?: "Here's an image:";
				image_url?: { url: string };
		  };
	metadata?: Record<string, unknown> | null;
	options?: Record<string, unknown> | null;
};

export type APIResponse = ChatMessage[];
