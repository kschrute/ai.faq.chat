import { describe, it, expect, vi, beforeEach } from "vitest";
import { fetchResponse } from "../fetchResponse";
import type { ChatMessage } from "@/types";

// Mock fetch
const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

// Mock import.meta.env
vi.mock("vite", () => ({
	default: {
		env: {
			VITE_API_URL: undefined,
		},
	},
}));

// Use the real implementation for these tests
vi.unmock("@/utils");

describe("fetchResponse", () => {
	beforeEach(() => {
		vi.clearAllMocks();
		mockFetch.mockClear();
	});

	it("should send correct request format", async () => {
		const mockResponse = {
			ok: true,
			json: vi.fn().mockResolvedValue({
				id: "test-id",
				object: "chat.completion",
				created: Date.now(),
				model: "faq-chat",
				choices: [
					{
						index: 0,
						message: { role: "assistant", content: "Test response" },
						finish_reason: "stop",
					},
				],
			}),
		};
		mockFetch.mockResolvedValue(mockResponse);

		const message = "How do I reset my password?";
		const history: ChatMessage[] = [
			{ id: "1", role: "user", content: "Previous question" },
			{ id: "2", role: "assistant", content: "Previous answer" },
			{ id: "3", role: "system", content: "System message" }, // Should be filtered out
		];

		await fetchResponse(message, history);

		expect(mockFetch).toHaveBeenCalledWith(
			"http://localhost:3000/chat",
			expect.objectContaining({
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				signal: expect.any(AbortSignal),
			})
		);

		// Parse the body to check structure
		const requestBody = JSON.parse(mockFetch.mock.calls[0][1].body);
		expect(requestBody).toEqual({
			model: "faq-chat",
			messages: expect.arrayContaining([
				expect.objectContaining({ role: "user", content: "Previous question" }),
				expect.objectContaining({ role: "assistant", content: "Previous answer" }),
				expect.objectContaining({ role: "user", content: message }),
			]),
		});
		expect(requestBody.messages).toHaveLength(3);
	});

	it("should handle successful response", async () => {
		const expectedResponse = {
			id: "test-id",
			object: "chat.completion",
			created: Date.now(),
			model: "faq-chat",
			choices: [
				{
					index: 0,
					message: { role: "assistant", content: "Test response" },
					finish_reason: "stop",
				},
			],
		};

		mockFetch.mockResolvedValue({
			ok: true,
			json: vi.fn().mockResolvedValue(expectedResponse),
		});

		const result = await fetchResponse("Test message");

		expect(result).toEqual(expectedResponse);
	});

	it("should handle HTTP error responses", async () => {
		mockFetch.mockResolvedValue({
			ok: false,
			status: 500,
			text: vi.fn().mockResolvedValue("Internal Server Error"),
		});

		await expect(fetchResponse("Test message")).rejects.toThrow(
			"HTTP 500: Internal Server Error"
		);
	});

	it("should handle network errors", async () => {
		const networkError = new Error("Network error");
		mockFetch.mockRejectedValue(networkError);

		await expect(fetchResponse("Test message")).rejects.toThrow("Network error");
	});

	it("should handle request timeout", async () => {
		// Create a mock that aborts
		const abortError = new Error("Request timeout");
		abortError.name = "AbortError";
		mockFetch.mockRejectedValue(abortError);

		await expect(fetchResponse("Test message")).rejects.toThrow(
			"Request timeout. Please try again."
		);
	});

	it("should work without history", async () => {
		const expectedResponse = {
			id: "test-id",
			object: "chat.completion",
			created: Date.now(),
			model: "faq-chat",
			choices: [
				{
					index: 0,
					message: { role: "assistant", content: "Test response" },
					finish_reason: "stop",
				},
			],
		};

		mockFetch.mockResolvedValue({
			ok: true,
			json: vi.fn().mockResolvedValue(expectedResponse),
		});

		await fetchResponse("Test message");

		expect(mockFetch).toHaveBeenCalledWith(
			"http://localhost:3000/chat",
			expect.objectContaining({
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				signal: expect.any(AbortSignal),
			})
		);

		// Parse the body to check structure
		const requestBody = JSON.parse(mockFetch.mock.calls[0][1].body);
		expect(requestBody).toEqual({
			model: "faq-chat",
			messages: expect.arrayContaining([
				expect.objectContaining({ role: "user", content: "Test message" }),
			]),
		});
		expect(requestBody.messages).toHaveLength(1);
	});

	it("should filter out system messages from history", async () => {
		const history: ChatMessage[] = [
			{ id: "1", role: "system", content: "System message" },
			{ id: "2", role: "user", content: "User message" },
			{ id: "3", role: "assistant", content: "Assistant message" },
			{ id: "4", role: "system", content: "Another system message" },
		];

		mockFetch.mockResolvedValue({
			ok: true,
			json: vi.fn().mockResolvedValue({
				id: "test-id",
				object: "chat.completion",
				created: Date.now(),
				model: "faq-chat",
				choices: [],
			}),
		});

		await fetchResponse("New message", history);

		const requestBody = JSON.parse(mockFetch.mock.calls[0][1].body);
		expect(requestBody.messages).toHaveLength(3); // user + assistant + new message
		expect(requestBody.messages.map((m: ChatMessage) => m.role)).toEqual([
			"user",
			"assistant",
			"user",
		]);
	});

	it("should handle complex content objects in history", async () => {
		const history: ChatMessage[] = [
			{
				id: "1",
				role: "user",
				content: { type: "text", text: "Here's an image:" },
			},
			{
				id: "2",
				role: "assistant",
				content: ["Line 1", "Line 2"],
			},
		];

		mockFetch.mockResolvedValue({
			ok: true,
			json: vi.fn().mockResolvedValue({
				id: "test-id",
				object: "chat.completion",
				created: Date.now(),
				model: "faq-chat",
				choices: [],
			}),
		});

		await fetchResponse("New message", history);

		const requestBody = JSON.parse(mockFetch.mock.calls[0][1].body);
		expect(requestBody.messages[0].content).toBe(
			'{"type":"text","text":"Here\'s an image:"}'
		);
		expect(requestBody.messages[1].content).toBe('["Line 1","Line 2"]');
	});
});
