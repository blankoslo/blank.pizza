import React from 'react';
import { useTranslation } from 'react-i18next';
import { Additional, Group, Option, SelectPaginate } from './SelectPaginate';
import { OptionsOrGroups } from 'react-select';
import { useInfiniteGroups } from '../hooks/useGroups';

interface Props {
    disabled?: boolean;
}

const SelectGroup: React.FC<Props> = ({ disabled = false }) => {
    const { t } = useTranslation();

    const { isLoading, data: _groups, hasNextPage, fetchNextPage } = useInfiniteGroups({ page_size: 10 });

    const loadOptions = async (
        inputValue: string,
        options: OptionsOrGroups<Option, Group>,
        additional?: Additional,
    ) => {
        await fetchNextPage();

        const page = additional?.page !== undefined ? additional?.page : (_groups?.pages ?? []).length;
        const groups = _groups?.pages[page - 1].data ?? [];

        let hasMore = isLoading ? true : hasNextPage ?? false;
        if (hasNextPage != undefined && !hasNextPage) {
            hasMore = page < (_groups ? _groups.pages.length : 0);
        }

        const restaurantOptions = groups.map((groups) => ({
            value: groups.id,
            label: groups.name,
        }));

        return {
            options: restaurantOptions,
            hasMore: hasMore,
            additional: {
                page: page + 1,
            },
        };
    };

    return (
        <SelectPaginate
            id="groupSelect"
            name="group"
            label={t('groups.groupSelect.placeholder')}
            fullWidth={true}
            marginLeft={false}
            loadOptions={loadOptions}
            disabled={disabled}
        />
    );
};

export { SelectGroup };
