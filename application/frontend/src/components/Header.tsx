import React from 'react';
import {
    Link,
    AppBar,
    Box,
    Toolbar,
    IconButton,
    Typography,
    Menu,
    Container,
    Avatar,
    Tooltip,
    MenuItem,
    styled,
} from '@mui/material';
import { Menu as MenuIcon } from '@styled-icons/material/Menu';
import { Link as RouterLink } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { LocalizationButton } from './LocalizationButton';

const pages = [
    { name: 'header.pages.home.name', link: 'header.pages.home.link' },
    { name: 'header.pages.restaurants.name', link: 'header.pages.restaurants.link' },
    { name: 'header.pages.events.name', link: 'header.pages.events.link' },
    { name: 'header.pages.users.name', link: 'header.pages.users.link' },
    { name: 'header.pages.images.name', link: 'header.pages.images.link' },
];
const settings = [{ name: 'header.settings.logout.name', link: 'header.settings.logout.link' }];

const StyledMenuItem = styled(MenuItem)({
    position: 'relative',
    padding: 0,
});

const StyledLink = styled(RouterLink)({
    width: '100%',
    height: '100%',
    top: 0,
    left: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'normal',
    color: 'black',
    padding: '6px 16px',
});

const Header: React.FC = () => {
    const { t } = useTranslation();

    const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(null);
    const [anchorElUser, setAnchorElUser] = React.useState<null | HTMLElement>(null);

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElNav(event.currentTarget);
    };
    const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElUser(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    const handleCloseUserMenu = () => {
        setAnchorElUser(null);
    };

    return (
        <AppBar position="static">
            <Container maxWidth="xl">
                <Toolbar disableGutters>
                    <Link
                        to="/"
                        component={RouterLink}
                        variant="h6"
                        noWrap
                        sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
                        underline="none"
                        color="white"
                    >
                        <Typography
                            variant="h5"
                            component="h1"
                            align="center"
                            sx={(theme) => ({
                                color: theme.palette.secondary.main,
                                fontFamily: '"Respira"',
                                fontStyle: 'normal',
                                fontWeight: 400,
                            })}
                        >
                            {t('header.logo')}
                        </Typography>
                    </Link>

                    <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
                        <IconButton
                            size="large"
                            aria-label="account of current user"
                            aria-controls="menu-appbar"
                            aria-haspopup="true"
                            onClick={handleOpenNavMenu}
                            color="inherit"
                        >
                            <MenuIcon size="1em" />
                        </IconButton>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorElNav}
                            anchorOrigin={{
                                vertical: 'bottom',
                                horizontal: 'left',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'left',
                            }}
                            open={Boolean(anchorElNav)}
                            onClose={handleCloseNavMenu}
                            sx={{
                                display: { xs: 'block', md: 'none' },
                            }}
                        >
                            {pages.map((page) => (
                                <StyledMenuItem key={page.name} onClick={handleCloseNavMenu}>
                                    <Link
                                        component={StyledLink}
                                        to={t(page.link)}
                                        sx={{ color: 'black', display: 'block' }}
                                    >
                                        <Typography textAlign="center">{t(page.name)}</Typography>
                                    </Link>
                                </StyledMenuItem>
                            ))}
                        </Menu>
                    </Box>
                    <Link
                        to="/"
                        component={RouterLink}
                        variant="h6"
                        noWrap
                        sx={(theme) => ({
                            flexGrow: 1,
                            display: { xs: 'flex', md: 'none' },
                            color: theme.palette.secondary.main,
                            fontSize: 13,
                            fontFamily: '"Respira"',
                            fontStyle: 'normal',
                            fontWeight: 400,
                        })}
                        underline="none"
                        color="white"
                    >
                        {t('header.logo')}
                    </Link>
                    <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
                        {pages.map((page) => (
                            <Link
                                key={page.name}
                                component={RouterLink}
                                to={t(page.link)}
                                onClick={handleCloseNavMenu}
                                sx={(theme) => ({
                                    display: 'block',
                                    margin: 2,
                                    color: theme.palette.secondary.main,
                                    fontFamily: '"Respira"',
                                    fontStyle: 'normal',
                                    fontWeight: 400,
                                })}
                            >
                                {t(page.name)}
                            </Link>
                        ))}
                    </Box>

                    <Box sx={{ flexGrow: 0, display: 'flex' }}>
                        <LocalizationButton />
                        <Tooltip title="Open settings">
                            <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                                <Avatar alt="profile picture" />
                            </IconButton>
                        </Tooltip>
                        <Menu
                            sx={{ mt: '45px' }}
                            id="menu-appbar"
                            anchorEl={anchorElUser}
                            anchorOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                            open={Boolean(anchorElUser)}
                            onClose={handleCloseUserMenu}
                        >
                            {settings.map((setting) => (
                                <StyledMenuItem key={setting.name} onClick={handleCloseUserMenu}>
                                    <Link component={StyledLink} to={t(setting.link)}>
                                        <Typography textAlign="center">{t(setting.name)}</Typography>
                                    </Link>
                                </StyledMenuItem>
                            ))}
                        </Menu>
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
};
export default Header;
