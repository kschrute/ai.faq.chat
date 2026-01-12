export default async function fetchAnswer(question: string) {
    try {
        const baseUrl = import.meta.env.VITE_API_URL || window.location.origin;
        const response = await fetch(`${baseUrl}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		const data = await response.json();
		// Parse OpenAI chat API format
		const content = data.choices?.[0]?.message?.content;
		return content || null;
	} catch (error) {
		console.error("API error:", error);
		throw error;
	}
}
