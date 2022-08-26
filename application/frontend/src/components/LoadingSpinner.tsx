import React from 'react';
import styled from 'styled-components';
import { keyframes } from 'styled-components';

const spin = keyframes`
    to {
        transform: translate(-50%, -50%) rotate(360deg);
    }
`;

const Loader = styled.div`
    border: 0.25rem solid hsla(0, 0%, 0%, 0.5);
    border-right-color: #000;
    display: inline-block;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    animation: ${spin} 1s linear infinite;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
`;

export const LoadingSpinner: React.FC = () => {
    return <Loader />;
};
