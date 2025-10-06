import { useCallback, useEffect, useRef, useState } from "react";
import Messages from "./Messages";
import MessageInput from "./MessageInput";
import fetchAnswer from "../utils/fetchAnswer";
import type { ChatMessage } from "./Message";

export default function Chat() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      direction: "in",
      text: "Hi there! Please ask anything you'd like to know. And I'll answer if your question is in the FAQ.",
    },
  ]);

  useEffect(() => {
    if (!isLoading) {
      inputRef?.current?.focus();
    }
  }, [isLoading]);

  useEffect(() => {
    if (messages) {
      scrollToBottom();
    }
  }, [messages]);

  const addMessage = useCallback((text: string, direction: "in" | "out") => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { id: Date.now(), text, direction },
    ]);
  }, []);

  const onSendMessage = async (message: string) => {
    addMessage(message, "out");
    setIsLoading(true);
    const answer = await fetchAnswer(message);
    setIsLoading(false);
    addMessage(answer || "This question is not in the FAQ.", "in");
  };

  const scrollToBottom = () =>
    messagesRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
      inline: "nearest",
    });

  return (
    <div className="bg-gray-800 max-w-3xl mx-auto p-2 w-xl rounded-xl shadow-[0px_0px_42px_rgba(0,0,0,0.25)]">
      <Messages
        isLoading={isLoading}
        messages={messages}
        ref={messagesRef}
      />
      <MessageInput
        isLoading={isLoading}
        ref={inputRef}
        onSendMessage={onSendMessage}
      />
    </div>
  );
}
