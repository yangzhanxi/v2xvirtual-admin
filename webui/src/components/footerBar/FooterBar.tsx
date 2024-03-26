import React from 'react';

import {SpirentLogoIcon} from 'assets/icons';

import styles from './styles/footerBar.scss';

const FooterBar: React.FC = () => {
    const renderLogo = (
        <div className={styles.left}>
            {/* <img className={styles.logo} alt="img" src={SpirentLogoIcon} /> */}
            <SpirentLogoIcon className={styles.logo} />
        </div>
    );
    const date = new Date();
    const renderText = (
        <div className={styles.center}>
            <span>© {date.getFullYear()} Spirent Communications, Inc. All rights reserved.</span>
        </div>
    );

    const renderVer = (
        <div className={styles.right}>
            <span>Ver 1.0.0</span>
        </div>
    );

    return (
        <div className={styles.root}>
            {renderLogo}
            {renderText}
            {renderVer}
        </div>
    );
};

export default React.memo(FooterBar);
