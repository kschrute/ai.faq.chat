import type { ChatMessageContent } from "@/types";

export const flattenContent = (
	content: ChatMessageContent | undefined,
): string | undefined => {
	if (!content) {
		return content;
	}

	if (typeof content === "string") {
		return content;
	}

	if (Array.isArray(content)) {
		return content?.join("\n");
	}

	if (content.type === "text" && content.text) {
		return content.text;
	}

	if (content.type === "image_url" && content.image_url) {
		return content.image_url.url;
	}

	return undefined;
};
