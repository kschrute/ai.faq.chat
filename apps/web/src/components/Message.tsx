import React from "react";
import TypingIndicator from "./TypingIndicator";

export type ChatMessage = {
  id: number;
  direction: "in" | "out";
  text?: string;
};

const Message = React.memo((message: ChatMessage) => {
  const { direction, text } = message;

  const className = `${
    direction === "out"
      ? "self-end text-white bg-blue-500 dark:bg-blue-400"
      : "self-start bg-gray-200 dark:bg-gray-700"
  } min-w-1/12 max-w-10/12 mb-3 px-4 py-2 rounded-2xl whitespace-pre-wrap`;

  return (
    <div className={className}>
      {text || <TypingIndicator isTyping={true} />}
    </div>
  );
});

export default Message;
