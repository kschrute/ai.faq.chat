import { forwardRef } from "react";
import Message from "./Message";
import type { ChatMessage } from "@/types";

interface MessagesProps {
  isLoading: boolean;
  messages: Array<ChatMessage>;
}

const Messages = forwardRef<HTMLDivElement, MessagesProps>((props, ref) => {
  const { isLoading, messages } = props;

  return (
    <div className="flex flex-col flex-1 p-5 pb-0 w-full overflow-y-auto">
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
      {isLoading && <Message message={{ id: "loading", role: "assistant" }} />}
      <div ref={ref} />
    </div>
  );
});

export default Messages;
