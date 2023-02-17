import React from 'react';
import { useTranslation } from 'react-i18next';
import { Additional, Group, Option, SelectPaginate } from './SelectPaginate';
import { OptionsOrGroups } from 'react-select';
import { useInfiniteRestaurants } from '../hooks/useRestaurants';

const SelectRestaurant: React.FC = () => {
    const { t } = useTranslation();

    const { isLoading, data: _restaurants, hasNextPage, fetchNextPage } = useInfiniteRestaurants({ page_size: 10 });

    const loadOptions = async (
        inputValue: string,
        options: OptionsOrGroups<Option, Group>,
        additional?: Additional,
    ) => {
        await fetchNextPage();

        const page = additional?.page !== undefined ? additional?.page : (_restaurants?.pages ?? []).length;
        const restaurants = _restaurants?.pages[page - 1].data ?? [];

        let hasMore = isLoading ? true : hasNextPage ?? false;
        if (hasNextPage != undefined && !hasNextPage) {
            hasMore = page < (_restaurants ? _restaurants.pages.length : 0);
        }

        const restaurantOptions = restaurants.map((restaurant) => ({
            value: restaurant.id,
            label: restaurant.name,
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
            name="restaurant"
            label={t('restaurants.select.label')}
            fullWidth={true}
            marginLeft={false}
            loadOptions={loadOptions}
        />
    );
};

export { SelectRestaurant };
