import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import Header from "../Header";

describe("Header", () => {
	it("should render the header with correct text", () => {
		render(<Header />);

		const heading = screen.getByRole("heading", { level: 1 });
		expect(heading).toBeInTheDocument();
		expect(heading).toHaveTextContent("FAQ Chat");
	});

	it("should have correct styling classes", () => {
		render(<Header />);

		const heading = screen.getByRole("heading", { level: 1 });
		expect(heading).toHaveClass(
			"m-10",
			"text-5xl",
			"font-bold",
			"text-center",
			"bg-gradient-to-r",
			"from-cyan-400",
			"to-blue-400",
			"text-transparent",
			"bg-clip-text"
		);
	});

	it("should be an h1 element", () => {
		render(<Header />);

		const heading = screen.getByRole("heading", { level: 1 });
		expect(heading.tagName).toBe("H1");
	});

	it("should have correct displayName", () => {
		expect(Header.displayName).toBe("Header");
	});

	it("should have whyDidYouRender configuration", () => {
		expect(Header.whyDidYouRender).toEqual({
			collapseGroups: true,
			logOnDifferentValues: true,
			onlyLogs: true,
			trackAllPureComponents: true,
			trackHooks: true,
		});
	});
});
