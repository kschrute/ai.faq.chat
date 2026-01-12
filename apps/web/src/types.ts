export type ChatRole = "user" | "assistant" | "developer" | "system";

export type ChatMessageContent =
	| string
	| string[]
	| {
			type: "text" | "image_url";
			text?: "Here's an image:";
			image_url?: { url: string };
	  };

export type ChatMessage = {
	id: string;
	role: ChatRole;
	content?: ChatMessageContent;
	metadata?: Record<string, unknown> | null;
	options?: Record<string, unknown> | null;
};

export type ChatRequest = {
	model: string;
	messages: Array<ChatMessage>;
	temperature?: number; // optional (0–2, default 1)
	max_tokens?: number; // optional – hard limit on output tokens
	top_p?: number; // optional (nucleus sampling)
	stream?: boolean; // optional – true for streaming response
	response_format?: { type: "json_object" }; // optional – for JSON mode
	seed?: number; // optional – for more reproducible outputs
};

type ChatCompletionChoice = {
	index: number;
	message: ChatMessage;
	finish_reason: "stop" | "length" | "content_filter" | "null";
};

export type ChatCompletionResponse = {
	id: string;
	object: "chat.completion";
	created: number;
	model: string;
	choices: Array<ChatCompletionChoice>;
};
