import i18n from 'i18next';

export const dateToString = (timestamp: string) => {
    const date = new Date(timestamp);
    const readableDate = date.toLocaleString(i18n.language, {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    });

    return readableDate;
};
