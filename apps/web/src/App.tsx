import Chat from "@/components/Chat";
import Header from "@/components/Header";

function App() {
	return (
		<div className="w-full min-h-screen flex flex-col items-center justify-center">
			<div className="hidden sm:block">
				<Header />
			</div>
			<Chat />
		</div>
	);
}

export default App;
