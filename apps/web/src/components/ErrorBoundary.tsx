import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
	children: ReactNode;
	fallback?: ReactNode;
}

interface State {
	hasError: boolean;
	error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
	constructor(props: Props) {
		super(props);
		this.state = { hasError: false };
	}

	static getDerivedStateFromError(error: Error): State {
		return { hasError: true, error };
	}

	componentDidCatch(error: Error, errorInfo: ErrorInfo) {
		console.error("Error caught by boundary:", error, errorInfo);
	}

	render() {
		if (this.state.hasError) {
			return (
				this.props.fallback || (
					<div className="flex flex-col items-center justify-center p-8 text-center">
						<div className="text-yellow-500 text-6xl mb-5">
							<div className="i-lucide-circle-x" />
						</div>
						<h2 className="text-xl font-semibold mb-2">Something went wrong</h2>
						<p className="text-gray-600 dark:text-gray-400 mb-4">
							An unexpected error occurred. Please refresh the page and try again.
						</p>
						<button
							type="button"
							onClick={() => window.location.reload()}
							className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors cursor-pointer"
						>
							Refresh Page
						</button>
					</div>
				)
			);
		}

		return this.props.children;
	}
}

export default ErrorBoundary;
