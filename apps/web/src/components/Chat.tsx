import { useCallback, useEffect, useRef, useState } from "react";
import Messages from "./Messages";
import MessageInput from "./MessageInput";
import { fetchResponse, flattenContent } from "@/utils";
import type { ChatMessage } from "@/types";

export default function Chat() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const messagesRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "system-1",
      role: "system",
      content:
        "Hi there! Please ask anything you'd like to know. I'll answer if your question is similar enough to one of the questions on the FAQ list.",
    },
    {
      id: "system-2",
      role: "system",
      content:
        'You can ask something like "How do I reset my password?" or just "Password reset".',
    },
  ]);

  useEffect(() => {
    if (!isLoading) {
      inputRef?.current?.focus();
    }
  }, [isLoading]);

  const scrollToBottom = useCallback(() => {
    messagesRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
      inline: "nearest",
    });
  }, []);

  useEffect(() => {
    if (messages) {
      scrollToBottom();
    }
  }, [messages, scrollToBottom]);

  const addMessage = useCallback(
    (message: Pick<ChatMessage, "content" | "role">) => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { ...message, id: crypto.randomUUID() },
      ]);
    },
    []
  );

  const onSendMessage = useCallback(
    async (message: string) => {
      addMessage({
        content: message,
        role: "user",
      });

      setIsLoading(true);

      try {
        const res = await fetchResponse(message, messages);
        setIsLoading(false);

        const content = res.choices?.[0]?.message?.content;
        addMessage({
          content:
            flattenContent(content) ||
            'This question is not in the FAQ. Type in "Questions list" to see the list.',
          role: "assistant",
        });
      } catch (error: unknown) {
        setIsLoading(false);
        addMessage({
          content:
            error instanceof Error ? error.message : "Something went wrong",
          role: "assistant",
        });
      }
    },
    [addMessage, messages]
  );

  return (
    <div className="flex flex-col p-0 sm:p-5 max-w-3xl w-screen h-dvh sm:w-auto sm:h-180 sm:min-h-0 sm:max-h-dvh sm:min-w-lg md:min-w-3xl">
      <div className="flex flex-col flex-1 rounded-xl overflow-y-auto shadow-[0px_0px_42px_rgba(0,0,0,0.2)] bg-zinc-100 dark:bg-gray-800">
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
