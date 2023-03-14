import React from 'react';
import { useTranslation } from 'react-i18next';
import { Additional, Group, Option, SelectPaginate } from './SelectPaginate';
import { OptionsOrGroups } from 'react-select';
import { useInfiniteUsers } from '../hooks/useUsers';

interface Props {
    name?: string;
}

const SelectUsers: React.FC<Props> = ({ name }) => {
    const { t } = useTranslation();

    const { isLoading, data: _users, hasNextPage, fetchNextPage } = useInfiniteUsers({ page_size: 10 });

    const loadOptions = async (
        inputValue: string,
        options: OptionsOrGroups<Option, Group>,
        additional?: Additional,
    ) => {
        await fetchNextPage();

        const page = additional?.page !== undefined ? additional?.page : (_users?.pages ?? []).length;
        const users = _users?.pages[page - 1].data ?? [];

        let hasMore = isLoading ? true : hasNextPage ?? false;
        if (hasNextPage != undefined && !hasNextPage) {
            hasMore = page < (_users ? _users.pages.length : 0);
        }

        const usersOptions = users.map((user) => ({
            value: user.slack_id,
            label: user.current_username,
        }));

        return {
            options: usersOptions,
            hasMore: hasMore,
            additional: {
                page: page + 1,
            },
        };
    };

    return (
        <SelectPaginate
            name={name ?? 'users'}
            label={t('groups.usersSelect.label')}
            fullWidth={true}
            marginLeft={false}
            loadOptions={loadOptions}
            multi={true}
        />
    );
};

export { SelectUsers };
