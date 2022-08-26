import * as React from 'react';
import { Box, ButtonProps } from '@mui/material';

interface Props extends ButtonProps {
    text: string;
    onClick?: () => void;
}

const Button3D: React.FC<Props> = ({ text, onClick }) => {
    const _onClick = () => {
        if (onClick) {
            // Allow the animation to finish so that it looks like the button goes back up
            setTimeout(onClick, 200);
        }
    };

    return (
        <Box
            onClick={_onClick}
            sx={(theme) => ({
                float: 'right',
                backgroundColor: theme.palette.primary.main,
                borderRadius: '6px',
                boxShadow: `0 0 0 1px ${theme.palette.primary.light} inset,0 0 0 2px rgba(255, 255, 255, 0.15) inset,0 4px 0 0 ${theme.palette.primary.dark},0 4px 0 1px rgba(0, 0, 0, 0.4),0 4px 4px 1px rgba(0, 0, 0, 0.5)`,
                color: 'white !important',
                marginBottom: '4px',
                marginX: '1px',
                fontSize: '20px',
                fontWeight: 'bold',
                letterSpacing: '-1px',
                position: 'relative',
                textAlign: 'center',
                textShadow: '0 1px 1px rgba(0, 0, 0, 0.5)',
                textDecoration: 'none !important',
                transition: 'all .2s linear',
                paddingX: 3,
                paddingY: 1,
                display: 'flex',
                alignItems: 'center',
                userSelect: 'none',
                '&:hover': {
                    backgroundColor: theme.palette.primary.light,
                    poisiton: 'relative',
                    top: '-1px',
                    boxShadow: `0 0 0 1px ${theme.palette.primary.light} inset,0 0 0 2px rgba(255, 255, 255, 0.15) inset,0 5px 0 0 ${theme.palette.primary.dark},0 5px 0 1px rgba(0, 0, 0, 0.4),0 5px 8px 1px rgba(0, 0, 0, 0.5)`,
                },
                '&:active': {
                    backgroundColor: theme.palette.primary.main,
                    top: '4px',
                    boxShadow: `0 0 0 1px ${theme.palette.primary.light} inset,0 0 0 2px rgba(255, 255, 255, 0.15) inset,0 0 0 0 ${theme.palette.primary.dark},0 0 0 1px rgba(0, 0, 0, 0.4),0 0px 8px 1px rgba(0, 0, 0, 0.5)`,
                },
            })}
        >
            {text}
        </Box>
    );
};

export { Button3D };
