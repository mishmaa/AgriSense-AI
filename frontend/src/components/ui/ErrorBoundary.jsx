import { Component } from 'react';

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error('AgriSense UI error', error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="grid min-h-screen place-items-center bg-[#f6fbf7] p-4 text-graphite-900 dark:bg-graphite-950 dark:text-white">
          <div className="glass max-w-md rounded-lg p-6 text-center">
            <h1 className="text-2xl font-semibold">AgriSense AI needs a refresh</h1>
            <p className="mt-3 text-sm leading-6 text-slate-600 dark:text-slate-300">
              The interface hit an unexpected state. Refresh the page to continue the demo.
            </p>
            <button onClick={() => window.location.reload()} className="mt-5 h-11 rounded-lg bg-agri-500 px-5 text-sm font-semibold text-white shadow-glow">
              Refresh
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
