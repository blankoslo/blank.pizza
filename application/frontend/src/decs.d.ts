declare module '*.png';

declare module '*.otf';

declare module '*.svg' {
    const content: any;
    export default content;
}

declare module 'react-https-redirect';
