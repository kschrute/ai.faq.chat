import { defineConfig, presetWind4, presetIcons } from "unocss";
import presetAnimations from "unocss-preset-animations";
import presetAttributify from "@unocss/preset-attributify";
import transformerDirectives from "@unocss/transformer-directives";

export default defineConfig({
	presets: [
		presetWind4({
			// dark: "class",
			dark: "media",
		}),
		presetIcons({
			scale: 1.3,
		}),
		presetAnimations(),
		presetAttributify(),
	],
	rules: [
		// [/^m-(\d+)$/, ([, d]) => ({ margin: `${d / 4}rem` })],
		// You can get rich context information from the second argument, such as `theme`, `symbols`, etc.
		// [/^p-(\d+)$/, (match, ctx) => ({ padding: `${match[1] / 4}rem` })],
		// ["m-1", { margin: "1px" }],
		// ["m-100", { margin: "100px" }],
	],
	transformers: [transformerDirectives()],
	theme: {
		// optional: override DaisyUI themes
		// daisyui: { themes: ['light', 'dark', 'cupcake'] },
	},
});
