import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import { useTranslation } from 'react-i18next';

interface Props {
    parentId: string;
    fetchData: () => void;
    hasMore: boolean;
    items: React.ReactNode[];
    showEndMessage?: boolean;
}

export const InfinityList: React.FC<Props> = ({ parentId, fetchData, hasMore, items, showEndMessage = true }) => {
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
                showEndMessage ? (
                    <p style={{ textAlign: 'center' }}>
                        <b>{t('infinityLoadingList.end')}</b>
                    </p>
                ) : null
            }
        >
            {items}
        </InfiniteScroll>
    );
};
