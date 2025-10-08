import { forwardRef } from "react";
import Message, { type ChatMessage } from "./Message";

interface MessagesProps {
  isLoading: boolean;
  messages: ChatMessage[];
}

const Messages = forwardRef<HTMLDivElement, MessagesProps>((props, ref) => {
  const { isLoading, messages } = props;

  return (
    <div className="flex-1 p-5 overflow-y-auto">
      {messages.map((message) => (
        <Message
          id={message.id}
          key={message.id}
          text={message.text}
          direction={message.direction}
        />
      ))}
      {isLoading && <Message id={1} direction="in" />}
      <div ref={ref} />
    </div>
  );
});

export default Messages;
