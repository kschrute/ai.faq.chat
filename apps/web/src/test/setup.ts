import "@testing-library/jest-dom";
import { vi } from "vitest";
import type {
	ChatCompletionResponse,
	ChatMessage,
	ChatMessageContent,
} from "@/types";

// Mock crypto.randomUUID for test environment
Object.defineProperty(globalThis, "crypto", {
	value: {
		randomUUID: () => "test-uuid-" + Math.random().toString(36).substr(2, 9),
	},
});

// Mock window.location.origin
Object.defineProperty(window, "location", {
	value: {
		origin: "http://localhost:3000",
	},
	writable: true,
});

// Mock import.meta.env
vi.mock("vite", () => ({
	default: {
		env: {
			VITE_API_URL: undefined,
		},
	},
}));

// Create a mock for the entire utils module
const mockFetchResponse =
	vi.fn<
		(message: string, history?: ChatMessage[]) => Promise<ChatCompletionResponse>
	>();
const mockFlattenContent =
	vi.fn<(content: ChatMessageContent | undefined) => string | undefined>();

vi.mock("@/utils", () => ({
	fetchResponse: mockFetchResponse,
	flattenContent: mockFlattenContent,
}));

export { mockFetchResponse, mockFlattenContent };
