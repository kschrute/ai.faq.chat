import { forwardRef, useState } from "react";

interface MessageInputProps {
	isLoading: boolean;
	onSendMessage: (message: string) => Promise<void>;
}

const MessageInput = forwardRef<HTMLInputElement, MessageInputProps>(
	(props, ref) => {
		const { isLoading, onSendMessage } = props;
		const [input, setInput] = useState("");

		const onChange = (e: React.ChangeEvent<HTMLInputElement>) =>
			setInput(e.target.value);

		const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
			e.preventDefault();
			if (!input.trim()) return;
			setInput("");
			await onSendMessage(input.trim());
		};

		return (
			<div className="p-5">
				<form className="relative" onSubmit={onSubmit}>
					<input
						ref={ref}
						autoComplete="off"
						className="w-full px-4 py-2 pr-12 text-md rounded-3xl border disabled:opacity-50 focus:outline-none focus:ring-1 border-gray-300 focus:ring-gray-500 focus:border-gray-500 dark:border-gray-500 dark:focus:ring-gray-300 dark:focus:border-gray-300"
						placeholder="Type your question or ask me for the list of available questions."
						disabled={isLoading}
						value={input}
						onChange={onChange}
					/>
					<button
						type="submit"
						aria-label="Send"
						className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 disabled:opacity-50"
						disabled={isLoading}
					>
						<div className="i-lucide-corner-down-left cursor-pointer text-gray-900 dark:text-gray-100" />
					</button>
				</form>
			</div>
		);
	},
);

export default MessageInput;
