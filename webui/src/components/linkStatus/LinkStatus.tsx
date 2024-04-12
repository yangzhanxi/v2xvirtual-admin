import React from 'react';

import LinkStatusIcon from 'components/linkStatusIcon/LinkStatusIcon';

import styles from './styles/linkStatus.scss';

const LinkStatus: React.FC<{
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
                <LinkStatusIcon linkStatus={value} />
            </div>
        </div>
    );
};

export default React.memo(LinkStatus);
