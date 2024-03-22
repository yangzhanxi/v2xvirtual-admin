import React, {useEffect, useState} from 'react';

import styles from './styles/v2xAddress.scss';

const V2xAddress: React.FC = () => {
    const [hostAddr, setHostAddr] = useState('');
    useEffect(() => {
        const address = window.location.hostname;
        setHostAddr(address);
    }, []);

    return (
        <div className={styles.root}>
            <div className={styles.title}>
                <span>V2X Virtual Address: </span>
            </div>
            <div className={styles.address}>{hostAddr}</div>
        </div>
    );
};

export default React.memo(V2xAddress);
