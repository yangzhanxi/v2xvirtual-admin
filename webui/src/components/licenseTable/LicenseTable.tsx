import React, {useEffect, useState} from 'react';
import {SpinnerOverlay, Table, TableColumn, TableRow} from 'orion-rwc';
import {useTranslation} from 'react-i18next';

import {LicnesesControllerService} from 'api/services/LicensesService';
import {useAsync} from 'utils/hooks';

import {LicenseRowItem, createLicenseRowItem, tableSortOption} from './models';
import {sortByExpiration, sortByName, sortByOrdinalNumber, sortByStartTime, sortLicenses} from './utils';
import styles from './styles/licenseTable.scss';

const LicenseTable: React.FC = () => {
    const [localSortOrder, setLocalSortOrder] = useState(Table.SortOrder.ASC);
    const [localSortOption, setLocalSortOprtion] = useState(tableSortOption.ORDINAL_NUMBER);
    const [localRowItems, setLocalRowItems] = useState<LicenseRowItem[]>([]);

    const {
        exec: getLic,
        isPending,
        error,
    } = useAsync(async () => {
        try {
            const data = await LicnesesControllerService.getLicenses();
            setLocalRowItems(data.sort(sortLicenses).map((lic, index) => createLicenseRowItem(index, lic)));
        } catch (err) {
            if (err instanceof Error) {
                console.log(err?.message);
            }
        }
    });
    useEffect(() => {
        getLic();
    }, [getLic]);

    const {t} = useTranslation('components');

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
            content: t('licenseTable.colmunNames.name'),
            sortOption: 'sortByName',
        },
        {
            align: 'center',
            content: t('licenseTable.colmunNames.start'),
            sortOption: 'sortByStart',
        },
        {
            align: 'center',
            content: t('licenseTable.colmunNames.expiration'),
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
        if ((!isPending && localRowItems.length === 0) || error) {
            return renderNoLicense();
        }

        return renderTable();
    };

    return renderContent();
};

export default React.memo(LicenseTable);
