import React, {useEffect, useMemo, useState} from 'react';
import {SpinnerOverlay, Table, TableColumn, TableRow} from 'orion-rwc';

// import {useGetLicensesQuery} from 'lib/features/licenseManagement/licensesApiSlice';
// import {License, LicenseApiResponse} from '@/lib/features/licenseManagement/licenseModels';
import {getLicensesRequested} from 'domain/licenseManagement/licenseManagementSlice';
import {isLicensesLoadingSelector, isLicensesSelector} from 'domain/licenseManagement/licenseManagementSelector';
import {useAppDispatch, useAppSelector} from 'store/hooks';
import {useAsync} from 'utils/hooks';
import {LicnesesControllerService} from 'api/services/LicensesService';

import {LicenseRowItem, createLicenseRowItem, tableSortOption} from './models';
import {sortByExpiration, sortByName, sortByOrdinalNumber, sortByStartTime, sortLicenses} from './utils';
import styles from './styles/licenseTable.scss';

const LicenseTable: React.FC = () => {
    const [localSortOrder, setLocalSortOrder] = useState(Table.SortOrder.ASC);
    const [localSortOption, setLocalSortOprtion] = useState(tableSortOption.ORDINAL_NUMBER);
    const [localRowItems, setLocalRowItems] = useState<LicenseRowItem[]>([]);

    const {exec: getLic, isPending} = useAsync(async () => {
        try {
            const data = await LicnesesControllerService.getLicenses();
            setLocalRowItems(data.sort(sortLicenses).map((lic, index) => createLicenseRowItem(index, lic)));
        } catch (err) {
            console.log(err);
        }
    });
    useEffect(() => {
        getLic();
    }, [getLic]);

    const getCompareFunc = (a: LicenseRowItem, b: LicenseRowItem) => {
        if (localSortOption === tableSortOption.SORT_BY_NAME) {
            return sortByName(a, b, localSortOrder);
        }
        if (localSortOption === tableSortOption.SORT_BY_START) {
            return sortByStartTime(a, b, localSortOrder);
        }
        if (localSortOption === tableSortOption.SORT_BY_EXPIRATION) {
            return sortByExpiration(a, b, localSortOrder);
        }

        return sortByOrdinalNumber(a, b, localSortOrder);
    };

    const handleSortOptionChange = (newSortOption: any) => {
        let sortOption = newSortOption;
        let sortOrder =
            localSortOrder === Table.SortOrder.DESC || sortOption !== localSortOption
                ? Table.SortOrder.ASC
                : Table.SortOrder.DESC;

        if (
            sortOption === localSortOption &&
            localSortOption !== tableSortOption.ORDINAL_NUMBER &&
            localSortOrder === Table.SortOrder.DESC
        ) {
            sortOption = tableSortOption.ORDINAL_NUMBER;
            sortOrder = Table.SortOrder.ASC;
        }

        setLocalSortOprtion(sortOption);
        setLocalSortOrder(sortOrder);
    };

    const tableOptions: Table.ITableOptions = {
        sort: {
            enabled: true,
            sortOption: localSortOption,
            sortOrder: localSortOrder,
            sortableByOrdinalNumber: true,
            onSortOptionChange: handleSortOptionChange,
        },
        resize: {
            enabled: true,
            columnMinWidth: 60,
            indicatorVisible: true,
        },
    };

    const columns: TableColumn[] = [
        {
            align: 'center',
            content: 'Name',
            sortOption: 'sortByName',
        },
        {
            align: 'center',
            content: 'Start',
            sortOption: 'sortByStart',
        },
        {
            align: 'center',
            content: 'Expiration',
            sortOption: 'sortByExpiration',
        },
    ];

    const createRow = (rowItem: LicenseRowItem): TableRow => {
        return {
            id: rowItem.id,
            ordinalNumber: rowItem.index,
            cells: [
                {
                    content: rowItem.name,
                },
                {
                    content: rowItem.start,
                },
                {
                    content: rowItem.expiration,
                },
            ],
        };
    };

    const createRows = () => {
        const rows = localRowItems;
        return rows.sort(getCompareFunc).map(row => createRow(row));
    };

    const renderTable = () => {
        return <Table.Table rows={createRows()} columns={columns} options={tableOptions} />;
    };

    const renderSpinner = () => {
        return (
            <div className={styles.loadingContainer}>
                <SpinnerOverlay text={'Loading...'} />
            </div>
        );
    };

    const renderNoLicense = () => {
        return (
            <div className={styles.noLicenseContainer}>
                <div></div>
                <div className={styles.noLicenseContext}>
                    <span> No licenses found.</span>
                </div>
            </div>
        );
    };

    const renderContent = () => {
        if (isPending) {
            return renderSpinner();
        }
        if (!isPending && localRowItems.length === 0) {
            return renderNoLicense();
        }

        return renderTable();
    };

    return renderContent();
};

export default React.memo(LicenseTable);
