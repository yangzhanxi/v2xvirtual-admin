import React, {useEffect} from 'react';
import {ConnectedRouter} from 'connected-react-router';
import {Provider} from 'react-redux';
import ReactModal from 'react-modal';
import {createRoot} from 'react-dom/client';
import {enableMapSet} from 'immer';

import 'api/preconfiguration';
import './dependencies';

import history from 'store/history';
import {init} from 'i18n/config';

import store, {runSaga} from './store/store';
import {Routes} from './routes';

runSaga();

const App: React.FC = () => {
    const [isTranslationInitialized, setIsTranslationInitialized] = React.useState(false);
    useEffect(() => {
        init(store.dispatch);
        setIsTranslationInitialized(true);
    }, []);

    if (!isTranslationInitialized) {
        return null;
    }

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
