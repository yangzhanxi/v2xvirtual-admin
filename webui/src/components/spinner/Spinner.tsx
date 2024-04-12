import React from 'react';
import {SpinnerOverlay} from 'orion-rwc';

import styles from './styles/spinner.scss';

const Spinner: React.FC = () => {
    return (
        <div className={styles.root}>
            <SpinnerOverlay text={'Loading...'} />
        </div>
    );
};

export default React.memo(Spinner);
