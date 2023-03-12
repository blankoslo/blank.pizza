import { createTheme, ThemeOptions } from '@mui/material';
import Respira from './assets/fonts/Respira-Black.otf';

const components: ThemeOptions['components'] = {
    MuiFormControl: {
        styleOverrides: {
            root: {
                height: '56px',
            },
        },
    },
    MuiInputBase: {
        styleOverrides: {
            root: {
                height: '56px',
                fieldset: {
                    borderColor: 'rgba(0,0,0,0.23)',
                },
            },
        },
    },
    MuiCssBaseline: {
        styleOverrides: `
      @font-face {
        font-family: 'Respira';
        font-style: normal;
        font-display: swap;
        font-weight: 400;
        src: local('Respira'), local('Respira-Regular'), url(${Respira}) format('opentype');
        unicodeRange: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF;
      }
    `,
    },
};

declare module '@mui/material/styles/createMixins' {
    // Allow for custom mixins to be added
    interface Mixins {
        footer: CSSProperties;
    }
}

const theme = createTheme({
    components: components,
    mixins: {
        footer: {
            '@media (min-width:0px)': {
                '@media (orientation: landscape)': {
                    minHeight: 96,
                },
            },
            '@media (min-width:600px)': {
                minHeight: 128,
            },
            minHeight: 112,
        },
    },
    typography: {
        fontFamily: [
            'Roboto',
            'Respira',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
            '"Apple Color Emoji"',
            '"Segoe UI Emoji"',
            '"Segoe UI Symbol"',
        ].join(','),
    },
    palette: {
        background: {
            default: '#272d2a',
        },
        primary: {
            main: '#272d2a',
        },
        secondary: {
            main: '#fffcb6',
        },
    },
});

export default theme;
