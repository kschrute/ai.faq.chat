import Chat from "@/components/Chat";
import Header from "@/components/Header";
import ErrorBoundary from "@/components/ErrorBoundary";

function App() {
	return (
		<ErrorBoundary>
			<div className="w-full min-h-screen flex flex-col items-center justify-center">
				<div className="hidden sm:block">
					<Header />
				</div>
				<ErrorBoundary fallback={null}>
					<Chat />
				</ErrorBoundary>
			</div>
		</ErrorBoundary>
	);
}

export default App;
