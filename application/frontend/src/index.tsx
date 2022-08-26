import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

import './i18n';

// 'as Element' needed to not trigger "Forbidden non-null assertion" from @typescript-eslint
const container = document.getElementById('root') as Element;

const root = createRoot(container);

root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
);
