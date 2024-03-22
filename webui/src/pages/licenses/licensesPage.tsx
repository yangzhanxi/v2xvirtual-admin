import React from 'react';

import V2xAddress from 'components/v2xAddress/V2xAddress';
import LicensesBlock from 'components/licensesBlock/LicensesBlock';
import CommonPage from 'pages/common/commonPage';

const LicensesPage: React.FC = () => {
    return (
        <CommonPage>
            <V2xAddress />
            <LicensesBlock />
        </CommonPage>
    );
};

export default React.memo(LicensesPage);
