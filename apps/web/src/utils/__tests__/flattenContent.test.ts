import { describe, it, expect, vi, beforeEach } from "vitest";
import { flattenContent } from "../flattenContent";

// Use the real implementation for these tests
vi.unmock("@/utils");

describe("flattenContent", () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	it("should return undefined for undefined input", () => {
		expect(flattenContent(undefined)).toBeUndefined();
	});

	it("should return string as-is for string input", () => {
		const input = "Hello, world!";
		expect(flattenContent(input)).toBe(input);
	});

	it("should join array of strings with newlines", () => {
		const input = ["Line 1", "Line 2", "Line 3"];
		expect(flattenContent(input)).toBe("Line 1\nLine 2\nLine 3");
	});

	it("should handle empty array", () => {
		const input: string[] = [];
		expect(flattenContent(input)).toBe("");
	});

	it("should extract text from text object", () => {
		const input = {
			type: "text" as const,
			text: "Here's an image:" as const,
		};
		expect(flattenContent(input)).toBe("Here's an image:");
	});

	it("should extract URL from image_url object", () => {
		const input = {
			type: "image_url" as const,
			image_url: { url: "https://example.com/image.jpg" },
		};
		expect(flattenContent(input)).toBe("https://example.com/image.jpg");
	});

	it("should return undefined for text object without text", () => {
		const input = {
			type: "text" as const,
		};
		expect(flattenContent(input)).toBeUndefined();
	});

	it("should return undefined for image_url object without image_url", () => {
		const input = {
			type: "image_url" as const,
		};
		expect(flattenContent(input)).toBeUndefined();
	});

	it("should return undefined for image_url object without URL", () => {
		const input = {
			type: "image_url" as const,
			image_url: undefined,
		};
		expect(flattenContent(input)).toBeUndefined();
	});

	it("should return undefined for unknown object type", () => {
		const input = {
			type: "text" as const,
		};
		expect(flattenContent(input)).toBeUndefined();
	});
});
