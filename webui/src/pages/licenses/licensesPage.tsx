import React from 'react';

import CommonPage from 'pages/common/commonPage';
import LicensesBlock from 'components/licensesBlock/LicensesBlock';
import V2xInfo from 'components/v2xInfo/V2xInfo';

const LicensesPage: React.FC = () => {
    return (
        <CommonPage>
            <V2xInfo />
            <LicensesBlock />
        </CommonPage>
    );
};

export default React.memo(LicensesPage);
