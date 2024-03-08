import type { ReactNode } from 'react';

import FooterBar from '@/components/footerBar/FooterBar';
import Navigator from '@/components/headerBar/Navigator';

import '@/styles/globals.css';

import { StoreProvider } from './StoreProvider';
import styles from '@/styles/layout.module.scss';


interface Props {
  readonly children: ReactNode;
}

export default function RootLayout({ children }: Props) {
    return (
        <StoreProvider>
            <html lang='en'>
                <body>
                    <section>
                        <div className={styles.header}>
                            <Navigator/>
                        </div>
                        <main className={styles.main}>{children}</main>
                        <footer className={styles.footer}>
                            <FooterBar/>
                        </footer>
                    </section>
                </body>
            </html>
        </StoreProvider>
  );
}
