import React from 'react';

import CommonPage from 'pages/common/commonPage';
import LicensesBlock from 'components/licensesBlock/LicensesBlock';
import V2xAddress from 'components/v2xAddress/V2xAddress';

const LicensesPage: React.FC = () => {
    return (
        <CommonPage>
            <V2xAddress />
            <LicensesBlock />
        </CommonPage>
    );
};

export default React.memo(LicensesPage);
