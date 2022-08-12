import { useQuery } from '@tanstack/react-query'
import { IPizzaEvent, PizzaEventProps } from 'types';
import { Typography } from '@mui/material';

function PizzaEvents({ queryKey, query } : PizzaEventProps) {
  const { isLoading, error, data } = useQuery(
      queryKey,
      query
  )

  if (isLoading) return (
      <Typography variant="subtitle1">Loading...</Typography>
  )
      
  if (error) return (
    <Typography variant="subtitle1">Could not fetch pizza events</Typography>
    )

  console.log(queryKey, data);
    
  if (data === undefined || data.length == 0) {
      return (
          <Typography variant="subtitle1">No pizza events :(</Typography>
      )
  }

  return (
    <>
        {
            data.map((pizzaEvent : IPizzaEvent) => {
                return <PizzaEvent 
                    time={pizzaEvent.time} 
                    place={pizzaEvent.place} 
                    attendees={pizzaEvent.attendees} 
                />
            })
        }
    </>
  )
}

function PizzaEvent({time, place, attendees }: IPizzaEvent) {
    return (
        <>
            <p><b>{place}</b> - {time}</p>
            <ul>
                {attendees.map(attendee => {
                    return <li>{attendee}</li>
                })}
            </ul>
        </>
    )
}

export default PizzaEvents;