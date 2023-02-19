import { Box } from '@mui/material';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { Chrono, TimelineItem } from 'react-chrono';
import { useInfiniteImages } from '../../../hooks/useImages';
import { useTheme } from '@mui/material/styles';
import i18n from 'i18next';
import {useTranslation} from "react-i18next";

const ImagesPage: React.FC = () => {
    const { t } = useTranslation();
    const theme = useTheme();

    const {
        isLoading,
        data: _images,
        hasNextPage,
        fetchNextPage,
    } = useInfiniteImages({
        page_size: 10,
        order: 'Desc',
    });

    const [images, setImages] = useState<TimelineItem[]>([]);

    useEffect(() => {
        const imageCards: TimelineItem[] =
            _images?.pages
                .flatMap((page) => page.data)
                .map((image) => ({
                    title: `${new Date(image.uploaded_at).toLocaleString(i18n.language, {
                        minute: '2-digit',
                        hour: '2-digit',
                        weekday: 'long',
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric',
                    })}`,
                    cardTitle: `"${image.title}" ${t('global.by')} @${image.uploaded_by.current_username}`,
                    media: {
                        name: image.title,
                        source: {
                            url: `https://res.cloudinary.com/blank/image/upload/c_scale,q_auto,w_350/v1485972107/${image.cloudinary_id}`,
                        },
                        type: 'IMAGE',
                    },
                })) ?? [];
        setImages(imageCards);
    }, [_images, i18n.language]);

    const loadMore = async () => {
        if (!isLoading && hasNextPage) {
            await fetchNextPage();
        }
    };

    return (
        <Box
            sx={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
        >
            <Chrono
                items={images}
                mode="VERTICAL_ALTERNATING"
                allowDynamicUpdate={true}
                onScrollEnd={loadMore}
                hideControls={true}
                scrollable={true}
                cardWidth={500}
                theme={{
                    primary: theme.palette.common.black,
                    secondary: theme.palette.secondary.main,
                    cardBgColor: theme.palette.secondary.main,
                    cardForeColor: theme.palette.common.black,
                    titleColor: theme.palette.common.white,
                    titleColorActive: theme.palette.primary.main,
                }}
            />
        </Box>
    );
};
export default ImagesPage;
