'use client';

import React from 'react';

import styles from './styles/v2xAddress.module.scss';

const V2xAddress: React.FC = () => {
    return (
        <div className={styles.root}>
            <div className={styles.title}>
                <span>V2X Virtual Address: </span>
            </div>
            <div className={styles.address}>
                 {window.location.hostname}
            </div>
        </div>
    )
}

export default React.memo(V2xAddress);