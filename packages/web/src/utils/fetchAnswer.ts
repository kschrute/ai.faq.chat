export default async function fetchAnswer(question: string) {
	try {
		const response = await fetch("http://localhost:8000/ask", {
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
		return data.answer;
	} catch (error) {
		console.error("API error:", error);
		throw error;
	}
}
