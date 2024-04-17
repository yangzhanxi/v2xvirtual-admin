import React from 'react';

import styles from './styles/portAttribute.scss';

const PortAttribute: React.FC<{
    label: string;
    value: string;
}> = props => {
    const {label, value} = props;

    return (
        <div className={styles.root}>
            <div className={styles.label}>
                <span> {label}: </span>
            </div>
            <div className={styles.value}>
                <span> {value} </span>
            </div>
        </div>
    );
};

export default React.memo(PortAttribute);
