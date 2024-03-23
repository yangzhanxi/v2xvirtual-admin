import {ConnectedRouter} from 'connected-react-router';
import {Provider} from 'react-redux';
import React from 'react';
import ReactModal from 'react-modal';
import {createRoot} from 'react-dom/client';
import {enableMapSet} from 'immer';

import './dependencies';

import history from 'store/history';

import store, {runSaga} from './store/store';
import {Routes} from './routes';

runSaga();

const App: React.FC = () => {
    // useEffect(() => {
    //     init(store.dispatch);
    // });
    return (
        <Provider store={store}>
            <ConnectedRouter history={history}>
                <Routes />
            </ConnectedRouter>
        </Provider>
    );
};

enableMapSet();

const appElement = document.getElementById('v2x-virtual-admin');

if (appElement) {
    ReactModal.setAppElement(appElement);
    const root = createRoot(appElement);
    root.render(<App />);
}
