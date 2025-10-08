import { useCallback, useEffect, useRef, useState } from "react";
import Header from "./Header";
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
    <div className="flex flex-col p-0 sm:p-5 max-w-3xl w-screen h-dvh sm:w-auto sm:h-180 sm:min-h-0 sm:max-h-dvh sm:min-w-lg md:min-w-3xl">
      <div className="hidden sm:block">
        <Header />
      </div>
      <div className="bg-gray-800 flex flex-col flex-1 rounded-xl overflow-y-auto shadow-[0px_0px_42px_rgba(0,0,0,0.25)]">
        <Messages isLoading={isLoading} messages={messages} ref={messagesRef} />
        <MessageInput
          isLoading={isLoading}
          ref={inputRef}
          onSendMessage={onSendMessage}
        />
      </div>
    </div>
  );
}
