import React from 'react';

import FooterBar from 'components/footerBar/FooterBar';

import styles from './styles/page.scss';

const FOOTER_HEIGHT_PX = 50;

const footerStyle = {height: FOOTER_HEIGHT_PX};

const Page: React.FC<{
    headerBar: React.ReactNode;
    children: React.ReactNode;
}> = ({children, headerBar}) => {
    return (
        <div className={styles.root}>
            {headerBar}
            <div className={styles.workspace}>
                <div className={styles.workingArea}>
                    <div className={styles.content}>{children}</div>
                </div>
                <div className={styles.footer} style={footerStyle}>
                    <FooterBar />
                </div>
            </div>
        </div>
    );
};

export default React.memo(Page);
