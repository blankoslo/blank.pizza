import i18n from 'i18next';

export const datetimeToString = (timestamp: string) => {
    const date = new Date(timestamp);
    const readableDate = date.toLocaleString(i18n.language, {
        minute: '2-digit',
        hour: '2-digit',
        day: 'numeric',
        month: 'long',
        year: 'numeric',
    });

    return readableDate;
};
