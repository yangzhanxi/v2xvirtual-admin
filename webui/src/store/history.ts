import {createBrowserHistory} from 'history';

import {getBasePath} from 'utils/browser';

const history = createBrowserHistory({
    basename: getBasePath(true),
});

export default history;
