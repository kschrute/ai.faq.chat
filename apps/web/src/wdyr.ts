/// <reference types="vite/client" />
import React from "react";

if (import.meta.env.DEV) {
	const { default: whyDidYouRender } = await import(
		"@welldone-software/why-did-you-render"
	);
	whyDidYouRender(React, {
		trackAllPureComponents: true,
		trackHooks: true,
		// collapseGroups: true,
		// logOnDifferentValues: true,
		// onlyLogs: true,
		// trackExtraHooks: [[useMyHook, 1]],
	});
}
