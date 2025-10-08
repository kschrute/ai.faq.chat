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
      ? "bg-blue-500 justify-self-end"
      : "bg-zinc-500 justify-self-start"
  } min-w-3/12 max-w-10/12 mb-3 px-4 py-2 rounded-2xl`;

  return (
    <div className={className}>
      {text || <TypingIndicator isTyping={true} />}
    </div>
  );
});

export default Message;
