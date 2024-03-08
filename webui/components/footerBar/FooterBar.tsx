import React from 'react';
import Image from 'next/image';

import spirentLogo from '@/public/icons/spirent-logo.svg';

import styles from './styles/footerBar.module.scss';

const FooterBar: React.FC = () => {
    const renderLogo =
        <div className={styles.left}>
            <Image className={styles.logo} alt='img' src={spirentLogo}/>
        </div>
    const date = new Date
    const renderText =
        <div className={styles.center}>
            <span>
                © {date.getFullYear()} Spirent Communications, Inc. All rights reserved.
            </span>
        </div>

    const renderVer =
        <div className={styles.right}>
            <span>
                Ver 1.0.0
            </span>
        </div>

    return (
        <div className={styles.root}>
            {renderLogo}
            {renderText}
            {renderVer}
        </div>
    )
}

export default React.memo(FooterBar);