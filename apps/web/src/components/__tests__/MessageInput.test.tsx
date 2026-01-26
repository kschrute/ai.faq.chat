import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import MessageInput from "../MessageInput";

describe("MessageInput", () => {
	const mockOnSendMessage = vi.fn();

	beforeEach(() => {
		vi.clearAllMocks();
	});

	it("should render input field and send button", () => {
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);
		const button = screen.getByRole("button", { name: "Send message" });

		expect(input).toBeInTheDocument();
		expect(button).toBeInTheDocument();
	});

	it("should allow typing in the input field", async () => {
		const user = userEvent.setup();
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);

		await user.type(input, "Hello world");

		expect(input).toHaveValue("Hello world");
	});

	it("should call onSendMessage when form is submitted with valid input", async () => {
		const user = userEvent.setup();
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);
		const button = screen.getByRole("button", { name: "Send message" });

		await user.type(input, "Test message");
		await user.click(button);

		expect(mockOnSendMessage).toHaveBeenCalledWith("Test message");
		expect(input).toHaveValue(""); // Input should be cleared
	});

	it("should call onSendMessage when Enter key is pressed", async () => {
		const user = userEvent.setup();
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);

		await user.type(input, "Test message{enter}");

		expect(mockOnSendMessage).toHaveBeenCalledWith("Test message");
		expect(input).toHaveValue(""); // Input should be cleared
	});

	it("should not call onSendMessage when input is empty", async () => {
		const user = userEvent.setup();
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const button = screen.getByRole("button", { name: "Send message" });

		await user.click(button);

		expect(mockOnSendMessage).not.toHaveBeenCalled();
	});

	it("should not call onSendMessage when input contains only whitespace", async () => {
		const user = userEvent.setup();
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);
		const button = screen.getByRole("button", { name: "Send message" });

		await user.type(input, "   ");
		await user.click(button);

		expect(mockOnSendMessage).not.toHaveBeenCalled();
	});

	it("should disable input and button when loading", () => {
		render(<MessageInput isLoading={true} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);
		const button = screen.getByRole("button", { name: "Send message" });

		expect(input).toBeDisabled();
		expect(button).toBeDisabled();
	});

	it("should disable send button when input is empty", () => {
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const button = screen.getByRole("button", { name: "Send message" });

		expect(button).toBeDisabled();
	});

	it("should enable send button when input has text", async () => {
		const user = userEvent.setup();
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);
		const button = screen.getByRole("button", { name: "Send message" });

		expect(button).toBeDisabled();

		await user.type(input, "Test");

		expect(button).not.toBeDisabled();
	});

	it("should trim whitespace from message before sending", async () => {
		const user = userEvent.setup();
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);

		await user.type(input, "  Test message with spaces  ");
		await user.click(screen.getByRole("button", { name: "Send message" }));

		expect(mockOnSendMessage).toHaveBeenCalledWith("Test message with spaces");
	});

	it("should not submit if already loading", () => {
		render(<MessageInput isLoading={true} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByPlaceholderText(
			"Type your question or ask me for the list of available questions."
		);
		const button = screen.getByRole("button", { name: "Send message" });

		// Even if we could type (which we can't when disabled), it shouldn't submit
		expect(input).toBeDisabled();
		expect(button).toBeDisabled();
	});

	it("should have proper accessibility attributes", () => {
		render(<MessageInput isLoading={false} onSendMessage={mockOnSendMessage} />);

		const input = screen.getByRole("textbox");
		const button = screen.getByRole("button", { name: "Send message" });

		expect(input).toHaveAttribute("autoComplete", "off");
		expect(input).toHaveAttribute("type", "text");
		expect(button).toHaveAttribute("aria-label", "Send message");
	});
});
