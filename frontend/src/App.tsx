import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ThemeProvider, Grid, Typography } from '@mui/material';
import { Container } from '@mui/system';
import { CssBaseline } from '@mui/material';

import theme from 'theme';

import PizzaEvents from 'components/PizzaEvents';
import { fetchAllPizzaEvents, fetchUpcomingPizzaEvents } from 'queries';

const queryClient = new QueryClient()

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
          <Container>
            <h1>Pizza Events</h1>
            <Grid container spacing={3}>
              <Grid item xs={6}>
                <Typography variant="h6" component="h6">Upcoming</Typography>
                <PizzaEvents queryKey={['upcomingPizzaEvents']} query={fetchUpcomingPizzaEvents}/>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="h6" component="h6">Old</Typography>
                <PizzaEvents queryKey={['allPizzaEvents']} query={fetchAllPizzaEvents}/>
              </Grid>
            </Grid>
          </Container>
      </QueryClientProvider>
    </ThemeProvider>
  );
}

export default App;
