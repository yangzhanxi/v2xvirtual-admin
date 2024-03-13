'use client';

import React from 'react';

import V2xAddress from '@/components/v2xAddress/V2xAddress'
import LicensesBlock from '@/components/licensesBlock/LicensesBlock';

const LicensesManagement: React.FC = () => {
    return (
        <>
            <V2xAddress/>
            <LicensesBlock/>
        </>
    )
}

export default React.memo(LicensesManagement);