import React from 'react';

import Navigation from 'components/headerBar/Navigation';
import Page from 'components/page/page';

import styles from './styles/commonPage.scss';

const CommonPage: React.FC<{
    children: React.ReactNode;
    hideHeaderBar?: boolean;
}> = ({children, hideHeaderBar}) => {
    const headerBar = hideHeaderBar ? null : (
        <div className={styles.headerBar}>
            <Navigation />
        </div>
    );

    return <Page headerBar={headerBar}>{children}</Page>;
};

export default React.memo(CommonPage);
