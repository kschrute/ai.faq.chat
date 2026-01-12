export default function isJSON(value: unknown) {
	// Fast-path common primitives
	if (value === null) return true;
	if (typeof value === "string") {
		try {
			JSON.parse(value);
			return true;
		} catch {
			return false;
		}
	}
	if (typeof value === "number" && Number.isFinite(value)) return true;
	if (typeof value === "boolean") return true;

	// For objects/arrays: attempt to stringify
	if (typeof value === "object") {
		try {
			JSON.stringify(value);
			return true;
		} catch (err) {
			return false;
		}
	}

	return false;
}
