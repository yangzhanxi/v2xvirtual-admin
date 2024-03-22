// import {Link, useRouteMatch} from 'react-router-dom';
import React from 'react';

// import routePaths from 'routePaths';
// import {useTranslation} from 'react-i18next';
// import ContextMenuHeaderButton, {ContextMenuItem} from 'components/headerBar/contextMenuHeaderButton';
// import HeaderBar, {HeaderBarItems, HeaderButton} from 'components/headerBar/headerBar';
// import {ModalsIDs, useModal} from 'components/modals/hooks';
// import Notifications from 'components/notifications/notifications';
// import UserInfo from 'components/userInfo/userInfo';
// import {useScenarioQueryState} from 'utils/useQueryState';

import Navigation from 'components/headerBar/Navigation';
import Page from 'components/page/page';
// import {useAppSelector} from 'store/hooks';
// import routePaths from 'routePaths';

import styles from './styles/commonPage.scss';

const CommonPage: React.FC<{
    children: React.ReactNode;
    hideHeaderBar?: boolean;
}> = ({children, hideHeaderBar}) => {
    // const isAuthPage = !!useRouteMatch({path: routePaths.AUTHORIZATION, exact: true});
    // const {t: tComponents} = useTranslation('components');
    // const {t: tCommon} = useTranslation('common');
    // const {t: tNotifications} = useTranslation('notifications');
    // const {openModal} = useModal();

    // const isDashboardPage = !!useRouteMatch({path: routePaths.INDEX, exact: true});
    // const isLicensesPage = !!useRouteMatch({path: routePaths.LICENSES, exact: true});

    // const dashboardTitle = tCommon('dashboard');

    // const leftItems = (
    //     <HeaderBarItems>
    //         <Link to={routePaths.INDEX}>
    //             <div className={styles.appIconContainer}>
    //                 <LogoIcon className={styles.appIcon} />
    //             </div>
    //         </Link>
    //         <Link to={routePaths.INDEX}>
    //             <HeaderButton text={'License Management'} data-cy="dashboard" isActive={isDashboardPage} />
    //         </Link>
    //         <Link to={routePaths.LICENSES}>
    //             <HeaderButton text={'Network Management'} isActive={isLicensesPage} />
    //         </Link>
    //     </HeaderBarItems>
    // );

    // const rightItems = <HeaderBarItems>{/* <UserInfo /> */}</HeaderBarItems>;
    // const headerBar = hideHeaderBar ? null : (
    //     <div className={styles.headerBar}>
    //         {simulation && (
    //             <div className={styles.simulationActiveBanner}>
    //                 <span>{tNotifications('simulation.simulationActive')}</span>
    //             </div>
    //         )}
    //         <HeaderBar leftItems={leftItems} rightItems={} />
    //     </div>
    // );

    const headerBar = hideHeaderBar ? null : (
        <div className={styles.headerBar}>
            <Navigation />
        </div>
    );

    return <Page headerBar={headerBar}>{children}</Page>;
};

export default React.memo(CommonPage);
