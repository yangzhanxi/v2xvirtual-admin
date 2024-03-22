import React from 'react';
import {Link, useRouteMatch} from 'react-router-dom';
// import {usePathname} from 'next/navigation';

import routePaths from 'routePaths';
import {HeaderLogo} from 'assets/icons';

// import UserInfo from '@/components/userInfo/UserInfo';
import HeaderBar, {HeaderBarItems, HeaderButton} from './HeaderBar';
import styles from './styles/navigation.scss';

const Navigator: React.FC = () => {
    // const isDashboardPage = !!useRouteMatch({path: routePaths.INDEX, exact: true});
    const isLicensesPage = !!useRouteMatch({path: routePaths.LICENSES, exact: true});

    const leftItems = (
        <HeaderBarItems>
            <Link to={routePaths.INDEX}>
                <img className={styles.appIconContainer} alt="V2X Virtual Admin" src={HeaderLogo} />
            </Link>
            <Link to={routePaths.LICENSES}>
                <HeaderButton text={'License Management'} data-cy="dashboard" isActive={isLicensesPage} />
            </Link>
        </HeaderBarItems>
    );

    const rightTtems = <HeaderBarItems>{/* <UserInfo/> */}</HeaderBarItems>;

    return (
        <div>
            <HeaderBar leftItems={leftItems} rightItems={rightTtems} />
        </div>
    );
};

export default React.memo(Navigator);
