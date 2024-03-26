import {Link, useRouteMatch} from 'react-router-dom';
import React from 'react';
import {useTranslation} from 'react-i18next';

import {FilesIcon, HeaderLogo} from 'assets/icons';
import UserInfo from 'components/userInfo/UserInfo';
import routePaths from 'routePaths';

import HeaderBar, {HeaderBarItems, HeaderButton} from './HeaderBar';
import styles from './styles/navigation.scss';

const Navigator: React.FC = () => {
    const {t} = useTranslation('components');
    const isDashboardPage = !!useRouteMatch({path: routePaths.INDEX, exact: true});
    const isLicensesPage = !!useRouteMatch({path: routePaths.LICENSES, exact: true});

    const leftItems = (
        <HeaderBarItems>
            <Link to={routePaths.INDEX}>
                <HeaderLogo className={styles.appIconContainer} />
            </Link>
            <Link to={routePaths.LICENSES}>
                <HeaderButton
                    Icon={FilesIcon}
                    text={t('navigation.licenseManagement')}
                    data-cy="dashboard"
                    isActive={isLicensesPage || isDashboardPage}
                />
            </Link>
        </HeaderBarItems>
    );

    const rightTtems = (
        <HeaderBarItems>
            <UserInfo />
        </HeaderBarItems>
    );

    return (
        <div>
            <HeaderBar leftItems={leftItems} rightItems={rightTtems} />
        </div>
    );
};

export default React.memo(Navigator);
