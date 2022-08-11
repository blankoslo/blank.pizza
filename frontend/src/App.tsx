import React, { useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './App.css';

import PizzaEvents from 'components/PizzaEvents';

const queryClient = new QueryClient()

function App() {
  return (
  <QueryClientProvider client={queryClient}>
    <div className="App">
      <h1>Pizza Events</h1>
      <PizzaEvents />
    </div>
  </QueryClientProvider>
  );
}

export default App;
