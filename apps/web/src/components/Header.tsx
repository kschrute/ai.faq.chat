function Header() {
	return (
		<h1 className="m-10 text-5xl font-bold text-center bg-gradient-to-r from-cyan-400 to-blue-400 text-transparent bg-clip-text">
			FAQ Chat
		</h1>
	);
}

Header.displayName = "Header";
Header.whyDidYouRender = {
	collapseGroups: true,
	logOnDifferentValues: true,
	onlyLogs: true,
	trackAllPureComponents: true,
	trackHooks: true,
};

export default Header;
