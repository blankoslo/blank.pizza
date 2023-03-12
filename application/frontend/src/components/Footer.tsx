import React from 'react';
import { Box, Typography } from '@mui/material';
import { useTranslation } from 'react-i18next';
import Logo from '../assets/BlankLogoLight5.svg';

const Footer: React.FC = () => {
    const { t } = useTranslation();

    return (
        <Box
            sx={(theme) => ({
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'flex-end',
                padding: 2,
                backgroundColor: theme.palette.primary.main,
                ...theme.mixins.footer,
                [theme.breakpoints.down('md')]: {
                    display: 'none',
                },
                /*[`${theme.breakpoints.up("xs")} and (orientation: landscape)`]: {
            // eslint-disable-next-line
            // @ts-expect-error
            maxHeight: `Calc(100vh - ${theme.mixins.toolbar['@media (min-width:0px) and (orientation: landscape)'].minHeight}px)` 
          },*/
            })}
        >
            <Typography
                variant="h4"
                component="span"
                align="center"
                sx={(theme) => ({
                    color: theme.palette.secondary.main,
                    fontFamily: '"Respira"',
                    fontStyle: 'normal',
                    fontWeight: 400,
                })}
            >
                {t('footer.logo')}
            </Typography>
            <Logo />
        </Box>
    );
};
export default Footer;
