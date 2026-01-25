import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import unocss from "unocss/vite";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
	const isProduction = mode === "production";

	return {
		plugins: [
			react({
				jsxImportSource: isProduction
					? "react"
					: "@welldone-software/why-did-you-render",
				babel: {
					plugins: isProduction ? [] : [["babel-plugin-react-compiler"]],
				},
			}),
			unocss(),
		],

		resolve: {
			alias: {
				"@": path.resolve(__dirname, "./src"),
			},
		},

		build: {
			target: "esnext",
			minify: "esbuild",
			sourcemap: !isProduction,
			rollupOptions: {
				output: {
					manualChunks: {
						vendor: ["react", "react-dom"],
					},
				},
			},
		},

		server: {
			fs: {
				allow: [".."],
			},
		},
	};
});
