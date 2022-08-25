import * as React from 'react';
import styled from 'styled-components';
import { ErrorMessage as HookformErrorMessage } from '@hookform/error-message';
import { useTheme } from '@mui/material/styles';

const StyledError = styled.span<{ errorColor: string; size: string | number }>`
    color: ${(props) => props.errorColor};
    display: flex;
    flex-wrap: wrap;
    font-size: ${(props) => props.size};
    max-width: fit-content;
`;

type Props = {
    children?: React.ReactNode;
};

const ErrorContainer: React.FC<Props> = ({ children }) => {
    const theme = useTheme();

    return (
        <StyledError
            errorColor={theme.palette.warning.main}
            size={theme.typography.caption.fontSize?.toString() ?? theme.typography.fontSize}
        >
            {children}
        </StyledError>
    );
};

export const ErrorMessage: React.FC<React.ComponentPropsWithoutRef<typeof HookformErrorMessage>> = ({
    name,
    ...rest
}) => <HookformErrorMessage name={name} as={ErrorContainer} {...rest} />;
