import type React from "react";
import { memo } from "react";

interface TypingIndicatorProps {
	isTyping: boolean;
	senderName?: string;
}

const TypingDot = memo(
	({ className, ...rest }: React.HTMLAttributes<HTMLDivElement>) => (
		<div
			className={`typing-dot animate-bounce bg-gray-700 dark:bg-gray-200 w-[6px] h-[6px] rounded-full ${className}`}
			{...rest}
		/>
	)
);

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ isTyping }) => {
	if (!isTyping) return null;

	return (
		<div className="flex flex-row gap-1 py-2">
			<TypingDot />
			<TypingDot style={{ animationDelay: "0.2s" }} />
			<TypingDot style={{ animationDelay: "0.4s" }} />
		</div>
	);
};

TypingIndicator.displayName = "TypingIndicator";

export default TypingIndicator;
