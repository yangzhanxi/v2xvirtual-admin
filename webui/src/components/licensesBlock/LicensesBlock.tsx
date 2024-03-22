import React from 'react';

import LicenseTable from 'components/licenseTable/LicenseTable';

import styles from './styles/licensesBlock.scss';

const LicensesBlock: React.FC = () => {
    return (
        <div className={styles.root}>
            <div className={styles.header}>
                <div className={styles.text}>
                    <span> Licenses </span>
                </div>
            </div>
            <div className={styles.table}>
                <LicenseTable />
            </div>
        </div>
    );
};

export default React.memo(LicensesBlock);
