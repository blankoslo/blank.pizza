import { createTheme } from '@mui/material/styles';
import { orange } from '@mui/material/colors'
import { PaletteOptions } from '@mui/material';

const theme = createTheme({
    status: {
      danger: orange[500],
    },
    palette: {
        primary: {
          light: '#272D2A',
          main: '#272D2A',
          dark: '#272D2A',
          contrastText: '#FFFCB6',
        },
        secondary: {
          light: '#FFFCB6',
          main: '#FFFCB6',
          dark: '#FFFCB6',
          contrastText: '#272D2A',
        },
        text: {
            primary: '#FFFCB6',
        },
        background: {
            default: '#272D2A',
        }
    },
  });
  

declare module '@mui/material/styles' {
    interface Theme {
      status: {
        danger: string;
      };
    }
    // allow configuration using `createTheme`
    interface ThemeOptions {
      status?: {
        danger?: string;
      };
      palette?: PaletteOptions;
    }
  }
  

export default theme;