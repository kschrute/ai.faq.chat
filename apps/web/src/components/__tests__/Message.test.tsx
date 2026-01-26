import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import Message from "../Message";
import type { ChatMessage } from "@/types";

// Mock the flattenContent utility
vi.mock("@/utils", () => ({
	flattenContent: vi.fn(),
}));

// Mock the TypingIndicator component
vi.mock("../TypingIndicator", () => ({
	default: ({ isTyping }: { isTyping: boolean }) => (
		<div data-testid="typing-indicator" data-typing={isTyping}>
			Typing...
		</div>
	),
}));

import { flattenContent } from "@/utils";

describe("Message", () => {
	it("should render user message with correct styling", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("Hello world");

		const userMessage: ChatMessage = {
			id: "1",
			role: "user",
			content: "Hello world",
		};

		render(<Message message={userMessage} />);

		const messageElement = screen.getByText("Hello world");
		expect(messageElement).toBeInTheDocument();
		expect(messageElement).toHaveClass(
			"self-end",
			"text-white",
			"bg-blue-500",
			"dark:bg-blue-400"
		);
	});

	it("should render assistant message with correct styling", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("I am an assistant");

		const assistantMessage: ChatMessage = {
			id: "2",
			role: "assistant",
			content: "I am an assistant",
		};

		render(<Message message={assistantMessage} />);

		const messageElement = screen.getByText("I am an assistant");
		expect(messageElement).toBeInTheDocument();
		expect(messageElement).toHaveClass(
			"self-start",
			"bg-gray-200",
			"dark:bg-gray-700",
			"dark:text-gray-100"
		);
	});

	it("should render system message with correct styling", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("System message");

		const systemMessage: ChatMessage = {
			id: "3",
			role: "system",
			content: "System message",
		};

		render(<Message message={systemMessage} />);

		const messageElement = screen.getByText("System message");
		expect(messageElement).toBeInTheDocument();
		expect(messageElement).toHaveClass(
			"self-start",
			"bg-gray-200",
			"dark:bg-gray-700",
			"dark:text-gray-100"
		);
	});

	it("should render developer message with correct styling", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("Developer message");

		const developerMessage: ChatMessage = {
			id: "4",
			role: "developer",
			content: "Developer message",
		};

		render(<Message message={developerMessage} />);

		const messageElement = screen.getByText("Developer message");
		expect(messageElement).toBeInTheDocument();
		expect(messageElement).toHaveClass(
			"self-start",
			"bg-gray-200",
			"dark:bg-gray-700",
			"dark:text-gray-100"
		);
	});

	it("should show typing indicator when content is undefined", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue(undefined);

		const message: ChatMessage = {
			id: "5",
			role: "assistant",
			content: undefined,
		};

		render(<Message message={message} />);

		const typingIndicator = screen.getByTestId("typing-indicator");
		expect(typingIndicator).toBeInTheDocument();
		expect(typingIndicator).toHaveAttribute("data-typing", "true");
	});

	it("should show typing indicator when flattenContent returns undefined", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue(undefined);

		const message: ChatMessage = {
			id: "6",
			role: "user",
			content: "Some content",
		};

		render(<Message message={message} />);

		const typingIndicator = screen.getByTestId("typing-indicator");
		expect(typingIndicator).toBeInTheDocument();
		expect(typingIndicator).toHaveAttribute("data-typing", "true");
	});

	it("should not show typing indicator when content is defined", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("Defined content");

		const message: ChatMessage = {
			id: "7",
			role: "assistant",
			content: "Some content",
		};

		render(<Message message={message} />);

		expect(screen.queryByTestId("typing-indicator")).not.toBeInTheDocument();
		expect(screen.getByText("Defined content")).toBeInTheDocument();
	});

	it("should call flattenContent with message content", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("Flattened content");

		const message: ChatMessage = {
			id: "8",
			role: "user",
			content: "Original content",
		};

		render(<Message message={message} />);

		expect(mockFlattenContent).toHaveBeenCalledWith("Original content");
	});

	it("should have correct base styling classes", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("Test message");

		const message: ChatMessage = {
			id: "9",
			role: "user",
			content: "Test message",
		};

		render(<Message message={message} />);

		const messageElement = screen.getByText("Test message");
		expect(messageElement).toHaveClass(
			"min-w-1/12",
			"max-w-10/12",
			"mb-3",
			"px-4",
			"py-2",
			"rounded-2xl",
			"whitespace-pre-wrap"
		);
	});

	it("should handle empty string content", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("");

		const message: ChatMessage = {
			id: "10",
			role: "user",
			content: "",
		};

		const { container } = render(<Message message={message} />);

		const messageElement = container.querySelector('[class*="self-end"]');
		expect(messageElement).toBeInTheDocument();
		expect(messageElement).toHaveTextContent("");
		expect(screen.queryByTestId("typing-indicator")).not.toBeInTheDocument();
	});

	it("should handle complex content objects", () => {
		const mockFlattenContent = vi.mocked(flattenContent);
		mockFlattenContent.mockReturnValue("Processed complex content");

		const complexContent = {
			type: "text" as const,
			text: "Here's an image:" as const,
		};

		const message: ChatMessage = {
			id: "11",
			role: "assistant",
			content: complexContent,
		};

		render(<Message message={message} />);

		expect(mockFlattenContent).toHaveBeenCalledWith(complexContent);
		expect(screen.getByText("Processed complex content")).toBeInTheDocument();
	});
});
