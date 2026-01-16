import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import unocss from "unocss/vite";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
	return {
		plugins: [
			react({
				jsxImportSource:
					mode === "development" ? "@welldone-software/why-did-you-render" : "react",
				babel: {
					plugins: [["babel-plugin-react-compiler"]],
				},
			}),
			unocss(),
		],

		resolve: {
			alias: {
				"@": path.resolve(__dirname, "./src"),
			},
		},
	};
});
