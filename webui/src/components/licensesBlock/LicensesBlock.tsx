import React from 'react';
import {useTranslation} from 'react-i18next';

import LicenseTable from 'components/licenseTable/LicenseTable';

import styles from './styles/licensesBlock.scss';

const LicensesBlock: React.FC = () => {
    const {t} = useTranslation('components');

    return (
        <div className={styles.root}>
            <div className={styles.header}>
                <div className={styles.text}>
                    <span> {t('licensesBlock.licenses')} </span>
                </div>
            </div>
            <div className={styles.table}>
                <LicenseTable />
            </div>
        </div>
    );
};

export default React.memo(LicensesBlock);
