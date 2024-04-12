import React, {useEffect, useState} from 'react';
import classNames from 'classnames';
import {useTranslation} from 'react-i18next';

import styles from './styles/v2xInfo.scss';

interface V2xInfoProps {
    partNum?: string;
}

const V2xInfo: React.FC<V2xInfoProps> = ({partNum}) => {
    const {t} = useTranslation('components');
    const [hostAddr, setHostAddr] = useState('');
    useEffect(() => {
        const address = window.location.hostname;
        setHostAddr(address);
    }, []);

    const partNumTitleClassName = classNames(styles.title, {
        [styles.mTitle]: true,
    });
    const renderPartNum = partNum ? (
        <>
            <div className={partNumTitleClassName}>
                <span> {t('partNum')}: </span>
            </div>
            <div className={styles.content}>{partNum}</div>
        </>
    ) : null;

    return (
        <div className={styles.root}>
            <div className={styles.title}>
                <span>{t('v2xAddress')}: </span>
            </div>
            <div className={styles.content}>{hostAddr}</div>
            {renderPartNum}
        </div>
    );
};

export default React.memo(V2xInfo);
