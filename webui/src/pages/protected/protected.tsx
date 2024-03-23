import React, {useEffect} from 'react';

import {
    isEnvironmentInitializedSelector,
    isEnvironmentLoadingSelector,
    userTokenSelector,
} from 'domain/environment/environmentSelector';
import {AccountDataRequest} from 'domain/environment/environmentSlice';
import routePaths from 'routePaths';
import {useAppSelector} from 'store/hooks';

import history from '../../store/history';

import styles from './styles/protected.scss';

type ProtectedProps = {
    children?: any;
};

const Protected = ({children}: ProtectedProps) => {
    const token = useAppSelector(userTokenSelector);
    const userAccountDataRequest = AccountDataRequest.useRequest();
    const isEnvironmentInitialized = useAppSelector(isEnvironmentInitializedSelector);
    const isEnvLoading = useAppSelector(isEnvironmentLoadingSelector);

    useEffect(() => {
        userAccountDataRequest();
    }, [userAccountDataRequest]);

    useEffect(() => {
        if (!token) {
            const prevLocation = `${history.location.pathname}${history.location.search}`;
            history.push(
                `${routePaths.AUTHORIZATION}${
                    prevLocation && prevLocation !== '/' ? `?redirectTo=${prevLocation}` : ''
                }`
            );
        }
    }, [token]);

    if (isEnvLoading === true) {
        return (
            <div className={styles.root}>
                <span> LOADING</span>
            </div>
        );
    }
    if (isEnvironmentInitialized) {
        return children;
    }
    return null;
};

export default Protected;
