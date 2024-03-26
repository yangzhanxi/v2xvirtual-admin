import React, {useEffect, useState} from 'react';
import {useTranslation} from 'react-i18next';

import styles from './styles/v2xAddress.scss';

const V2xAddress: React.FC = () => {
    const {t} = useTranslation('components');
    const [hostAddr, setHostAddr] = useState('');
    useEffect(() => {
        const address = window.location.hostname;
        setHostAddr(address);
    }, []);

    return (
        <div className={styles.root}>
            <div className={styles.title}>
                <span>{t('v2xAddress')}: </span>
            </div>
            <div className={styles.address}>{hostAddr}</div>
        </div>
    );
};

export default React.memo(V2xAddress);
