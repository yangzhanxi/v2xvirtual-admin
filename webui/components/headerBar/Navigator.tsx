'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

import UserInfo from '@/components/userInfo/UserInfo';
import logo from '@/public/icons/logo.svg';

import HeaderBar, { HeaderBarItems, HeaderButton } from './HeaderBar';

import styles from './styles/navigator.module.scss';

const Navigator: React.FC = () => {
    const leftItems = (
        <HeaderBarItems>
            <Link href="/">
                <Image className={styles.appIconContainer} alt='V2X Virtual Admin' src={logo} priority={true}/>
            </Link>
            <Link href="/verify">
                <HeaderButton text={'License Management'} data-cy="dashboard" isActive={true}/>
            </Link>
            <Link href="/quotes">
                <HeaderButton text={'Network Management'} isActive={false}/>
            </Link>
        </HeaderBarItems>
    )

    const rightTtems = (
        <HeaderBarItems>
            <UserInfo/>
        </HeaderBarItems>
    )

    return (
        <div>
            <HeaderBar leftItems={leftItems} rightItems={rightTtems}/>
        </div>
    )
}

export default React.memo(Navigator);