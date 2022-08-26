import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import { useTranslation } from 'react-i18next';

interface Props {
    parentId: string;
    fetchData: () => void;
    hasMore: boolean;
    items: React.ReactNode[];
}

export const InfinityList: React.FC<Props> = ({ parentId, fetchData, hasMore, items }) => {
    const { t } = useTranslation();

    return (
        <InfiniteScroll
            scrollableTarget={parentId}
            dataLength={items.length}
            next={fetchData}
            hasMore={hasMore}
            loader={
                <p style={{ textAlign: 'center' }}>
                    <b>{t('infinityLoadingList.loading')}</b>
                </p>
            }
            endMessage={
                <p style={{ textAlign: 'center' }}>
                    <b>{t('infinityLoadingList.end')}</b>
                </p>
            }
        >
            {items}
        </InfiniteScroll>
    );
};
