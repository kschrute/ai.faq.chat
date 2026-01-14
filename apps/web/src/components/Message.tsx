import React, { useMemo } from "react";
import TypingIndicator from "./TypingIndicator";
import { flattenContent } from "@/utils";
import type { ChatMessage } from "@/types";

const Message = React.memo(({ message }: { message: ChatMessage }) => {
	const { role, content } = message;

	const result = useMemo(() => flattenContent(content), [content]);

	const className = `${
		role === "user"
			? "self-end text-white bg-blue-500 dark:bg-blue-400"
			: "self-start bg-gray-200 dark:bg-gray-700 dark:text-gray-100"
	} min-w-1/12 max-w-10/12 mb-3 px-4 py-2 rounded-2xl whitespace-pre-wrap`;

	return (
		<div className={className}>
			{result === undefined && <TypingIndicator isTyping={true} />}
			{result !== undefined && result}
		</div>
	);
});

export default Message;
